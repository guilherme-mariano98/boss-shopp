#!/usr/bin/env python3
"""
Script para gerar páginas HTML para todas as categorias
"""

import sqlite3

# Definir ícones para cada categoria
CATEGORY_ICONS = {
    'moda': 'fa-tshirt',
    'eletronicos': 'fa-laptop',
    'casa': 'fa-home',
    'games': 'fa-gamepad',
    'esportes': 'fa-dumbbell',
    'infantil': 'fa-baby',
    'beleza': 'fa-spa',
    'livros': 'fa-book',
    'automotivo': 'fa-car',
    'pet-shop': 'fa-paw',
    'alimentos': 'fa-utensils',
    'ferramentas': 'fa-tools',
    'musica': 'fa-music',
    'saude': 'fa-heartbeat',
    'brinquedos': 'fa-puzzle-piece',
    'papelaria': 'fa-pen'
}

# Ícones para produtos por categoria
PRODUCT_ICONS = {
    'moda': ['fa-tshirt', 'fa-jeans', 'fa-shoe-prints', 'fa-hat-cowboy'],
    'eletronicos': ['fa-mobile-alt', 'fa-laptop', 'fa-headphones', 'fa-tv'],
    'casa': ['fa-couch', 'fa-bed', 'fa-utensils', 'fa-lightbulb'],
    'games': ['fa-gamepad', 'fa-dice', 'fa-headset', 'fa-keyboard'],
    'esportes': ['fa-dumbbell', 'fa-running', 'fa-futbol', 'fa-bicycle'],
    'infantil': ['fa-tshirt', 'fa-socks', 'fa-shoe-prints', 'fa-car'],
    'beleza': ['fa-spray-can', 'fa-palette', 'fa-pump-soap'],
    'livros': ['fa-book', 'fa-book-open', 'fa-book-reader'],
    'automotivo': ['fa-car-side', 'fa-tools', 'fa-mobile-alt'],
    'pet-shop': ['fa-bone', 'fa-cat', 'fa-home'],
    'alimentos': ['fa-coffee', 'fa-candy-cane', 'fa-wine-bottle'],
    'ferramentas': ['fa-screwdriver', 'fa-wrench', 'fa-ruler'],
    'musica': ['fa-guitar', 'fa-piano', 'fa-headphones-alt'],
    'saude': ['fa-thermometer', 'fa-heartbeat', 'fa-pills'],
    'brinquedos': ['fa-puzzle-piece', 'fa-cubes', 'fa-puzzle-piece'],
    'papelaria': ['fa-book', 'fa-pen', 'fa-backpack']
}

