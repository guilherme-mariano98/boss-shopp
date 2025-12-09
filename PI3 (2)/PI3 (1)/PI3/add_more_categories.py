#!/usr/bin/env python3
"""
Script para adicionar mais categorias ao banco de dados BOSS SHOPP
"""

import sqlite3

def add_categories():
    """Adiciona mais categorias ao banco de dados"""
    
    db_file = "bossshopp_complete.db"
    
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        print(f"Conectado ao banco de dados: {db_file}")
        
        # Adicionar novas categorias
        new_categories = [
            ('Beleza', 'beleza', 'Produtos de beleza e cuidados pessoais', 7),
            ('Livros', 'livros', 'Livros, revistas e e-books', 8),
            ('Automotivo', 'automotivo', 'Acessórios e peças para veículos', 9),
            ('Pet Shop', 'pet-shop', 'Produtos para animais de estimação', 10),
            ('Alimentos', 'alimentos', 'Alimentos e bebidas', 11),
            ('Ferramentas', 'ferramentas', 'Ferramentas e equipamentos', 12),
            ('Música', 'musica', 'Instrumentos musicais e acessórios', 13),
            ('Saúde', 'saude', 'Produtos de saúde e bem-estar', 14),
            ('Brinquedos', 'brinquedos', 'Brinquedos e jogos infantis', 15),
            ('Papelaria', 'papelaria', 'Material escolar e de escritório', 16)
        ]
        
        for name, slug, description, sort_order in new_categories:
            cursor.execute("""
                INSERT OR IGNORE INTO categories (name, slug, description, sort_order) 
                VALUES (?, ?, ?, ?)
            """, (name, slug, description, sort_order))
        
        # Adicionar produtos para as novas categorias
        new_products = [
            # Beleza (categoria 7)
            ('Perfume Importado', 'Perfume masculino 100ml', 189.90, 249.90, 7, 45, 'BEL-PER-001', 4.6, 178),
            ('Kit Maquiagem', 'Kit completo com 12 itens', 159.90, None, 7, 30, 'BEL-MAQ-001', 4.5, 234),
            ('Shampoo Premium', 'Shampoo hidratante 500ml', 45.90, 59.90, 7, 80, 'BEL-SHA-001', 4.3, 156),
            
            # Livros (categoria 8)
            ('Romance Bestseller', 'Livro de romance mais vendido', 39.90, None, 8, 100, 'LIV-ROM-001', 4.8, 567),
            ('Livro de Autoajuda', 'Desenvolvimento pessoal', 44.90, 54.90, 8, 75, 'LIV-AUT-001', 4.7, 423),
            ('Mangá Volume 1', 'Série completa de mangá', 29.90, None, 8, 120, 'LIV-MAN-001', 4.9, 789),
            
            # Automotivo (categoria 9)
            ('Capa de Banco', 'Capa universal para banco de carro', 89.90, 119.90, 9, 40, 'AUT-CAP-001', 4.2, 89),
            ('Kit Limpeza Automotiva', 'Kit completo para limpeza', 79.90, None, 9, 55, 'AUT-LIM-001', 4.4, 134),
            ('Suporte Celular Veicular', 'Suporte magnético universal', 34.90, 49.90, 9, 90, 'AUT-SUP-001', 4.5, 267),
            
            # Pet Shop (categoria 10)
            ('Ração Premium Cães', 'Ração para cães adultos 15kg', 189.90, 229.90, 10, 35, 'PET-RAC-001', 4.7, 345),
            ('Brinquedo para Gatos', 'Kit com 5 brinquedos', 39.90, None, 10, 70, 'PET-BRI-001', 4.6, 234),
            ('Casinha para Cachorro', 'Casinha de plástico resistente', 249.90, 299.90, 10, 20, 'PET-CAS-001', 4.5, 156),
            
            # Alimentos (categoria 11)
            ('Café Gourmet', 'Café especial 500g', 34.90, None, 11, 100, 'ALI-CAF-001', 4.8, 456),
            ('Chocolate Premium', 'Chocolate belga 200g', 24.90, 29.90, 11, 150, 'ALI-CHO-001', 4.7, 678),
            ('Azeite Extra Virgem', 'Azeite português 500ml', 49.90, None, 11, 80, 'ALI-AZE-001', 4.6, 234),
            
            # Ferramentas (categoria 12)
            ('Furadeira Elétrica', 'Furadeira de impacto 650W', 299.90, 399.90, 12, 25, 'FER-FUR-001', 4.7, 189),
            ('Kit Chaves', 'Kit com 40 peças', 89.90, None, 12, 45, 'FER-CHA-001', 4.5, 234),
            ('Trena Digital', 'Trena a laser 40m', 159.90, 199.90, 12, 30, 'FER-TRE-001', 4.6, 156),
            
            # Música (categoria 13)
            ('Violão Acústico', 'Violão para iniciantes', 349.90, 449.90, 13, 20, 'MUS-VIO-001', 4.6, 234),
            ('Teclado Musical', 'Teclado 61 teclas', 599.90, None, 13, 15, 'MUS-TEC-001', 4.7, 178),
            ('Fone de Ouvido Studio', 'Fone profissional para estúdio', 449.90, 599.90, 13, 25, 'MUS-FON-001', 4.8, 345),
            
            # Saúde (categoria 14)
            ('Termômetro Digital', 'Termômetro infravermelho', 89.90, 119.90, 14, 60, 'SAU-TER-001', 4.5, 267),
            ('Medidor de Pressão', 'Medidor digital de pressão', 149.90, None, 14, 40, 'SAU-MED-001', 4.6, 189),
            ('Vitamina C', 'Suplemento vitamina C 60 cápsulas', 39.90, 49.90, 14, 100, 'SAU-VIT-001', 4.4, 456),
            
            # Brinquedos (categoria 15)
            ('Boneca Articulada', 'Boneca com acessórios', 79.90, 99.90, 15, 50, 'BRI-BON-001', 4.7, 345),
            ('Lego Criativo', 'Kit Lego 500 peças', 149.90, None, 15, 35, 'BRI-LEG-001', 4.8, 567),
            ('Quebra-Cabeça 1000 peças', 'Quebra-cabeça paisagem', 59.90, 79.90, 15, 60, 'BRI-QUE-001', 4.5, 234),
            
            # Papelaria (categoria 16)
            ('Caderno Universitário', 'Caderno 10 matérias', 29.90, None, 16, 120, 'PAP-CAD-001', 4.3, 456),
            ('Kit Canetas Coloridas', 'Kit com 24 cores', 34.90, 44.90, 16, 90, 'PAP-CAN-001', 4.5, 345),
            ('Mochila Escolar', 'Mochila resistente com 3 compartimentos', 89.90, 119.90, 16, 55, 'PAP-MOC-001', 4.6, 234)
        ]
        
        for name, description, price, old_price, category_id, stock, sku, rating, reviews in new_products:
            cursor.execute("""
                INSERT OR IGNORE INTO products 
                (name, description, price, old_price, category_id, stock_quantity, sku, rating, review_count) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, description, price, old_price, category_id, stock, sku, rating, reviews))
        
        conn.commit()
        
        # Contar categorias e produtos
        cursor.execute("SELECT COUNT(*) FROM categories")
        total_categories = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM products")
        total_products = cursor.fetchone()[0]
        
        print("\n" + "="*50)
        print("CATEGORIAS ADICIONADAS COM SUCESSO!")
        print("="*50)
        print(f"Total de categorias: {total_categories}")
        print(f"Total de produtos: {total_products}")
        print("="*50)
        
    except sqlite3.Error as e:
        print(f"Erro: {e}")
        if conn:
            conn.rollback()
    
    finally:
        if conn:
            conn.close()
            print("Conexão fechada")

if __name__ == "__main__":
    add_categories()
