#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BOSS SHOPP - Exemplo Prático de Uso
Demonstração completa das funcionalidades do sistema de banco de dados
"""

import sys
import os
from datetime import datetime, timedelta
from decimal import Decimal

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database_manager import BossShoppDatabase, DatabaseConfig

def print_separator(title=""):
    """Imprimir separador visual"""
    print("\n" + "=" * 60)
    if title:
        print(f" {title}")
        print("=" * 60)
    else:
        print("=" * 60)

def print_subsection(title):
    """Imprimir subsecção"""
    print(f"\n--- {title} ---")

def main():
    """Demonstração completa do sistema BOSS SHOPP"""
    
    print_separator("BOSS SHOPP - Demonstração do Sistema de Banco de Dados")
    
    # Configurar conexão
    config = DatabaseConfig(
        host='localhost',
        port=3306,
        user='root',
        password='root',  # Altere conforme necessário
        database='boss_shopp_complete'
    )
    
    # Conectar ao banco
    db = BossShoppDatabase(config)
    
    if not db.connect():
        print("❌ Erro ao conectar ao banco de dados!")
        print("Verifique se:")
        print("1. MySQL está rodando")
        print("2. Credenciais estão corretas")
        print("3. Banco de dados foi criado (execute setup_database.py)")
        return
    
    print("✅ Conectado ao banco de dados com sucesso!")
    
    try:
        # =====================================================
        # 1. DEMONSTRAÇÃO DE USUÁRIOS
        # =====================================================
        
        print_separator("1. GERENCIAMENTO DE USUÁRIOS")
        
        print_subsection("Criando usuários")
        
        # Criar usuários de exemplo
        users_data = [
            {
                'name': 'João Silva',
                'email': 'joao.silva@email.com',
                'password': 'senha123',
                'phone': '(11) 99999-1111',
                'city': 'São Paulo',
                'state': 'SP'
            },
            {
                'name': 'Maria Santos',
                'email': 'maria.santos@email.com',
                'password': 'senha456',
                'phone': '(21) 88888-2222',
                'city': 'Rio de Janeiro',
                'state': 'RJ'
            },
            {
                'name': 'Pedro Oliveira',
                'email': 'pedro.oliveira@email.com',
                'password': 'senha789',
                'phone': '(31) 77777-3333',
                'city': 'Belo Horizonte',
                'state': 'MG'
            }
        ]
        
        created_users = []
        for user_data in users_data:
            user_id = db.create_user(**user_data)
            if user_id:
                created_users.append(user_id)
                print(f"✅ Usuário criado: {user_data['name']} (ID: {user_id})")
            else:
                print(f"❌ Erro ao criar usuário: {user_data['name']}")
        
        print_subsection("Testando autenticação")
        
        # Testar autenticação
        user = db.authenticate_user('joao.silva@email.com', 'senha123')
        if user:
            print(f"✅ Login bem-sucedido: {user['name']} ({user['email']})")
            main_user_id = user['id']
        else:
            print("❌ Falha na autenticação")
            return
        
        # Testar senha incorreta
        user_wrong = db.authenticate_user('joao.silva@email.com', 'senha_errada')
        if user_wrong:
            print("❌ ERRO: Autenticação deveria ter falhado!")
        else:
            print("✅ Senha incorreta rejeitada corretamente")
        
        # =====================================================
        # 2. DEMONSTRAÇÃO DE PRODUTOS E CATEGORIAS
        # =====================================================
        
        print_separator("2. CATÁLOGO DE PRODUTOS")
        
        print_subsection("Listando categorias")
        
        categories = db.get_categories()
        print(f"📂 Encontradas {len(categories)} categorias:")
        for category in categories:
            print(f"   - {category['name']} ({category['slug']}) - {category['product_count']} produtos")
        
        print_subsection("Listando produtos por categoria")
        
        # Mostrar produtos de algumas categorias
        for category_slug in ['moda', 'eletronicos', 'casa']:
            products = db.get_products(category_slug=category_slug, limit=3)
            if products:
                print(f"\n📦 Produtos da categoria '{category_slug}':")
                for product in products:
                    price_str = f"R$ {float(product['price']):.2f}".replace('.', ',')
                    rating_str = f"⭐ {float(product['rating']):.1f}" if product['rating'] else "Sem avaliação"
                    print(f"   - {product['name']} - {price_str} - {rating_str}")
        
        print_subsection("Buscando produtos")
        
        # Testar busca
        search_results = db.search_products("smartphone", limit=5)
        print(f"\n🔍 Resultados da busca por 'smartphone': {len(search_results)} produtos")
        for product in search_results:
            price_str = f"R$ {float(product['price']):.2f}".replace('.', ',')
            print(f"   - {product['name']} - {price_str}")
        
        # =====================================================
        # 3. DEMONSTRAÇÃO DE CARRINHO
        # =====================================================
        
        print_separator("3. CARRINHO DE COMPRAS")
        
        print_subsection("Adicionando produtos ao carrinho")
        
        # Obter alguns produtos para adicionar ao carrinho
        all_products = db.get_products(limit=5)
        
        if len(all_products) >= 3:
            # Adicionar produtos ao carrinho
            cart_additions = [
                (all_products[0]['id'], 2),  # 2 unidades do primeiro produto
                (all_products[1]['id'], 1),  # 1 unidade do segundo produto
                (all_products[2]['id'], 3),  # 3 unidades do terceiro produto
            ]
            
            for product_id, quantity in cart_additions:
                success = db.add_to_cart(main_user_id, product_id, quantity)
                if success:
                    product = db.get_product_by_id(product_id)
                    print(f"✅ Adicionado ao carrinho: {quantity}x {product['name']}")
                else:
                    print(f"❌ Erro ao adicionar produto {product_id} ao carrinho")
        
        print_subsection("Visualizando carrinho")
        
        cart_items = db.get_cart_items(main_user_id)
        if cart_items:
            print(f"🛒 Carrinho tem {len(cart_items)} tipos de produtos:")
            total_cart = 0
            for item in cart_items:
                subtotal = float(item['subtotal'])
                total_cart += subtotal
                price_str = f"R$ {float(item['price']):.2f}".replace('.', ',')
                subtotal_str = f"R$ {subtotal:.2f}".replace('.', ',')
                print(f"   - {item['quantity']}x {item['name']} - {price_str} cada = {subtotal_str}")
            
            total_str = f"R$ {total_cart:.2f}".replace('.', ',')
            print(f"\n💰 Total do carrinho: {total_str}")
        else:
            print("🛒 Carrinho vazio")
        
        print_subsection("Atualizando quantidade no carrinho")
        
        if cart_items:
            # Atualizar quantidade do primeiro item
            first_item = cart_items[0]
            new_quantity = first_item['quantity'] + 1
            
            success = db.update_cart_item(main_user_id, first_item['product_id'], new_quantity)
            if success:
                print(f"✅ Quantidade atualizada: {first_item['name']} agora tem {new_quantity} unidades")
            else:
                print("❌ Erro ao atualizar quantidade")
        
        # =====================================================
        # 4. DEMONSTRAÇÃO DE FAVORITOS
        # =====================================================
        
        print_separator("4. LISTA DE FAVORITOS")
        
        print_subsection("Adicionando produtos aos favoritos")
        
        if len(all_products) >= 2:
            # Adicionar alguns produtos aos favoritos
            favorite_products = all_products[:2]
            
            for product in favorite_products:
                success = db.add_to_favorites(main_user_id, product['id'])
                if success:
                    print(f"❤️ Adicionado aos favoritos: {product['name']}")
                else:
                    print(f"❌ Erro ao adicionar {product['name']} aos favoritos")
        
        print_subsection("Visualizando favoritos")
        
        favorites = db.get_user_favorites(main_user_id)
        if favorites:
            print(f"❤️ {len(favorites)} produtos nos favoritos:")
            for fav in favorites:
                price_str = f"R$ {float(fav['price']):.2f}".replace('.', ',')
                rating_str = f"⭐ {float(fav['rating']):.1f}" if fav['rating'] else "Sem avaliação"
                print(f"   - {fav['name']} - {price_str} - {rating_str}")
        else:
            print("❤️ Nenhum produto nos favoritos")
        
        # =====================================================
        # 5. DEMONSTRAÇÃO DE ENDEREÇOS
        # =====================================================
        
        print_separator("5. ENDEREÇOS DO USUÁRIO")
        
        print_subsection("Adicionando endereços")
        
        # Adicionar endereços de exemplo
        addresses_data = [
            {
                'name': 'Casa',
                'street': 'Rua das Flores',
                'number': '123',
                'complement': 'Apto 45',
                'neighborhood': 'Jardim Primavera',
                'city': 'São Paulo',
                'state': 'SP',
                'zip_code': '01234-567',
                'is_default': True
            },
            {
                'name': 'Trabalho',
                'street': 'Av. Paulista',
                'number': '1000',
                'neighborhood': 'Bela Vista',
                'city': 'São Paulo',
                'state': 'SP',
                'zip_code': '01310-100'
            }
        ]
        
        created_addresses = []
        for addr_data in addresses_data:
            addr_id = db.add_user_address(main_user_id, **addr_data)
            if addr_id:
                created_addresses.append(addr_id)
                default_text = " (Padrão)" if addr_data.get('is_default') else ""
                print(f"🏠 Endereço adicionado: {addr_data['name']}{default_text}")
            else:
                print(f"❌ Erro ao adicionar endereço: {addr_data['name']}")
        
        print_subsection("Listando endereços")
        
        addresses = db.get_user_addresses(main_user_id)
        if addresses:
            print(f"🏠 {len(addresses)} endereços cadastrados:")
            for addr in addresses:
                default_text = " (Padrão)" if addr['is_default'] else ""
                print(f"   - {addr['name']}{default_text}")
                print(f"     {addr['street']}, {addr['number']} - {addr['neighborhood']}")
                print(f"     {addr['city']} - {addr['state']}, {addr['zip_code']}")
        
        # =====================================================
        # 6. DEMONSTRAÇÃO DE PEDIDOS
        # =====================================================
        
        print_separator("6. SISTEMA DE PEDIDOS")
        
        print_subsection("Criando pedido a partir do carrinho")
        
        # Obter itens do carrinho atual
        current_cart = db.get_cart_items(main_user_id)
        
        if current_cart and created_addresses:
            # Preparar itens para o pedido
            order_items = []
            for item in current_cart:
                order_items.append({
                    'product_id': item['product_id'],
                    'quantity': item['quantity'],
                    'price': float(item['price'])
                })
            
            # Criar pedido
            order_id = db.create_order(
                user_id=main_user_id,
                items=order_items,
                shipping_address_id=created_addresses[0],  # Usar primeiro endereço
                payment_method='credit_card'
            )
            
            if order_id:
                print(f"✅ Pedido criado com sucesso! ID: {order_id}")
                
                # Obter detalhes do pedido
                order = db.get_order_by_id(order_id, main_user_id)
                if order:
                    total_str = f"R$ {float(order['total_amount']):.2f}".replace('.', ',')
                    print(f"   💰 Total: {total_str}")
                    print(f"   💳 Pagamento: {order['payment_method']}")
                    print(f"   📦 Status: {order['status']}")
                    print(f"   📅 Data: {order['created_at']}")
                
                # Listar itens do pedido
                order_items_details = db.get_order_items(order_id)
                if order_items_details:
                    print(f"\n📦 Itens do pedido:")
                    for item in order_items_details:
                        unit_price_str = f"R$ {float(item['unit_price']):.2f}".replace('.', ',')
                        total_price_str = f"R$ {float(item['total_price']):.2f}".replace('.', ',')
                        print(f"   - {item['quantity']}x {item['name']} - {unit_price_str} cada = {total_price_str}")
            else:
                print("❌ Erro ao criar pedido")
        else:
            print("⚠️ Carrinho vazio ou sem endereços cadastrados")
        
        print_subsection("Atualizando status do pedido")
        
        if 'order_id' in locals():
            # Simular processamento do pedido
            statuses = ['processing', 'shipped', 'delivered']
            
            for status in statuses:
                success = db.update_order_status(order_id, status)
                if success:
                    print(f"✅ Status atualizado para: {status}")
                else:
                    print(f"❌ Erro ao atualizar status para: {status}")
        
        print_subsection("Listando pedidos do usuário")
        
        user_orders = db.get_user_orders(main_user_id, limit=5)
        if user_orders:
            print(f"📋 {len(user_orders)} pedidos encontrados:")
            for order in user_orders:
                total_str = f"R$ {float(order['total_amount']):.2f}".replace('.', ',')
                print(f"   - Pedido #{order['id']} - {total_str} - {order['status']} - {order['item_count']} itens")
        else:
            print("📋 Nenhum pedido encontrado")
        
        # =====================================================
        # 7. DEMONSTRAÇÃO DE AVALIAÇÕES
        # =====================================================
        
        print_separator("7. SISTEMA DE AVALIAÇÕES")
        
        print_subsection("Adicionando avaliações")
        
        if len(all_products) >= 2:
            # Adicionar algumas avaliações
            reviews_data = [
                {
                    'product_id': all_products[0]['id'],
                    'rating': 5,
                    'title': 'Produto excelente!',
                    'comment': 'Superou minhas expectativas. Recomendo!'
                },
                {
                    'product_id': all_products[1]['id'],
                    'rating': 4,
                    'title': 'Muito bom',
                    'comment': 'Produto de boa qualidade, entrega rápida.'
                }
            ]
            
            for review_data in reviews_data:
                review_id = db.add_product_review(
                    user_id=main_user_id,
                    **review_data
                )
                
                if review_id:
                    product = db.get_product_by_id(review_data['product_id'])
                    print(f"⭐ Avaliação adicionada: {product['name']} - {review_data['rating']} estrelas")
                else:
                    print(f"❌ Erro ao adicionar avaliação")
        
        print_subsection("Visualizando avaliações")
        
        if len(all_products) >= 1:
            product_reviews = db.get_product_reviews(all_products[0]['id'], limit=5)
            if product_reviews:
                product_name = all_products[0]['name']
                print(f"⭐ Avaliações do produto '{product_name}':")
                for review in product_reviews:
                    stars = "⭐" * review['rating']
                    print(f"   {stars} ({review['rating']}/5) - {review['user_name']}")
                    if review['title']:
                        print(f"   \"{review['title']}\"")
                    if review['comment']:
                        print(f"   {review['comment']}")
                    print()
            else:
                print("⭐ Nenhuma avaliação encontrada")
        
        # =====================================================
        # 8. DEMONSTRAÇÃO DE RELATÓRIOS
        # =====================================================
        
        print_separator("8. RELATÓRIOS E ESTATÍSTICAS")
        
        print_subsection("Estatísticas de vendas")
        
        sales_stats = db.get_sales_statistics()
        if sales_stats and sales_stats.get('total_orders', 0) > 0:
            print("📊 Estatísticas de vendas:")
            print(f"   📦 Total de pedidos: {sales_stats['total_orders']}")
            
            if sales_stats['total_revenue']:
                revenue_str = f"R$ {float(sales_stats['total_revenue']):.2f}".replace('.', ',')
                print(f"   💰 Receita total: {revenue_str}")
            
            if sales_stats['average_order_value']:
                avg_str = f"R$ {float(sales_stats['average_order_value']):.2f}".replace('.', ',')
                print(f"   📈 Ticket médio: {avg_str}")
        else:
            print("📊 Nenhuma venda registrada ainda")
        
        print_subsection("Produtos mais vendidos")
        
        top_products = db.get_top_products(limit=5)
        if top_products:
            print("🏆 Top 5 produtos mais vendidos:")
            for i, product in enumerate(top_products, 1):
                print(f"   {i}. {product['name']} - {product['total_sold']} vendidos")
        else:
            print("🏆 Nenhum produto vendido ainda")
        
        print_subsection("Estatísticas de usuários")
        
        user_stats = db.get_user_statistics()
        if user_stats:
            print("👥 Estatísticas de usuários:")
            print(f"   👤 Total de usuários: {user_stats['total_users']}")
            print(f"   🆕 Novos usuários (30 dias): {user_stats['new_users_30_days']}")
            print(f"   ✅ Usuários ativos: {user_stats['active_users']}")
        
        # =====================================================
        # 9. DEMONSTRAÇÃO DE CONFIGURAÇÕES
        # =====================================================
        
        print_separator("9. CONFIGURAÇÕES DO SISTEMA")
        
        print_subsection("Configurações atuais")
        
        settings = db.get_system_settings()
        if settings:
            print("⚙️ Configurações do sistema:")
            for key, value in settings.items():
                print(f"   {key}: {value}")
        
        print_subsection("Atualizando configuração")
        
        # Atualizar uma configuração
        success = db.update_system_setting('site_description', 'E-commerce BOSS SHOPP - Demonstração completa!')
        if success:
            print("✅ Configuração atualizada com sucesso")
        else:
            print("❌ Erro ao atualizar configuração")
        
        # =====================================================
        # RESUMO FINAL
        # =====================================================
        
        print_separator("RESUMO DA DEMONSTRAÇÃO")
        
        print("✅ Demonstração concluída com sucesso!")
        print("\nFuncionalidades testadas:")
        print("   👥 Criação e autenticação de usuários")
        print("   📦 Catálogo de produtos e categorias")
        print("   🛒 Carrinho de compras")
        print("   ❤️ Lista de favoritos")
        print("   🏠 Endereços do usuário")
        print("   📋 Sistema de pedidos")
        print("   ⭐ Avaliações de produtos")
        print("   📊 Relatórios e estatísticas")
        print("   ⚙️ Configurações do sistema")
        
        print(f"\nDados criados na demonstração:")
        print(f"   👤 {len(created_users)} usuários")
        print(f"   🏠 {len(created_addresses)} endereços")
        if 'order_id' in locals():
            print(f"   📋 1 pedido completo")
        
        print("\n🎉 O sistema BOSS SHOPP está funcionando perfeitamente!")
        
    except Exception as e:
        print(f"\n❌ Erro durante a demonstração: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Fechar conexão
        db.disconnect()
        print("\n🔌 Conexão com o banco de dados fechada")

if __name__ == "__main__":
    main()