def generate_category_page(category_name, category_slug, category_description, products, icon):
    """Gera uma página HTML para uma categoria"""
    
    # Gerar cards de produtos
    products_html = ""
    product_icons = PRODUCT_ICONS.get(category_slug, ['fa-box'])
    
    for idx, product in enumerate(products):
        icon_class = product_icons[idx % len(product_icons)]
        old_price_html = f'<span class="product-old-price">R$ {product[3]:.2f}</span>' if product[3] else ''
        
        stars = '★' * int(product[6]) + '☆' * (5 - int(product[6]))
        
        products_html += f'''
                <!-- Produto {idx + 1} -->
                <div class="product-card">
                    <div class="product-image">
                        <i class="fas {icon_class}"></i>
                    </div>
                    <div class="product-info">
                        <h3 class="product-name">{product[0]}</h3>
                        <p class="product-description">{product[1]}</p>
                        <div class="product-rating">
                            <span class="stars">{stars}</span>
                            <span class="rating-count">({product[7]})</span>
                        </div>
                        <div class="product-price">
                            R$ {product[2]:.2f}
                            {old_price_html}
                        </div>
                        <button class="add-to-cart-btn">
                            <i class="fas fa-shopping-cart"></i> Adicionar ao Carrinho
                        </button>
                    </div>
                </div>
'''
    
    html_content = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{category_name} - BOSS SHOPP</title>
    <link rel="stylesheet" href="optimized-styles.css">
    <link rel="stylesheet" href="panel-buttons.css">
    <link rel="stylesheet" href="pages.css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Montserrat', sans-serif;
            background: #f8f9fa;
        }}
        
        .category-header {{
            background: linear-gradient(135deg, #ff6b35 0%, #ff8c42 50%, #ffa45c 100%);
            padding: 80px 0;
            color: white;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        
        .category-header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 20% 50%, rgba(255,255,255,0.2) 0%, transparent 50%),
                        radial-gradient(circle at 80% 50%, rgba(255,255,255,0.15) 0%, transparent 50%);
            animation: pulse 8s ease-in-out infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 0.5; }}
            50% {{ opacity: 1; }}
        }}
        
        .category-header h1 {{
            font-size: 3rem;
            margin-bottom: 15px;
            font-weight: 900;
            text-shadow: 0 4px 10px rgba(0,0,0,0.2);
            position: relative;
            z-index: 1;
            animation: slideDown 0.8s ease-out;
        }}
        
        @keyframes slideDown {{
            from {{
                opacity: 0;
                transform: translateY(-30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .category-header h1 i {{
            margin-right: 15px;
            animation: bounce 2s ease-in-out infinite;
        }}
        
        @keyframes bounce {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-10px); }}
        }}
        
        .category-header p {{
            font-size: 1.3rem;
            opacity: 0.95;
            position: relative;
            z-index: 1;
            animation: slideUp 0.8s ease-out;
        }}
        
        @keyframes slideUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .products-section {{
            padding: 80px 0;
            background: white;
        }}
        
        .products-section h2 {{
            text-align: center;
            font-size: 2.5rem;
            color: #333;
            margin-bottom: 50px;
            font-weight: 800;
            position: relative;
        }}
        
        .products-section h2::after {{
            content: '';
            position: absolute;
            bottom: -15px;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 4px;
            background: linear-gradient(90deg, #ff6b35, #ff8c42, #ffa45c);
            border-radius: 2px;
        }}
        
        .products-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 35px;
            margin-top: 50px;
        }}
        
        .product-card {{
            background: white;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            border: 2px solid rgba(255,107,53,0.1);
            animation: cardAppear 0.6s ease-out backwards;
        }}
        
        @keyframes cardAppear {{
            from {{
                opacity: 0;
                transform: translateY(30px) scale(0.9);
            }}
            to {{
                opacity: 1;
                transform: translateY(0) scale(1);
            }}
        }}
        
        .product-card:nth-child(1) {{ animation-delay: 0.1s; }}
        .product-card:nth-child(2) {{ animation-delay: 0.2s; }}
        .product-card:nth-child(3) {{ animation-delay: 0.3s; }}
        .product-card:nth-child(4) {{ animation-delay: 0.4s; }}
        
        .product-card:hover {{
            transform: translateY(-15px) scale(1.03);
            box-shadow: 0 20px 50px rgba(255,107,53,0.2);
            border-color: #ff6b35;
        }}
        
        .product-image {{
            width: 100%;
            height: 250px;
            background: linear-gradient(135deg, #fff5f0 0%, #ffe8dc 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 4rem;
            color: #ff6b35;
            position: relative;
            overflow: hidden;
        }}
        
        .product-image::before {{
            content: '';
            position: absolute;
            width: 150%;
            height: 150%;
            background: radial-gradient(circle, rgba(255,107,53,0.1) 0%, transparent 70%);
            animation: pulse 3s ease-in-out infinite;
        }}
        
        .product-image i {{
            position: relative;
            z-index: 1;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); opacity: 0.5; }}
            50% {{ transform: scale(1.1); opacity: 0.8; }}
        }}
        
        .product-info {{
            padding: 25px;
        }}
        
        .product-category {{
            display: inline-block;
            background: #fff5f0;
            color: #ff6b35;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 12px;
        }}
        
        .product-name {{
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 12px;
            color: #333;
            line-height: 1.4;
        }}
        
        .product-description {{
            font-size: 0.95rem;
            color: #666;
            margin-bottom: 15px;
            line-height: 1.6;
        }}
        
        .product-price {{
            font-size: 1.5rem;
            font-weight: 700;
            color: #ff6b35;
            margin-bottom: 15px;
        }}
        
        .product-old-price {{
            font-size: 1rem;
            color: #999;
            text-decoration: line-through;
            margin-left: 10px;
        }}
        
        .product-rating {{
            display: flex;
            align-items: center;
            gap: 5px;
            margin-bottom: 15px;
        }}
        
        .stars {{
            color: #ffc107;
        }}
        
        .rating-count {{
            color: #666;
            font-size: 0.9rem;
        }}
        
        .add-to-cart-btn {{
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #ff6b35 0%, #ff8c42 100%);
            color: white;
            border: none;
            border-radius: 30px;
            font-weight: 700;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(255,107,53,0.3);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .add-to-cart-btn:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(255,107,53,0.5);
            background: linear-gradient(135deg, #ff8c42 0%, #ff6b35 100%);
        }}
        
        .add-to-cart-btn i {{
            margin-right: 8px;
        }}
        
        .breadcrumb {{
            padding: 25px 0;
            font-size: 1rem;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        
        .breadcrumb a {{
            color: #ff6b35;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        
        .breadcrumb a:hover {{
            color: #ff8c42;
            text-decoration: none;
        }}
        
        .breadcrumb strong {{
            color: #333;
            font-weight: 700;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
        }}
    </style>
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="container">
            <div class="header-top">
                <div class="header-links">
                    <a href="sobre.html" class="header-link">Sobre</a>
                    <a href="atendimento.html" class="header-link">Atendimento</a>
                    <a href="#" class="header-link">Vendedor</a>
                    <a href="#" class="header-link">Download</a>
                    <a href="#" class="header-link">Conecte-se</a>
                </div>
                <div class="header-social">
                    <a href="#" class="social-link"><i class="fab fa-facebook"></i></a>
                    <a href="#" class="social-link"><i class="fab fa-instagram"></i></a>
                    <a href="#" class="social-link"><i class="fab fa-twitter"></i></a>
                </div>
            </div>
        </div>
    </header>

    <!-- Navigation -->
    <nav class="navbar">
        <div class="container">
            <div class="nav-content">
                <div class="logo">
                    <a href="index.html">
                        <img src="boss-shop-logo.png" alt="BOSS SHOPP" class="logo-image">
                    </a>
                </div>
                
                <div class="search-bar">
                    <input type="text" placeholder="Buscar produtos...">
                    <button><i class="fas fa-search"></i></button>
                </div>
                
                <div class="nav-icons">
                    <a href="#" class="nav-icon"><i class="fas fa-user"></i></a>
                    <a href="#" class="nav-icon"><i class="fas fa-heart"></i></a>
                    <a href="#" class="nav-icon cart-icon">
                        <i class="fas fa-shopping-cart"></i>
                        <span class="cart-count">0</span>
                    </a>
                </div>
            </div>
        </div>
    </nav>

    <!-- Breadcrumb -->
    <div class="container">
        <div class="breadcrumb">
            <a href="index.html">Home</a> / <a href="categorias.html">Categorias</a> / <strong>{category_name}</strong>
        </div>
    </div>

    <!-- Category Header -->
    <section class="category-header">
        <div class="container">
            <h1><i class="fas {icon}"></i> {category_name}</h1>
            <p>{category_description}</p>
        </div>
    </section>

    <!-- Products Section -->
    <section class="products-section">
        <div class="container">
            <h2>Produtos em Destaque</h2>
            <div class="products-grid">
{products_html}
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>BOSS SHOPP</h3>
                    <p>Sua loja online de confiança</p>
                </div>
                <div class="footer-section">
                    <h4>Links Rápidos</h4>
                    <ul>
                        <li><a href="index.html">Home</a></li>
                        <li><a href="categorias.html">Categorias</a></li>
                        <li><a href="sobre.html">Sobre</a></li>
                        <li><a href="atendimento.html">Atendimento</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h4>Contato</h4>
                    <p>Email: contato@bossshopp.com</p>
                    <p>Tel: (11) 1234-5678</p>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 BOSS SHOPP. Todos os direitos reservados.</p>
            </div>
        </div>
    </footer>

    <script src="script.js"></script>
</body>
</html>'''
    
    return html_content

def main():
    """Função principal"""
    db_file = "bossshopp_complete.db"
    
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Buscar todas as categorias
        cursor.execute("SELECT id, name, slug, description FROM categories ORDER BY sort_order")
        categories = cursor.fetchall()
        
        print(f"Gerando páginas para {len(categories)} categorias...")
        
        for category in categories:
            category_id, category_name, category_slug, category_description = category
            
            # Buscar produtos da categoria
            cursor.execute("""
                SELECT name, description, price, old_price, stock_quantity, sku, rating, review_count
                FROM products
                WHERE category_id = ?
                ORDER BY rating DESC
                LIMIT 12
            """, (category_id,))
            
            products = cursor.fetchall()
            
            if products:
                # Gerar página HTML
                icon = CATEGORY_ICONS.get(category_slug, 'fa-box')
                html_content = generate_category_page(
                    category_name, 
                    category_slug, 
                    category_description, 
                    products,
                    icon
                )
                
                # Salvar arquivo
                filename = f"PI3 (2)/PI3 (1)/PI3/PI2/frontend/categoria-{category_slug}.html"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                print(f"✓ Criada: {filename} ({len(products)} produtos)")
            else:
                print(f"✗ Sem produtos para: {category_name}")
        
        print("\n" + "="*50)
        print("PÁGINAS GERADAS COM SUCESSO!")
        print("="*50)
        
    except Exception as e:
        print(f"Erro: {e}")
    
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
