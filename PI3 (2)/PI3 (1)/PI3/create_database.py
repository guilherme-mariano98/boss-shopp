#!/usr/bin/env python3
"""
BOSS SHOPP Database Creation Script
Creates the complete MySQL database for the e-commerce system
"""

import mysql.connector
from mysql.connector import Error
import os
import sys

def create_database():
    """Create the BOSS SHOPP database with all tables"""
    
    # Database configuration
    config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'root'
    }
    
    connection = None
    cursor = None
    
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            cursor = connection.cursor()
            print("Successfully connected to MySQL server")
            
            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS boss_shopp_complete")
            cursor.execute("USE boss_shopp_complete")
            print("Database 'boss_shopp_complete' created/selected")
            
            # Create tables
            print("Creating tables...")
            
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    phone VARCHAR(20),
                    address TEXT,
                    city VARCHAR(100),
                    state VARCHAR(100),
                    zip_code VARCHAR(20),
                    country VARCHAR(100) DEFAULT 'Brasil',
                    date_of_birth DATE,
                    is_active BOOLEAN DEFAULT TRUE,
                    is_admin BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    
                    INDEX idx_email (email),
                    INDEX idx_phone (phone),
                    INDEX idx_created_at (created_at)
                )
            """)
            
            # Categories table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    slug VARCHAR(50) NOT NULL UNIQUE,
                    description TEXT,
                    image_url VARCHAR(500),
                    is_active BOOLEAN DEFAULT TRUE,
                    sort_order INT DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    
                    INDEX idx_slug (slug),
                    INDEX idx_active (is_active),
                    INDEX idx_sort_order (sort_order)
                )
            """)
            
            # Products table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    price DECIMAL(10, 2) NOT NULL,
                    old_price DECIMAL(10, 2) NULL,
                    category_id INT NOT NULL,
                    image_url VARCHAR(500),
                    stock_quantity INT DEFAULT 0,
                    sku VARCHAR(100) UNIQUE,
                    weight DECIMAL(8, 3),
                    dimensions VARCHAR(100),
                    is_active BOOLEAN DEFAULT TRUE,
                    is_featured BOOLEAN DEFAULT FALSE,
                    rating DECIMAL(3, 2) DEFAULT 0.00,
                    review_count INT DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
                    INDEX idx_category (category_id),
                    INDEX idx_price (price),
                    INDEX idx_active (is_active),
                    INDEX idx_featured (is_featured),
                    INDEX idx_rating (rating),
                    INDEX idx_sku (sku)
                )
            """)
            
            # Product images table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS product_images (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    product_id INT NOT NULL,
                    image_url VARCHAR(500) NOT NULL,
                    alt_text VARCHAR(255),
                    is_primary BOOLEAN DEFAULT FALSE,
                    sort_order INT DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
                    INDEX idx_product (product_id),
                    INDEX idx_primary (is_primary)
                )
            """)
            
            # User addresses table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_addresses (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    street VARCHAR(255) NOT NULL,
                    number VARCHAR(20) NOT NULL,
                    complement VARCHAR(100),
                    neighborhood VARCHAR(100) NOT NULL,
                    city VARCHAR(100) NOT NULL,
                    state VARCHAR(50) NOT NULL,
                    zip_code VARCHAR(20) NOT NULL,
                    country VARCHAR(100) DEFAULT 'Brasil',
                    is_default BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    INDEX idx_user (user_id),
                    INDEX idx_default (is_default)
                )
            """)
            
            # Orders table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    order_number VARCHAR(50) UNIQUE NOT NULL,
                    user_id INT NOT NULL,
                    total_amount DECIMAL(10, 2) NOT NULL,
                    shipping_amount DECIMAL(10, 2) DEFAULT 0.00,
                    tax_amount DECIMAL(10, 2) DEFAULT 0.00,
                    discount_amount DECIMAL(10, 2) DEFAULT 0.00,
                    status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled', 'refunded') DEFAULT 'pending',
                    payment_status ENUM('pending', 'paid', 'failed', 'refunded') DEFAULT 'pending',
                    payment_method VARCHAR(50),
                    shipping_address_id INT,
                    billing_address_id INT,
                    notes TEXT,
                    shipped_at TIMESTAMP NULL,
                    delivered_at TIMESTAMP NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (shipping_address_id) REFERENCES user_addresses(id),
                    FOREIGN KEY (billing_address_id) REFERENCES user_addresses(id),
                    INDEX idx_user (user_id),
                    INDEX idx_status (status),
                    INDEX idx_payment_status (payment_status),
                    INDEX idx_order_number (order_number),
                    INDEX idx_created_at (created_at)
                )
            """)
            
            # Order items table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS order_items (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    order_id INT NOT NULL,
                    product_id INT NOT NULL,
                    quantity INT NOT NULL,
                    unit_price DECIMAL(10, 2) NOT NULL,
                    total_price DECIMAL(10, 2) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
                    INDEX idx_order (order_id),
                    INDEX idx_product (product_id)
                )
            """)
            
            # Cart items table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cart_items (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    product_id INT NOT NULL,
                    quantity INT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
                    UNIQUE KEY unique_user_product (user_id, product_id),
                    INDEX idx_user (user_id)
                )
            """)
            
            # Favorites table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS favorites (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    product_id INT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
                    UNIQUE KEY unique_user_product (user_id, product_id),
                    INDEX idx_user (user_id),
                    INDEX idx_product (product_id)
                )
            """)
            
            # Product reviews table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS product_reviews (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    product_id INT NOT NULL,
                    user_id INT NOT NULL,
                    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
                    title VARCHAR(255),
                    comment TEXT,
                    is_verified_purchase BOOLEAN DEFAULT FALSE,
                    is_approved BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    UNIQUE KEY unique_user_product_review (user_id, product_id),
                    INDEX idx_product (product_id),
                    INDEX idx_user (user_id),
                    INDEX idx_rating (rating),
                    INDEX idx_approved (is_approved)
                )
            """)
            
            # Coupons table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS coupons (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    code VARCHAR(50) UNIQUE NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    discount_type ENUM('percentage', 'fixed') NOT NULL,
                    discount_value DECIMAL(10, 2) NOT NULL,
                    minimum_amount DECIMAL(10, 2) DEFAULT 0.00,
                    maximum_discount DECIMAL(10, 2) NULL,
                    usage_limit INT NULL,
                    used_count INT DEFAULT 0,
                    is_active BOOLEAN DEFAULT TRUE,
                    starts_at TIMESTAMP NULL,
                    expires_at TIMESTAMP NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    
                    INDEX idx_code (code),
                    INDEX idx_active (is_active),
                    INDEX idx_expires_at (expires_at)
                )
            """)
            
            # Coupon usage table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS coupon_usage (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    coupon_id INT NOT NULL,
                    user_id INT NOT NULL,
                    order_id INT NOT NULL,
                    discount_amount DECIMAL(10, 2) NOT NULL,
                    used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY (coupon_id) REFERENCES coupons(id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                    INDEX idx_coupon (coupon_id),
                    INDEX idx_user (user_id),
                    INDEX idx_order (order_id)
                )
            """)
            
            # Payment methods table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS payment_methods (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    type ENUM('credit_card', 'debit_card', 'pix', 'boleto') NOT NULL,
                    card_last_four VARCHAR(4),
                    card_brand VARCHAR(50),
                    card_holder_name VARCHAR(255),
                    is_default BOOLEAN DEFAULT FALSE,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    INDEX idx_user (user_id),
                    INDEX idx_default (is_default)
                )
            """)
            
            # Payment transactions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS payment_transactions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    order_id INT NOT NULL,
                    transaction_id VARCHAR(255) UNIQUE,
                    payment_method_id INT,
                    amount DECIMAL(10, 2) NOT NULL,
                    status ENUM('pending', 'processing', 'completed', 'failed', 'cancelled', 'refunded') DEFAULT 'pending',
                    gateway VARCHAR(50),
                    gateway_response TEXT,
                    processed_at TIMESTAMP NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
                    FOREIGN KEY (payment_method_id) REFERENCES payment_methods(id),
                    INDEX idx_order (order_id),
                    INDEX idx_transaction_id (transaction_id),
                    INDEX idx_status (status)
                )
            """)
            
            # Stock movements table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS stock_movements (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    product_id INT NOT NULL,
                    movement_type ENUM('in', 'out', 'adjustment') NOT NULL,
                    quantity INT NOT NULL,
                    reference_type ENUM('purchase', 'sale', 'return', 'adjustment') NOT NULL,
                    reference_id INT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
                    INDEX idx_product (product_id),
                    INDEX idx_type (movement_type),
                    INDEX idx_reference (reference_type, reference_id)
                )
            """)
            
            # Notifications table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notifications (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    type VARCHAR(50) NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    message TEXT NOT NULL,
                    is_read BOOLEAN DEFAULT FALSE,
                    action_url VARCHAR(500),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    read_at TIMESTAMP NULL,
                    
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    INDEX idx_user (user_id),
                    INDEX idx_read (is_read),
                    INDEX idx_type (type)
                )
            """)
            
            # System settings table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_settings (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    setting_key VARCHAR(100) UNIQUE NOT NULL,
                    setting_value TEXT,
                    description TEXT,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    
                    INDEX idx_key (setting_key),
                    INDEX idx_active (is_active)
                )
            """)
            
            print("All tables created successfully!")
            
            # Insert initial data
            print("Inserting initial data...")
            
            # Insert categories
            cursor.execute("""
                INSERT IGNORE INTO categories (name, slug, description, sort_order) VALUES
                ('Moda', 'moda', 'Roupas e acessórios de moda', 1),
                ('Eletrônicos', 'eletronicos', 'Dispositivos eletrônicos e gadgets', 2),
                ('Casa', 'casa', 'Produtos para o lar', 3),
                ('Games', 'games', 'Jogos e acessórios para gamers', 4),
                ('Esportes', 'esportes', 'Equipamentos esportivos', 5),
                ('Infantil', 'infantil', 'Produtos para bebês e crianças', 6)
            """)
            
            # Insert products
            cursor.execute("""
                INSERT IGNORE INTO products (name, description, price, old_price, category_id, stock_quantity, sku, rating, review_count) VALUES
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
                INSERT IGNORE INTO users (name, email, password, is_admin, city, state, country) VALUES
                ('Administrador', 'admin@bossshopp.com', '$2b$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', TRUE, 'São Paulo', 'SP', 'Brasil')
            """)
            
            # Insert system settings
            cursor.execute("""
                INSERT IGNORE INTO system_settings (setting_key, setting_value, description) VALUES
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
            
            connection.commit()
            print("Initial data inserted successfully!")
            
            # Create triggers
            print("Creating triggers...")
            
            # Trigger to update product rating after review
            cursor.execute("""
                CREATE TRIGGER IF NOT EXISTS update_product_rating_after_review
                AFTER INSERT ON product_reviews
                FOR EACH ROW
                BEGIN
                    UPDATE products 
                    SET rating = (
                        SELECT AVG(rating) 
                        FROM product_reviews 
                        WHERE product_id = NEW.product_id AND is_approved = TRUE
                    ),
                    review_count = (
                        SELECT COUNT(*) 
                        FROM product_reviews 
                        WHERE product_id = NEW.product_id AND is_approved = TRUE
                    )
                    WHERE id = NEW.product_id;
                END
            """)
            
            # Trigger to generate order number automatically
            cursor.execute("""
                CREATE TRIGGER IF NOT EXISTS generate_order_number
                BEFORE INSERT ON orders
                FOR EACH ROW
                BEGIN
                    IF NEW.order_number IS NULL OR NEW.order_number = '' THEN
                        SET NEW.order_number = CONCAT(
                            (SELECT setting_value FROM system_settings WHERE setting_key = 'order_number_prefix'),
                            LPAD(FLOOR(RAND() * 1000000000), 9, '0')
                        );
                    END IF;
                END
            """)
            
            # Trigger to update stock after order
            cursor.execute("""
                CREATE TRIGGER IF NOT EXISTS update_stock_after_order
                AFTER INSERT ON order_items
                FOR EACH ROW
                BEGIN
                    UPDATE products 
                    SET stock_quantity = stock_quantity - NEW.quantity
                    WHERE id = NEW.product_id;
                    
                    INSERT INTO stock_movements (product_id, movement_type, quantity, reference_type, reference_id)
                    VALUES (NEW.product_id, 'out', NEW.quantity, 'sale', NEW.order_id);
                END
            """)
            
            print("Triggers created successfully!")
            
            # Create views
            print("Creating views...")
            
            # View for products with category
            cursor.execute("""
                CREATE OR REPLACE VIEW products_with_category AS
                SELECT 
                    p.*,
                    c.name as category_name,
                    c.slug as category_slug
                FROM products p
                JOIN categories c ON p.category_id = c.id
                WHERE p.is_active = TRUE AND c.is_active = TRUE
            """)
            
            # View for orders with user
            cursor.execute("""
                CREATE OR REPLACE VIEW orders_with_user AS
                SELECT 
                    o.*,
                    u.name as user_name,
                    u.email as user_email
                FROM orders o
                JOIN users u ON o.user_id = u.id
            """)
            
            # View for sales statistics
            cursor.execute("""
                CREATE OR REPLACE VIEW sales_statistics AS
                SELECT 
                    DATE(o.created_at) as sale_date,
                    COUNT(*) as total_orders,
                    SUM(o.total_amount) as total_revenue,
                    AVG(o.total_amount) as average_order_value
                FROM orders o
                WHERE o.status IN ('delivered', 'shipped')
                GROUP BY DATE(o.created_at)
                ORDER BY sale_date DESC
            """)
            
            print("Views created successfully!")
            
            # Create additional indexes
            print("Creating additional indexes...")
            
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_category_active ON products(category_id, is_active)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_featured_active ON products(is_featured, is_active)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_user_status ON orders(user_id, status)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_date_status ON orders(created_at, status)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_reviews_product_approved ON product_reviews(product_id, is_approved)")
            
            print("Additional indexes created successfully!")
            
            print("\n" + "="*50)
            print("DATABASE SETUP COMPLETED SUCCESSFULLY!")
            print("="*50)
            print("Database: boss_shopp_complete")
            print("Tables created: 17")
            print("Initial categories: 6")
            print("Initial products: 24")
            print("Admin user: admin@bossshopp.com / password")
            print("="*50)
            
    except Error as e:
        print(f"Error: {e}")
        if connection:
            connection.rollback()
    
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("MySQL connection closed")

if __name__ == "__main__":
    create_database()