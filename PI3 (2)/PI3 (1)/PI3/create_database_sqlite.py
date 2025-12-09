#!/usr/bin/env python3
"""
BOSS SHOPP Database Creation Script for SQLite
Creates the complete SQLite database for the e-commerce system
"""

import sqlite3
import os

def create_database():
    """Create the BOSS SHOPP SQLite database with all tables"""
    
    # Database file
    db_file = "bossshopp_complete.db"
    
    # Initialize connection variable
    conn = None
    
    try:
        # Connect to SQLite database (will create if it doesn't exist)
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        print(f"Successfully connected to SQLite database: {db_file}")
        
        # Create tables
        print("Creating tables...")
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                phone TEXT,
                address TEXT,
                city TEXT,
                state TEXT,
                zip_code TEXT,
                country TEXT DEFAULT 'Brasil',
                date_of_birth DATE,
                is_active BOOLEAN DEFAULT 1,
                is_admin BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create trigger for updated_at
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS update_users_updated_at 
            AFTER UPDATE ON users
            BEGIN
                UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END
        """)
        
        # Categories table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                slug TEXT NOT NULL UNIQUE,
                description TEXT,
                image_url TEXT,
                is_active BOOLEAN DEFAULT 1,
                sort_order INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create trigger for updated_at
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS update_categories_updated_at 
            AFTER UPDATE ON categories
            BEGIN
                UPDATE categories SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END
        """)
        
        # Products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                old_price REAL,
                category_id INTEGER NOT NULL,
                image_url TEXT,
                stock_quantity INTEGER DEFAULT 0,
                sku TEXT UNIQUE,
                weight REAL,
                dimensions TEXT,
                is_active BOOLEAN DEFAULT 1,
                is_featured BOOLEAN DEFAULT 0,
                rating REAL DEFAULT 0.0,
                review_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
            )
        """)
        
        # Create trigger for updated_at
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS update_products_updated_at 
            AFTER UPDATE ON products
            BEGIN
                UPDATE products SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END
        """)
        
        # Product images table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                image_url TEXT NOT NULL,
                alt_text TEXT,
                is_primary BOOLEAN DEFAULT 0,
                sort_order INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
            )
        """)
        
        # User addresses table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_addresses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                street TEXT NOT NULL,
                number TEXT NOT NULL,
                complement TEXT,
                neighborhood TEXT NOT NULL,
                city TEXT NOT NULL,
                state TEXT NOT NULL,
                zip_code TEXT NOT NULL,
                country TEXT DEFAULT 'Brasil',
                is_default BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        """)
        
        # Create trigger for updated_at
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS update_user_addresses_updated_at 
            AFTER UPDATE ON user_addresses
            BEGIN
                UPDATE user_addresses SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END
        """)
        
        # Orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_number TEXT UNIQUE NOT NULL,
                user_id INTEGER NOT NULL,
                total_amount REAL NOT NULL,
                shipping_amount REAL DEFAULT 0.0,
                tax_amount REAL DEFAULT 0.0,
                discount_amount REAL DEFAULT 0.0,
                status TEXT DEFAULT 'pending',
                payment_status TEXT DEFAULT 'pending',
                payment_method TEXT,
                shipping_address_id INTEGER,
                billing_address_id INTEGER,
                notes TEXT,
                shipped_at TIMESTAMP,
                delivered_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                FOREIGN KEY (shipping_address_id) REFERENCES user_addresses (id),
                FOREIGN KEY (billing_address_id) REFERENCES user_addresses (id)
            )
        """)
        
        # Create trigger for updated_at
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS update_orders_updated_at 
            AFTER UPDATE ON orders
            BEGIN
                UPDATE orders SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END
        """)
        
        # Order items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                total_price REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (order_id) REFERENCES orders (id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
            )
        """)
        
        # Cart items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cart_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, product_id),
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
            )
        """)
        
        # Create trigger for updated_at
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS update_cart_items_updated_at 
            AFTER UPDATE ON cart_items
            BEGIN
                UPDATE cart_items SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END
        """)
        
        # Favorites table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, product_id),
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
            )
        """)
        
        # Product reviews table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
                title TEXT,
                comment TEXT,
                is_verified_purchase BOOLEAN DEFAULT 0,
                is_approved BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, product_id),
                FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        """)
        
        # Create trigger for updated_at
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS update_product_reviews_updated_at 
            AFTER UPDATE ON product_reviews
            BEGIN
                UPDATE product_reviews SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END
        """)
        
        # Coupons table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS coupons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                discount_type TEXT NOT NULL,
                discount_value REAL NOT NULL,
                minimum_amount REAL DEFAULT 0.0,
                maximum_discount REAL,
                usage_limit INTEGER,
                used_count INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT 1,
                starts_at TIMESTAMP,
                expires_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create trigger for updated_at
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS update_coupons_updated_at 
            AFTER UPDATE ON coupons
            BEGIN
                UPDATE coupons SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END
        """)
        
        # Coupon usage table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS coupon_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                coupon_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                order_id INTEGER NOT NULL,
                discount_amount REAL NOT NULL,
                used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (coupon_id) REFERENCES coupons (id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
                FOREIGN KEY (order_id) REFERENCES orders (id) ON DELETE CASCADE
            )
        """)
        
        # Payment methods table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payment_methods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                card_last_four TEXT,
                card_brand TEXT,
                card_holder_name TEXT,
                is_default BOOLEAN DEFAULT 0,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        """)
        
        # Create trigger for updated_at
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS update_payment_methods_updated_at 
            AFTER UPDATE ON payment_methods
            BEGIN
                UPDATE payment_methods SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END
        """)
        
        # Payment transactions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payment_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                transaction_id TEXT UNIQUE,
                payment_method_id INTEGER,
                amount REAL NOT NULL,
                status TEXT DEFAULT 'pending',
                gateway TEXT,
                gateway_response TEXT,
                processed_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (order_id) REFERENCES orders (id) ON DELETE CASCADE,
                FOREIGN KEY (payment_method_id) REFERENCES payment_methods (id)
            )
        """)
        
        # Create trigger for updated_at
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS update_payment_transactions_updated_at 
            AFTER UPDATE ON payment_transactions
            BEGIN
                UPDATE payment_transactions SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END
        """)
        
        # Stock movements table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                movement_type TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                reference_type TEXT NOT NULL,
                reference_id INTEGER,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
            )
        """)
        
        # Notifications table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                is_read BOOLEAN DEFAULT 0,
                action_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                read_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        """)
        
        # System settings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                setting_key TEXT UNIQUE NOT NULL,
                setting_value TEXT,
                description TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create trigger for updated_at
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS update_system_settings_updated_at 
            AFTER UPDATE ON system_settings
            BEGIN
                UPDATE system_settings SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END
        """)
        
        print("All tables created successfully!")
        
        # Insert initial data
        print("Inserting initial data...")
        
        # Insert categories
        cursor.execute("""
            INSERT OR IGNORE INTO categories (name, slug, description, sort_order) VALUES
            ('Moda', 'moda', 'Roupas e acessórios de moda', 1),
            ('Eletrônicos', 'eletronicos', 'Dispositivos eletrônicos e gadgets', 2),
            ('Casa', 'casa', 'Produtos para o lar', 3),
            ('Games', 'games', 'Jogos e acessórios para gamers', 4),
            ('Esportes', 'esportes', 'Equipamentos esportivos', 5),
            ('Infantil', 'infantil', 'Produtos para bebês e crianças', 6)
        """)
        
        # Insert products
        cursor.execute("""
            INSERT OR IGNORE INTO products (name, description, price, old_price, category_id, stock_quantity, sku, rating, review_count) VALUES
            -- Moda
            ('Camiseta Básica', 'Camiseta de algodão 100% confortável e durável', 39.90, 49.90, 1, 100, 'MOD-CAM-001', 4.5, 234),
            ('Calça Jeans', 'Calça jeans masculina com corte moderno', 89.90, NULL, 1, 50, 'MOD-CAL-001', 4.2, 87),
            ('Tênis Esportivo', 'Tênis para corrida com tecnologia de amortecimento', 169.90, 199.90, 1, 30, 'MOD-TEN-001', 4.8, 156),
            ('Boné Estiloso', 'Boné com proteção UV e design moderno', 34.90, NULL, 1, 75, 'MOD-BON-001', 4.0, 45),

            -- Eletrônicos
            ('Smartphone Premium', 'Smartphone com câmera de 108MP e 5G', 1760.00, 2200.00, 2, 25, 'ELE-SMT-001', 4.7, 189),
            ('Notebook Ultrafino', 'Notebook com processador i7 e SSD 512GB', 2975.00, NULL, 2, 15, 'ELE-NOT-001', 4.6, 92),
            ('Fone Bluetooth Sem Fio', 'Fone com cancelamento de ruído ativo', 224.90, 299.90, 2, 60, 'ELE-FON-001', 4.4, 267),
            ('Smart TV 55"', 'TV 4K com HDR e sistema Android', 1750.00, 2100.00, 2, 20, 'ELE-TV-001', 4.5, 134),

            -- Casa
            ('Sofá Confortável', 'Sofá de 3 lugares com estrutura de madeira', 1020.00, 1200.00, 3, 10, 'CAS-SOF-001', 4.3, 78),
            ('Cama Queen Size', 'Cama com headboard estofado', 899.90, NULL, 3, 8, 'CAS-CAM-001', 4.6, 56),
            ('Jogo de Talheres', 'Talheres em aço inoxidável 24 peças', 159.90, 199.90, 3, 40, 'CAS-TAL-001', 4.2, 89),
            ('Kit de Lâmpadas LED', 'Lâmpadas LED econômicas 9W - Kit 4 unidades', 97.40, NULL, 3, 80, 'CAS-LED-001', 4.1, 123),

            -- Games
            ('Console de Videogame', 'Console de última geração com 1TB', 2250.00, NULL, 4, 12, 'GAM-CON-001', 4.9, 345),
            ('Jogo de Tabuleiro', 'Jogo estratégico para toda família', 89.90, NULL, 4, 35, 'GAM-TAB-001', 4.3, 67),
            ('Fone Gamer', 'Fone com som surround 7.1 e microfone', 299.90, 399.90, 4, 25, 'GAM-FON-001', 4.5, 178),
            ('Teclado Mecânico', 'Teclado RGB com switches blue', 319.90, NULL, 4, 18, 'GAM-TEC-001', 4.7, 234),

            -- Esportes
            ('Conjunto de Halteres', 'Halteres ajustáveis de 5 a 25kg', 254.90, NULL, 5, 22, 'ESP-HAL-001', 4.4, 89),
            ('Tênis para Corrida', 'Tênis com amortecimento especial', 199.90, 249.90, 5, 45, 'ESP-TEN-001', 4.6, 156),
            ('Bola de Futebol', 'Bola oficial com certificação FIFA', 74.90, NULL, 5, 60, 'ESP-BOL-001', 4.2, 234),
            ('Bicicleta Mountain Bike', 'Bicicleta para trilhas com 21 marchas', 1299.90, 1599.90, 5, 8, 'ESP-BIC-001', 4.8, 67),

            -- Infantil
            ('Camiseta Infantil', 'Camiseta 100% algodão tamanhos 2 a 12 anos', 33.90, NULL, 6, 90, 'INF-CAM-001', 4.3, 145),
            ('Meias Coloridas', 'Pacote com 5 pares de meias divertidas', 19.90, NULL, 6, 120, 'INF-MEI-001', 4.1, 89),
            ('Sapatilha Infantil', 'Sapatilha para festas e ocasiões especiais', 47.90, NULL, 6, 55, 'INF-SAP-001', 4.4, 67),
            ('Carrinho de Controle Remoto', 'Carrinho com controle remoto e luzes', 89.90, 119.90, 6, 30, 'INF-CAR-001', 4.6, 123)
        """)
        
        # Insert admin user
        cursor.execute("""
            INSERT OR IGNORE INTO users (name, email, password, is_admin, city, state, country) VALUES
            ('Administrador', 'admin@bossshopp.com', '$2b$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 1, 'São Paulo', 'SP', 'Brasil')
        """)
        
        # Insert system settings
        cursor.execute("""
            INSERT OR IGNORE INTO system_settings (setting_key, setting_value, description) VALUES
            ('site_name', 'BOSS SHOPP', 'Nome do site'),
            ('site_description', 'Sua loja online de confiança', 'Descrição do site'),
            ('currency', 'BRL', 'Moeda padrão'),
            ('tax_rate', '0.00', 'Taxa de imposto padrão'),
            ('free_shipping_minimum', '200.00', 'Valor mínimo para frete grátis'),
            ('max_cart_items', '50', 'Máximo de itens no carrinho'),
            ('order_number_prefix', 'BS', 'Prefixo do número do pedido'),
            ('email_notifications', 'true', 'Ativar notificações por email'),
            ('sms_notifications', 'false', 'Ativar notificações por SMS'),
            ('maintenance_mode', 'false', 'Modo de manutenção')
        """)
        
        conn.commit()
        print("Initial data inserted successfully!")
        
        print("\n" + "="*50)
        print("DATABASE SETUP COMPLETED SUCCESSFULLY!")
        print("="*50)
        print(f"Database file: {db_file}")
        print("Tables created: 17")
        print("Initial categories: 6")
        print("Initial products: 24")
        print("Admin user: admin@bossshopp.com / password")
        print("="*50)
        
    except sqlite3.Error as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()
    
    finally:
        if conn:
            conn.close()
            print("SQLite connection closed")

if __name__ == "__main__":
    create_database()