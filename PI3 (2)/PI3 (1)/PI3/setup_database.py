#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BOSS SHOPP Database Setup
Script para configurar e inicializar o banco de dados completo
"""

import mysql.connector
from mysql.connector import Error
import os
import sys
from pathlib import Path
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DatabaseSetup:
    """Classe para configuração inicial do banco de dados"""
    
    def __init__(self, host='localhost', port=3306, user='root', password='root'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None
        
    def connect_mysql(self):
        """Conectar ao MySQL (sem especificar database)"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                charset='utf8mb4'
            )
            
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                logger.info("Conectado ao MySQL")
                return True
                
        except Error as e:
            logger.error(f"Erro ao conectar ao MySQL: {e}")
            return False
    
    def create_database(self, database_name='boss_shopp_complete'):
        """Criar banco de dados se não existir"""
        try:
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
            self.cursor.execute(f"USE {database_name}")
            logger.info(f"Banco de dados '{database_name}' criado/selecionado")
            return True
        except Error as e:
            logger.error(f"Erro ao criar banco de dados: {e}")
            return False
    
    def execute_sql_file(self, file_path):
        """Executar arquivo SQL"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                sql_content = file.read()
            
            # Dividir por statements (usando ; como delimitador)
            statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
            
            for statement in statements:
                if statement.upper().startswith(('CREATE', 'INSERT', 'ALTER', 'DROP')):
                    try:
                        self.cursor.execute(statement)
                        self.connection.commit()
                    except Error as e:
                        if "already exists" not in str(e).lower():
                            logger.warning(f"Aviso ao executar statement: {e}")
            
            logger.info(f"Arquivo SQL '{file_path}' executado com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao executar arquivo SQL: {e}")
            return False
    
    def verify_installation(self):
        """Verificar se a instalação foi bem-sucedida"""
        try:
            # Verificar tabelas criadas
            self.cursor.execute("SHOW TABLES")
            tables = [table[0] for table in self.cursor.fetchall()]
            
            expected_tables = [
                'users', 'categories', 'products', 'product_images',
                'user_addresses', 'orders', 'order_items', 'cart_items',
                'favorites', 'product_reviews', 'coupons', 'coupon_usage',
                'payment_methods', 'payment_transactions', 'stock_movements',
                'notifications', 'system_settings'
            ]
            
            missing_tables = [table for table in expected_tables if table not in tables]
            
            if missing_tables:
                logger.error(f"Tabelas não encontradas: {missing_tables}")
                return False
            
            # Verificar dados iniciais
            self.cursor.execute("SELECT COUNT(*) FROM categories")
            category_count = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM products")
            product_count = self.cursor.fetchone()[0]
            
            logger.info(f"Verificação concluída:")
            logger.info(f"- {len(tables)} tabelas criadas")
            logger.info(f"- {category_count} categorias inseridas")
            logger.info(f"- {product_count} produtos inseridos")
            
            return True
            
        except Error as e:
            logger.error(f"Erro na verificação: {e}")
            return False
    
    def disconnect(self):
        """Fechar conexão"""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Conexão fechada")

def main():
    """Função principal de setup"""
    print("=" * 60)
    print("BOSS SHOPP - Configuração do Banco de Dados")
    print("=" * 60)
    
    # Obter configurações do usuário
    print("\nConfigurações do MySQL:")
    host = input("Host (localhost): ").strip() or "localhost"
    port = input("Porta (3306): ").strip() or "3306"
    user = input("Usuário (root): ").strip() or "root"
    password = input("Senha: ").strip()
    
    if not password:
        print("Senha é obrigatória!")
        sys.exit(1)
    
    try:
        port = int(port)
    except ValueError:
        print("Porta deve ser um número!")
        sys.exit(1)
    
    # Inicializar setup
    setup = DatabaseSetup(host, port, user, password)
    
    try:
        # Conectar ao MySQL
        if not setup.connect_mysql():
            print("Falha ao conectar ao MySQL. Verifique as configurações.")
            sys.exit(1)
        
        # Criar banco de dados
        database_name = input("\nNome do banco de dados (boss_shopp_complete): ").strip() or "boss_shopp_complete"
        
        if not setup.create_database(database_name):
            print("Falha ao criar banco de dados.")
            sys.exit(1)
        
        # Executar schema SQL
        schema_file = Path(__file__).parent / "database_schema.sql"
        
        if not schema_file.exists():
            print(f"Arquivo de schema não encontrado: {schema_file}")
            sys.exit(1)
        
        print(f"\nExecutando schema SQL: {schema_file}")
        if not setup.execute_sql_file(schema_file):
            print("Falha ao executar schema SQL.")
            sys.exit(1)
        
        # Verificar instalação
        print("\nVerificando instalação...")
        if setup.verify_installation():
            print("\n" + "=" * 60)
            print("✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
            print("=" * 60)
            print(f"\nBanco de dados: {database_name}")
            print(f"Host: {host}:{port}")
            print(f"Usuário: {user}")
            print("\nO banco de dados está pronto para uso!")
            print("\nPróximos passos:")
            print("1. Configure o arquivo database_manager.py com suas credenciais")
            print("2. Execute o backend do projeto")
            print("3. Acesse o frontend em seu navegador")
        else:
            print("❌ Falha na verificação da instalação.")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\nInstalação cancelada pelo usuário.")
        sys.exit(1)
    
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        sys.exit(1)
    
    finally:
        setup.disconnect()

if __name__ == "__main__":
    main()