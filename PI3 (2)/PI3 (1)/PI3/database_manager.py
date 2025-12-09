#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BOSS SHOPP Database Manager
Sistema completo de gerenciamento do banco de dados do e-commerce
Baseado na análise completa do código do projeto
"""

import mysql.connector
from mysql.connector import Error
import bcrypt
import json
from datetime import datetime, timedelta
from decimal import Decimal
import logging
from typing import Dict, List, Optional, Tuple, Any
import os
from dataclasses import dataclass

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DatabaseConfig:
    """Configuração do banco de dados"""
    host: str = 'localhost'
    port: int = 3306
    user: str = 'root'
    password: str = 'root'
    database: str = 'boss_shopp_complete'
    charset: str = 'utf8mb4'
    autocommit: bool = False

class BossShoppDatabase:
    """Classe principal para gerenciamento do banco de dados do BOSS SHOPP"""
    
    def __init__(self, config: DatabaseConfig = None):
        """Inicializar conexão com o banco de dados"""
        self.config = config or DatabaseConfig()
        self.connection = None
        self.cursor = None
        
    def connect(self) -> bool:
        """Estabelecer conexão com o banco de dados"""
        try:
            self.connection = mysql.connector.connect(
                host=self.config.host,
                port=self.config.port,
                user=self.config.user,
                password=self.config.password,
                database=self.config.database,
                charset=self.config.charset,
                autocommit=self.config.autocommit
            )
            
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                logger.info(f"Conectado ao banco de dados {self.config.database}")
                return True
                
        except Error as e:
            logger.error(f"Erro ao conectar ao banco de dados: {e}")
            return False
    
    def disconnect(self):
        """Fechar conexão com o banco de dados"""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Conexão com o banco de dados fechada")
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """Executar query SELECT e retornar resultados"""
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except Error as e:
            logger.error(f"Erro ao executar query: {e}")
            return []
    
    def execute_update(self, query: str, params: tuple = None) -> bool:
        """Executar query INSERT/UPDATE/DELETE"""
        try:
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return True
        except Error as e:
            logger.error(f"Erro ao executar update: {e}")
            self.connection.rollback()
            return False
    
    def get_last_insert_id(self) -> int:
        """Obter o último ID inserido"""
        return self.cursor.lastrowid

    # =====================================================
    # MÉTODOS PARA USUÁRIOS
    # =====================================================
    
    def create_user(self, name: str, email: str, password: str, **kwargs) -> Optional[int]:
        """Criar novo usuário"""
        # Hash da senha
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        query = """
        INSERT INTO users (name, email, password, phone, address, city, state, 
                          zip_code, country, date_of_birth)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        params = (
            name, email, hashed_password,
            kwargs.get('phone'), kwargs.get('address'), kwargs.get('city'),
            kwargs.get('state'), kwargs.get('zip_code', ''),
            kwargs.get('country', 'Brasil'), kwargs.get('date_of_birth')
        )
        
        if self.execute_update(query, params):
            return self.get_last_insert_id()
        return None
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        """Autenticar usuário"""
        query = "SELECT * FROM users WHERE email = %s AND is_active = TRUE"
        users = self.execute_query(query, (email,))
        
        if users and bcrypt.checkpw(password.encode('utf-8'), users[0]['password'].encode('utf-8')):
            user = users[0].copy()
            del user['password']  # Remover senha do retorno
            return user
        return None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Obter usuário por ID"""
        query = "SELECT * FROM users WHERE id = %s AND is_active = TRUE"
        users = self.execute_query(query, (user_id,))
        if users:
            user = users[0].copy()
            del user['password']
            return user
        return None
    
    def update_user(self, user_id: int, **kwargs) -> bool:
        """Atualizar dados do usuário"""
        fields = []
        values = []
        
        for field in ['name', 'phone', 'address', 'city', 'state', 'zip_code', 'country', 'date_of_birth']:
            if field in kwargs:
                fields.append(f"{field} = %s")
                values.append(kwargs[field])
        
        if not fields:
            return False
        
        query = f"UPDATE users SET {', '.join(fields)} WHERE id = %s"
        values.append(user_id)
        
        return self.execute_update(query, tuple(values))

    # =====================================================
    # MÉTODOS PARA PRODUTOS
    # =====================================================
    
    def get_products(self, category_slug: str = None, limit: int = None, 
                    featured_only: bool = False) -> List[Dict]:
        """Obter lista de produtos"""
        query = """
        SELECT p.*, c.name as category_name, c.slug as category_slug
        FROM products p
        JOIN categories c ON p.category_id = c.id
        WHERE p.is_active = TRUE AND c.is_active = TRUE
        """
        params = []
        
        if category_slug:
            query += " AND c.slug = %s"
            params.append(category_slug)
        
        if featured_only:
            query += " AND p.is_featured = TRUE"
        
        query += " ORDER BY p.created_at DESC"
        
        if limit:
            query += " LIMIT %s"
            params.append(limit)
        
        return self.execute_query(query, tuple(params) if params else None)
    
    def get_product_by_id(self, product_id: int) -> Optional[Dict]:
        """Obter produto por ID"""
        query = """
        SELECT p.*, c.name as category_name, c.slug as category_slug
        FROM products p
        JOIN categories c ON p.category_id = c.id
        WHERE p.id = %s AND p.is_active = TRUE
        """
        products = self.execute_query(query, (product_id,))
        return products[0] if products else None
    
    def search_products(self, search_term: str, limit: int = 20) -> List[Dict]:
        """Buscar produtos por termo"""
        query = """
        SELECT p.*, c.name as category_name, c.slug as category_slug
        FROM products p
        JOIN categories c ON p.category_id = c.id
        WHERE p.is_active = TRUE AND c.is_active = TRUE
        AND (p.name LIKE %s OR p.description LIKE %s)
        ORDER BY p.name
        LIMIT %s
        """
        search_pattern = f"%{search_term}%"
        return self.execute_query(query, (search_pattern, search_pattern, limit))
    
    def get_categories(self) -> List[Dict]:
        """Obter todas as categorias ativas"""
        query = """
        SELECT c.*, COUNT(p.id) as product_count
        FROM categories c
        LEFT JOIN products p ON c.id = p.category_id AND p.is_active = TRUE
        WHERE c.is_active = TRUE
        GROUP BY c.id
        ORDER BY c.sort_order, c.name
        """
        return self.execute_query(query)

    # =====================================================
    # MÉTODOS PARA CARRINHO
    # =====================================================
    
    def add_to_cart(self, user_id: int, product_id: int, quantity: int = 1) -> bool:
        """Adicionar produto ao carrinho"""
        # Verificar se produto já está no carrinho
        existing = self.execute_query(
            "SELECT * FROM cart_items WHERE user_id = %s AND product_id = %s",
            (user_id, product_id)
        )
        
        if existing:
            # Atualizar quantidade
            query = """
            UPDATE cart_items 
            SET quantity = quantity + %s, updated_at = NOW()
            WHERE user_id = %s AND product_id = %s
            """
            return self.execute_update(query, (quantity, user_id, product_id))
        else:
            # Inserir novo item
            query = """
            INSERT INTO cart_items (user_id, product_id, quantity)
            VALUES (%s, %s, %s)
            """
            return self.execute_update(query, (user_id, product_id, quantity))
    
    def get_cart_items(self, user_id: int) -> List[Dict]:
        """Obter itens do carrinho do usuário"""
        query = """
        SELECT ci.*, p.name, p.price, p.image_url, p.stock_quantity,
               (ci.quantity * p.price) as subtotal
        FROM cart_items ci
        JOIN products p ON ci.product_id = p.id
        WHERE ci.user_id = %s AND p.is_active = TRUE
        ORDER BY ci.created_at DESC
        """
        return self.execute_query(query, (user_id,))
    
    def update_cart_item(self, user_id: int, product_id: int, quantity: int) -> bool:
        """Atualizar quantidade de item no carrinho"""
        if quantity <= 0:
            return self.remove_from_cart(user_id, product_id)
        
        query = """
        UPDATE cart_items 
        SET quantity = %s, updated_at = NOW()
        WHERE user_id = %s AND product_id = %s
        """
        return self.execute_update(query, (quantity, user_id, product_id))
    
    def remove_from_cart(self, user_id: int, product_id: int) -> bool:
        """Remover item do carrinho"""
        query = "DELETE FROM cart_items WHERE user_id = %s AND product_id = %s"
        return self.execute_update(query, (user_id, product_id))
    
    def clear_cart(self, user_id: int) -> bool:
        """Limpar carrinho do usuário"""
        query = "DELETE FROM cart_items WHERE user_id = %s"
        return self.execute_update(query, (user_id,))

    # =====================================================
    # MÉTODOS PARA FAVORITOS
    # =====================================================
    
    def add_to_favorites(self, user_id: int, product_id: int) -> bool:
        """Adicionar produto aos favoritos"""
        query = """
        INSERT IGNORE INTO favorites (user_id, product_id)
        VALUES (%s, %s)
        """
        return self.execute_update(query, (user_id, product_id))
    
    def remove_from_favorites(self, user_id: int, product_id: int) -> bool:
        """Remover produto dos favoritos"""
        query = "DELETE FROM favorites WHERE user_id = %s AND product_id = %s"
        return self.execute_update(query, (user_id, product_id))
    
    def get_user_favorites(self, user_id: int) -> List[Dict]:
        """Obter favoritos do usuário"""
        query = """
        SELECT f.*, p.name, p.price, p.image_url, p.rating
        FROM favorites f
        JOIN products p ON f.product_id = p.id
        WHERE f.user_id = %s AND p.is_active = TRUE
        ORDER BY f.created_at DESC
        """
        return self.execute_query(query, (user_id,))

    # =====================================================
    # MÉTODOS PARA PEDIDOS
    # =====================================================
    
    def create_order(self, user_id: int, items: List[Dict], 
                    shipping_address_id: int, payment_method: str, **kwargs) -> Optional[int]:
        """Criar novo pedido"""
        try:
            # Calcular total
            total_amount = sum(Decimal(str(item['price'])) * item['quantity'] for item in items)
            
            # Inserir pedido
            order_query = """
            INSERT INTO orders (user_id, total_amount, shipping_address_id, 
                              payment_method, status, payment_status)
            VALUES (%s, %s, %s, %s, 'pending', 'pending')
            """
            
            if self.execute_update(order_query, (user_id, total_amount, shipping_address_id, payment_method)):
                order_id = self.get_last_insert_id()
                
                # Inserir itens do pedido
                for item in items:
                    item_query = """
                    INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    unit_price = Decimal(str(item['price']))
                    total_price = unit_price * item['quantity']
                    
                    self.execute_update(item_query, (
                        order_id, item['product_id'], item['quantity'], 
                        unit_price, total_price
                    ))
                
                # Limpar carrinho
                self.clear_cart(user_id)
                
                return order_id
                
        except Exception as e:
            logger.error(f"Erro ao criar pedido: {e}")
            self.connection.rollback()
        
        return None
    
    def get_user_orders(self, user_id: int, limit: int = None) -> List[Dict]:
        """Obter pedidos do usuário"""
        query = """
        SELECT o.*, COUNT(oi.id) as item_count
        FROM orders o
        LEFT JOIN order_items oi ON o.id = oi.order_id
        WHERE o.user_id = %s
        GROUP BY o.id
        ORDER BY o.created_at DESC
        """
        
        params = [user_id]
        if limit:
            query += " LIMIT %s"
            params.append(limit)
        
        return self.execute_query(query, tuple(params))
    
    def get_order_by_id(self, order_id: int, user_id: int = None) -> Optional[Dict]:
        """Obter pedido por ID"""
        query = """
        SELECT o.*, ua.street, ua.number, ua.neighborhood, ua.city, ua.state, ua.zip_code
        FROM orders o
        LEFT JOIN user_addresses ua ON o.shipping_address_id = ua.id
        WHERE o.id = %s
        """
        
        params = [order_id]
        if user_id:
            query += " AND o.user_id = %s"
            params.append(user_id)
        
        orders = self.execute_query(query, tuple(params))
        return orders[0] if orders else None
    
    def get_order_items(self, order_id: int) -> List[Dict]:
        """Obter itens de um pedido"""
        query = """
        SELECT oi.*, p.name, p.image_url
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id = %s
        """
        return self.execute_query(query, (order_id,))
    
    def update_order_status(self, order_id: int, status: str) -> bool:
        """Atualizar status do pedido"""
        query = "UPDATE orders SET status = %s, updated_at = NOW() WHERE id = %s"
        return self.execute_update(query, (status, order_id))

    # =====================================================
    # MÉTODOS PARA ENDEREÇOS
    # =====================================================
    
    def add_user_address(self, user_id: int, name: str, street: str, number: str,
                        neighborhood: str, city: str, state: str, zip_code: str, **kwargs) -> Optional[int]:
        """Adicionar endereço do usuário"""
        query = """
        INSERT INTO user_addresses (user_id, name, street, number, complement,
                                  neighborhood, city, state, zip_code, country, is_default)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        params = (
            user_id, name, street, number, kwargs.get('complement', ''),
            neighborhood, city, state, zip_code, kwargs.get('country', 'Brasil'),
            kwargs.get('is_default', False)
        )
        
        if self.execute_update(query, params):
            return self.get_last_insert_id()
        return None
    
    def get_user_addresses(self, user_id: int) -> List[Dict]:
        """Obter endereços do usuário"""
        query = """
        SELECT * FROM user_addresses 
        WHERE user_id = %s 
        ORDER BY is_default DESC, created_at DESC
        """
        return self.execute_query(query, (user_id,))

    # =====================================================
    # MÉTODOS PARA AVALIAÇÕES
    # =====================================================
    
    def add_product_review(self, product_id: int, user_id: int, rating: int, 
                          title: str = None, comment: str = None) -> Optional[int]:
        """Adicionar avaliação do produto"""
        query = """
        INSERT INTO product_reviews (product_id, user_id, rating, title, comment)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        rating = VALUES(rating), title = VALUES(title), comment = VALUES(comment),
        updated_at = NOW()
        """
        
        if self.execute_update(query, (product_id, user_id, rating, title, comment)):
            return self.get_last_insert_id()
        return None
    
    def get_product_reviews(self, product_id: int, limit: int = 10) -> List[Dict]:
        """Obter avaliações do produto"""
        query = """
        SELECT pr.*, u.name as user_name
        FROM product_reviews pr
        JOIN users u ON pr.user_id = u.id
        WHERE pr.product_id = %s AND pr.is_approved = TRUE
        ORDER BY pr.created_at DESC
        LIMIT %s
        """
        return self.execute_query(query, (product_id, limit))

    # =====================================================
    # MÉTODOS PARA RELATÓRIOS E ESTATÍSTICAS
    # =====================================================
    
    def get_sales_statistics(self, start_date: datetime = None, end_date: datetime = None) -> Dict:
        """Obter estatísticas de vendas"""
        where_clause = "WHERE o.status IN ('delivered', 'shipped')"
        params = []
        
        if start_date:
            where_clause += " AND o.created_at >= %s"
            params.append(start_date)
        
        if end_date:
            where_clause += " AND o.created_at <= %s"
            params.append(end_date)
        
        query = f"""
        SELECT 
            COUNT(*) as total_orders,
            SUM(total_amount) as total_revenue,
            AVG(total_amount) as average_order_value,
            MIN(total_amount) as min_order_value,
            MAX(total_amount) as max_order_value
        FROM orders o
        {where_clause}
        """
        
        result = self.execute_query(query, tuple(params) if params else None)
        return result[0] if result else {}
    
    def get_top_products(self, limit: int = 10) -> List[Dict]:
        """Obter produtos mais vendidos"""
        query = """
        SELECT p.*, SUM(oi.quantity) as total_sold
        FROM products p
        JOIN order_items oi ON p.id = oi.product_id
        JOIN orders o ON oi.order_id = o.id
        WHERE o.status IN ('delivered', 'shipped')
        GROUP BY p.id
        ORDER BY total_sold DESC
        LIMIT %s
        """
        return self.execute_query(query, (limit,))
    
    def get_user_statistics(self) -> Dict:
        """Obter estatísticas de usuários"""
        query = """
        SELECT 
            COUNT(*) as total_users,
            COUNT(CASE WHEN created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY) THEN 1 END) as new_users_30_days,
            COUNT(CASE WHEN is_active = TRUE THEN 1 END) as active_users
        FROM users
        """
        result = self.execute_query(query)
        return result[0] if result else {}

    # =====================================================
    # MÉTODOS UTILITÁRIOS
    # =====================================================
    
    def backup_database(self, backup_path: str) -> bool:
        """Fazer backup do banco de dados"""
        try:
            import subprocess
            
            cmd = [
                'mysqldump',
                f'--host={self.config.host}',
                f'--port={self.config.port}',
                f'--user={self.config.user}',
                f'--password={self.config.password}',
                '--single-transaction',
                '--routines',
                '--triggers',
                self.config.database
            ]
            
            with open(backup_path, 'w') as f:
                subprocess.run(cmd, stdout=f, check=True)
            
            logger.info(f"Backup criado em: {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao criar backup: {e}")
            return False
    
    def get_system_settings(self) -> Dict[str, str]:
        """Obter configurações do sistema"""
        query = "SELECT setting_key, setting_value FROM system_settings WHERE is_active = TRUE"
        results = self.execute_query(query)
        return {row['setting_key']: row['setting_value'] for row in results}
    
    def update_system_setting(self, key: str, value: str) -> bool:
        """Atualizar configuração do sistema"""
        query = """
        INSERT INTO system_settings (setting_key, setting_value)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE setting_value = VALUES(setting_value), updated_at = NOW()
        """
        return self.execute_update(query, (key, value))

# =====================================================
# EXEMPLO DE USO
# =====================================================

def main():
    """Exemplo de uso da classe BossShoppDatabase"""
    
    # Configurar banco
    config = DatabaseConfig(
        host='localhost',
        port=3306,
        user='root',
        password='root',
        database='boss_shopp_complete'
    )
    
    # Conectar ao banco
    db = BossShoppDatabase(config)
    
    if not db.connect():
        print("Erro ao conectar ao banco de dados")
        return
    
    try:
        # Exemplo: Criar usuário
        user_id = db.create_user(
            name="João Silva",
            email="joao@example.com",
            password="senha123",
            phone="(11) 99999-9999",
            city="São Paulo",
            state="SP"
        )
        
        if user_id:
            print(f"Usuário criado com ID: {user_id}")
            
            # Exemplo: Obter produtos
            products = db.get_products(limit=5)
            print(f"Encontrados {len(products)} produtos")
            
            # Exemplo: Adicionar ao carrinho
            if products:
                db.add_to_cart(user_id, products[0]['id'], 2)
                print("Produto adicionado ao carrinho")
                
                # Exemplo: Ver carrinho
                cart_items = db.get_cart_items(user_id)
                print(f"Carrinho tem {len(cart_items)} itens")
        
        # Exemplo: Estatísticas
        stats = db.get_sales_statistics()
        print(f"Estatísticas de vendas: {stats}")
        
    finally:
        db.disconnect()

if __name__ == "__main__":
    main()