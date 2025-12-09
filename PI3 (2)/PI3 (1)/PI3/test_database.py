#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BOSS SHOPP Database Tests
Testes completos para validar o sistema de banco de dados
"""

import unittest
import sys
import os
from datetime import datetime, timedelta
from decimal import Decimal

# Adicionar o diretório atual ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database_manager import BossShoppDatabase, DatabaseConfig

class TestBossShoppDatabase(unittest.TestCase):
    """Testes para a classe BossShoppDatabase"""
    
    @classmethod
    def setUpClass(cls):
        """Configuração inicial dos testes"""
        cls.config = DatabaseConfig(
            host='localhost',
            port=3306,
            user='root',
            password='root',  # Altere conforme necessário
            database='boss_shopp_test'  # Usar banco de teste
        )
        
        cls.db = BossShoppDatabase(cls.config)
        
        # Conectar e criar banco de teste
        if not cls.db.connect():
            raise Exception("Não foi possível conectar ao banco de dados para testes")
        
        # Criar banco de teste se não existir
        try:
            cls.db.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {cls.config.database}")
            cls.db.cursor.execute(f"USE {cls.config.database}")
            cls.db.connection.commit()
        except Exception as e:
            print(f"Erro ao criar banco de teste: {e}")
    
    @classmethod
    def tearDownClass(cls):
        """Limpeza após todos os testes"""
        if cls.db.connection:
            cls.db.disconnect()
    
    def setUp(self):
        """Configuração antes de cada teste"""
        # Limpar dados de teste
        self.cleanup_test_data()
    
    def tearDown(self):
        """Limpeza após cada teste"""
        self.cleanup_test_data()
    
    def cleanup_test_data(self):
        """Limpar dados de teste"""
        try:
            # Desabilitar verificação de chaves estrangeiras temporariamente
            self.db.cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            
            # Limpar tabelas na ordem correta
            tables = [
                'order_items', 'orders', 'cart_items', 'favorites',
                'product_reviews', 'user_addresses', 'users',
                'products', 'categories'
            ]
            
            for table in tables:
                try:
                    self.db.cursor.execute(f"DELETE FROM {table} WHERE id > 0")
                except:
                    pass  # Tabela pode não existir ainda
            
            # Reabilitar verificação de chaves estrangeiras
            self.db.cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            self.db.connection.commit()
            
        except Exception as e:
            print(f"Erro na limpeza: {e}")

class TestUserOperations(TestBossShoppDatabase):
    """Testes para operações de usuários"""
    
    def test_create_user(self):
        """Testar criação de usuário"""
        user_id = self.db.create_user(
            name="João Teste",
            email="joao.teste@example.com",
            password="senha123",
            phone="(11) 99999-9999",
            city="São Paulo",
            state="SP"
        )
        
        self.assertIsNotNone(user_id)
        self.assertIsInstance(user_id, int)
        self.assertGreater(user_id, 0)
    
    def test_authenticate_user(self):
        """Testar autenticação de usuário"""
        # Criar usuário
        user_id = self.db.create_user(
            name="Maria Teste",
            email="maria.teste@example.com",
            password="senha456"
        )
        
        self.assertIsNotNone(user_id)
        
        # Testar autenticação correta
        user = self.db.authenticate_user("maria.teste@example.com", "senha456")
        self.assertIsNotNone(user)
        self.assertEqual(user['email'], "maria.teste@example.com")
        self.assertEqual(user['name'], "Maria Teste")
        
        # Testar autenticação incorreta
        user_wrong = self.db.authenticate_user("maria.teste@example.com", "senha_errada")
        self.assertIsNone(user_wrong)
    
    def test_get_user_by_id(self):
        """Testar obtenção de usuário por ID"""
        # Criar usuário
        user_id = self.db.create_user(
            name="Pedro Teste",
            email="pedro.teste@example.com",
            password="senha789"
        )
        
        # Obter usuário
        user = self.db.get_user_by_id(user_id)
        self.assertIsNotNone(user)
        self.assertEqual(user['id'], user_id)
        self.assertEqual(user['name'], "Pedro Teste")
        self.assertNotIn('password', user)  # Senha não deve ser retornada
    
    def test_update_user(self):
        """Testar atualização de usuário"""
        # Criar usuário
        user_id = self.db.create_user(
            name="Ana Teste",
            email="ana.teste@example.com",
            password="senha000"
        )
        
        # Atualizar dados
        success = self.db.update_user(
            user_id,
            name="Ana Silva Teste",
            phone="(11) 88888-8888",
            city="Rio de Janeiro",
            state="RJ"
        )
        
        self.assertTrue(success)
        
        # Verificar atualização
        user = self.db.get_user_by_id(user_id)
        self.assertEqual(user['name'], "Ana Silva Teste")
        self.assertEqual(user['phone'], "(11) 88888-8888")
        self.assertEqual(user['city'], "Rio de Janeiro")

class TestProductOperations(TestBossShoppDatabase):
    """Testes para operações de produtos"""
    
    def setUp(self):
        """Configuração específica para testes de produtos"""
        super().setUp()
        
        # Criar categoria de teste
        self.db.cursor.execute("""
            INSERT INTO categories (name, slug, description)
            VALUES ('Teste', 'teste', 'Categoria de teste')
        """)
        self.db.connection.commit()
        self.category_id = self.db.get_last_insert_id()
    
    def test_get_categories(self):
        """Testar obtenção de categorias"""
        categories = self.db.get_categories()
        self.assertIsInstance(categories, list)
        self.assertGreater(len(categories), 0)
        
        # Verificar se nossa categoria de teste está lá
        category_names = [cat['name'] for cat in categories]
        self.assertIn('Teste', category_names)
    
    def test_create_and_get_products(self):
        """Testar criação e obtenção de produtos"""
        # Inserir produto de teste
        self.db.cursor.execute("""
            INSERT INTO products (name, description, price, category_id, stock_quantity)
            VALUES ('Produto Teste', 'Descrição do produto teste', 99.90, %s, 10)
        """, (self.category_id,))
        self.db.connection.commit()
        product_id = self.db.get_last_insert_id()
        
        # Testar obtenção de produtos
        products = self.db.get_products()
        self.assertIsInstance(products, list)
        self.assertGreater(len(products), 0)
        
        # Verificar se nosso produto está lá
        product_names = [prod['name'] for prod in products]
        self.assertIn('Produto Teste', product_names)
        
        # Testar obtenção por ID
        product = self.db.get_product_by_id(product_id)
        self.assertIsNotNone(product)
        self.assertEqual(product['name'], 'Produto Teste')
        self.assertEqual(float(product['price']), 99.90)
    
    def test_search_products(self):
        """Testar busca de produtos"""
        # Inserir produtos de teste
        products_data = [
            ('Smartphone Samsung', 'Smartphone Android', 1500.00),
            ('iPhone Apple', 'Smartphone iOS', 2000.00),
            ('Notebook Dell', 'Computador portátil', 2500.00)
        ]
        
        for name, desc, price in products_data:
            self.db.cursor.execute("""
                INSERT INTO products (name, description, price, category_id, stock_quantity)
                VALUES (%s, %s, %s, %s, 5)
            """, (name, desc, price, self.category_id))
        
        self.db.connection.commit()
        
        # Testar busca
        results = self.db.search_products("Smartphone")
        self.assertGreater(len(results), 0)
        
        # Verificar se encontrou os smartphones
        found_names = [prod['name'] for prod in results]
        self.assertIn('Smartphone Samsung', found_names)
        self.assertIn('iPhone Apple', found_names)
        self.assertNotIn('Notebook Dell', found_names)

class TestCartOperations(TestBossShoppDatabase):
    """Testes para operações de carrinho"""
    
    def setUp(self):
        """Configuração específica para testes de carrinho"""
        super().setUp()
        
        # Criar usuário de teste
        self.user_id = self.db.create_user(
            name="Usuário Carrinho",
            email="carrinho@example.com",
            password="senha123"
        )
        
        # Criar categoria e produto de teste
        self.db.cursor.execute("""
            INSERT INTO categories (name, slug, description)
            VALUES ('Carrinho Teste', 'carrinho-teste', 'Categoria para teste de carrinho')
        """)
        self.db.connection.commit()
        category_id = self.db.get_last_insert_id()
        
        self.db.cursor.execute("""
            INSERT INTO products (name, description, price, category_id, stock_quantity)
            VALUES ('Produto Carrinho', 'Produto para teste de carrinho', 50.00, %s, 20)
        """, (category_id,))
        self.db.connection.commit()
        self.product_id = self.db.get_last_insert_id()
    
    def test_add_to_cart(self):
        """Testar adição ao carrinho"""
        success = self.db.add_to_cart(self.user_id, self.product_id, 2)
        self.assertTrue(success)
        
        # Verificar se foi adicionado
        cart_items = self.db.get_cart_items(self.user_id)
        self.assertEqual(len(cart_items), 1)
        self.assertEqual(cart_items[0]['quantity'], 2)
        self.assertEqual(cart_items[0]['product_id'], self.product_id)
    
    def test_update_cart_item(self):
        """Testar atualização de item do carrinho"""
        # Adicionar item
        self.db.add_to_cart(self.user_id, self.product_id, 1)
        
        # Atualizar quantidade
        success = self.db.update_cart_item(self.user_id, self.product_id, 5)
        self.assertTrue(success)
        
        # Verificar atualização
        cart_items = self.db.get_cart_items(self.user_id)
        self.assertEqual(cart_items[0]['quantity'], 5)
    
    def test_remove_from_cart(self):
        """Testar remoção do carrinho"""
        # Adicionar item
        self.db.add_to_cart(self.user_id, self.product_id, 1)
        
        # Verificar que foi adicionado
        cart_items = self.db.get_cart_items(self.user_id)
        self.assertEqual(len(cart_items), 1)
        
        # Remover item
        success = self.db.remove_from_cart(self.user_id, self.product_id)
        self.assertTrue(success)
        
        # Verificar que foi removido
        cart_items = self.db.get_cart_items(self.user_id)
        self.assertEqual(len(cart_items), 0)
    
    def test_clear_cart(self):
        """Testar limpeza do carrinho"""
        # Adicionar múltiplos itens
        self.db.add_to_cart(self.user_id, self.product_id, 2)
        
        # Criar outro produto
        self.db.cursor.execute("""
            INSERT INTO products (name, description, price, category_id, stock_quantity)
            VALUES ('Produto 2', 'Segundo produto', 30.00, 
                   (SELECT id FROM categories WHERE slug = 'carrinho-teste'), 15)
        """)
        self.db.connection.commit()
        product_id_2 = self.db.get_last_insert_id()
        
        self.db.add_to_cart(self.user_id, product_id_2, 1)
        
        # Verificar que temos 2 itens
        cart_items = self.db.get_cart_items(self.user_id)
        self.assertEqual(len(cart_items), 2)
        
        # Limpar carrinho
        success = self.db.clear_cart(self.user_id)
        self.assertTrue(success)
        
        # Verificar que está vazio
        cart_items = self.db.get_cart_items(self.user_id)
        self.assertEqual(len(cart_items), 0)

class TestOrderOperations(TestBossShoppDatabase):
    """Testes para operações de pedidos"""
    
    def setUp(self):
        """Configuração específica para testes de pedidos"""
        super().setUp()
        
        # Criar usuário de teste
        self.user_id = self.db.create_user(
            name="Usuário Pedido",
            email="pedido@example.com",
            password="senha123"
        )
        
        # Criar endereço de teste
        self.address_id = self.db.add_user_address(
            user_id=self.user_id,
            name="Casa",
            street="Rua Teste",
            number="123",
            neighborhood="Bairro Teste",
            city="São Paulo",
            state="SP",
            zip_code="01234-567"
        )
        
        # Criar categoria e produtos de teste
        self.db.cursor.execute("""
            INSERT INTO categories (name, slug, description)
            VALUES ('Pedido Teste', 'pedido-teste', 'Categoria para teste de pedidos')
        """)
        self.db.connection.commit()
        category_id = self.db.get_last_insert_id()
        
        # Criar produtos
        self.products = []
        for i in range(3):
            self.db.cursor.execute("""
                INSERT INTO products (name, description, price, category_id, stock_quantity)
                VALUES (%s, %s, %s, %s, 10)
            """, (f'Produto {i+1}', f'Descrição do produto {i+1}', (i+1) * 25.00, category_id))
            self.db.connection.commit()
            self.products.append(self.db.get_last_insert_id())
    
    def test_create_order(self):
        """Testar criação de pedido"""
        # Preparar itens do pedido
        items = [
            {'product_id': self.products[0], 'quantity': 2, 'price': 25.00},
            {'product_id': self.products[1], 'quantity': 1, 'price': 50.00}
        ]
        
        # Criar pedido
        order_id = self.db.create_order(
            user_id=self.user_id,
            items=items,
            shipping_address_id=self.address_id,
            payment_method='credit_card'
        )
        
        self.assertIsNotNone(order_id)
        self.assertIsInstance(order_id, int)
        
        # Verificar pedido criado
        order = self.db.get_order_by_id(order_id, self.user_id)
        self.assertIsNotNone(order)
        self.assertEqual(order['user_id'], self.user_id)
        self.assertEqual(float(order['total_amount']), 100.00)  # 2*25 + 1*50
        
        # Verificar itens do pedido
        order_items = self.db.get_order_items(order_id)
        self.assertEqual(len(order_items), 2)
    
    def test_get_user_orders(self):
        """Testar obtenção de pedidos do usuário"""
        # Criar alguns pedidos
        items1 = [{'product_id': self.products[0], 'quantity': 1, 'price': 25.00}]
        items2 = [{'product_id': self.products[1], 'quantity': 2, 'price': 50.00}]
        
        order_id1 = self.db.create_order(self.user_id, items1, self.address_id, 'pix')
        order_id2 = self.db.create_order(self.user_id, items2, self.address_id, 'boleto')
        
        # Obter pedidos do usuário
        orders = self.db.get_user_orders(self.user_id)
        self.assertEqual(len(orders), 2)
        
        # Verificar se os pedidos estão corretos
        order_ids = [order['id'] for order in orders]
        self.assertIn(order_id1, order_ids)
        self.assertIn(order_id2, order_ids)
    
    def test_update_order_status(self):
        """Testar atualização de status do pedido"""
        # Criar pedido
        items = [{'product_id': self.products[0], 'quantity': 1, 'price': 25.00}]
        order_id = self.db.create_order(self.user_id, items, self.address_id, 'credit_card')
        
        # Atualizar status
        success = self.db.update_order_status(order_id, 'processing')
        self.assertTrue(success)
        
        # Verificar atualização
        order = self.db.get_order_by_id(order_id, self.user_id)
        self.assertEqual(order['status'], 'processing')

class TestFavoriteOperations(TestBossShoppDatabase):
    """Testes para operações de favoritos"""
    
    def setUp(self):
        """Configuração específica para testes de favoritos"""
        super().setUp()
        
        # Criar usuário de teste
        self.user_id = self.db.create_user(
            name="Usuário Favoritos",
            email="favoritos@example.com",
            password="senha123"
        )
        
        # Criar categoria e produto de teste
        self.db.cursor.execute("""
            INSERT INTO categories (name, slug, description)
            VALUES ('Favoritos Teste', 'favoritos-teste', 'Categoria para teste de favoritos')
        """)
        self.db.connection.commit()
        category_id = self.db.get_last_insert_id()
        
        self.db.cursor.execute("""
            INSERT INTO products (name, description, price, category_id, stock_quantity)
            VALUES ('Produto Favorito', 'Produto para teste de favoritos', 75.00, %s, 5)
        """, (category_id,))
        self.db.connection.commit()
        self.product_id = self.db.get_last_insert_id()
    
    def test_add_to_favorites(self):
        """Testar adição aos favoritos"""
        success = self.db.add_to_favorites(self.user_id, self.product_id)
        self.assertTrue(success)
        
        # Verificar se foi adicionado
        favorites = self.db.get_user_favorites(self.user_id)
        self.assertEqual(len(favorites), 1)
        self.assertEqual(favorites[0]['product_id'], self.product_id)
    
    def test_remove_from_favorites(self):
        """Testar remoção dos favoritos"""
        # Adicionar aos favoritos
        self.db.add_to_favorites(self.user_id, self.product_id)
        
        # Verificar que foi adicionado
        favorites = self.db.get_user_favorites(self.user_id)
        self.assertEqual(len(favorites), 1)
        
        # Remover dos favoritos
        success = self.db.remove_from_favorites(self.user_id, self.product_id)
        self.assertTrue(success)
        
        # Verificar que foi removido
        favorites = self.db.get_user_favorites(self.user_id)
        self.assertEqual(len(favorites), 0)

def run_tests():
    """Executar todos os testes"""
    print("=" * 60)
    print("BOSS SHOPP - Testes do Sistema de Banco de Dados")
    print("=" * 60)
    
    # Configurar suite de testes
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Adicionar classes de teste
    test_classes = [
        TestUserOperations,
        TestProductOperations,
        TestCartOperations,
        TestOrderOperations,
        TestFavoriteOperations
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Executar testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resultado final
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("✅ TODOS OS TESTES PASSARAM!")
        print(f"Executados: {result.testsRun} testes")
    else:
        print("❌ ALGUNS TESTES FALHARAM!")
        print(f"Executados: {result.testsRun} testes")
        print(f"Falhas: {len(result.failures)}")
        print(f"Erros: {len(result.errors)}")
    print("=" * 60)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)