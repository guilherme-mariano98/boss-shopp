-- =====================================================
-- BOSS SHOPP SQLite DATABASE SCHEMA WITH ADMIN AND VENDOR ROLES
-- =====================================================

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- =====================================================
-- CORE TABLES
-- =====================================================

-- Users table with role support
CREATE TABLE users (
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
    is_vendor BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes for performance
    CONSTRAINT idx_users_email UNIQUE (email)
);

-- Categories table
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    description TEXT,
    image_url TEXT,
    is_active BOOLEAN DEFAULT 1,
    sort_order INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    old_price DECIMAL(10, 2),
    category_id INTEGER NOT NULL,
    image_url TEXT,
    stock_quantity INTEGER DEFAULT 0,
    sku TEXT UNIQUE,
    weight DECIMAL(8, 3),
    dimensions TEXT,
    is_active BOOLEAN DEFAULT 1,
    is_featured BOOLEAN DEFAULT 0,
    rating DECIMAL(3, 2) DEFAULT 0.00,
    review_count INTEGER DEFAULT 0,
    vendor_id INTEGER, -- Link to vendor who owns this product
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    FOREIGN KEY (vendor_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Product images table
CREATE TABLE product_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    image_url TEXT NOT NULL,
    alt_text TEXT,
    is_primary BOOLEAN DEFAULT 0,
    sort_order INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- User addresses table
CREATE TABLE user_addresses (
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
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Orders table
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number TEXT UNIQUE NOT NULL,
    user_id INTEGER NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    shipping_amount DECIMAL(10, 2) DEFAULT 0.00,
    tax_amount DECIMAL(10, 2) DEFAULT 0.00,
    discount_amount DECIMAL(10, 2) DEFAULT 0.00,
    status TEXT DEFAULT 'pending',
    payment_status TEXT DEFAULT 'pending',
    payment_method TEXT,
    shipping_address_id INTEGER,
    billing_address_id INTEGER,
    notes TEXT,
    shipped_at DATETIME,
    delivered_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (shipping_address_id) REFERENCES user_addresses(id),
    FOREIGN KEY (billing_address_id) REFERENCES user_addresses(id)
);

-- Order items table
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Shopping cart table
CREATE TABLE cart_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    UNIQUE(user_id, product_id)
);

-- Favorites table
CREATE TABLE favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    UNIQUE(user_id, product_id)
);

-- Product reviews table
CREATE TABLE product_reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    title TEXT,
    comment TEXT,
    is_verified_purchase BOOLEAN DEFAULT 0,
    is_approved BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(user_id, product_id)
);

-- Coupons table
CREATE TABLE coupons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    discount_type TEXT NOT NULL, -- 'percentage' or 'fixed'
    discount_value DECIMAL(10, 2) NOT NULL,
    minimum_amount DECIMAL(10, 2) DEFAULT 0.00,
    maximum_discount DECIMAL(10, 2),
    usage_limit INTEGER,
    used_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    starts_at DATETIME,
    expires_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Coupon usage table
CREATE TABLE coupon_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    coupon_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    order_id INTEGER NOT NULL,
    discount_amount DECIMAL(10, 2) NOT NULL,
    used_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (coupon_id) REFERENCES coupons(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);

-- Payment methods table
CREATE TABLE payment_methods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    type TEXT NOT NULL, -- 'credit_card', 'debit_card', 'pix', 'boleto'
    card_last_four TEXT,
    card_brand TEXT,
    card_holder_name TEXT,
    is_default BOOLEAN DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Payment transactions table
CREATE TABLE payment_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    transaction_id TEXT UNIQUE,
    payment_method_id INTEGER,
    amount DECIMAL(10, 2) NOT NULL,
    status TEXT DEFAULT 'pending',
    gateway TEXT,
    gateway_response TEXT,
    processed_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (payment_method_id) REFERENCES payment_methods(id)
);

-- Stock movements table
CREATE TABLE stock_movements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    movement_type TEXT NOT NULL, -- 'in', 'out', 'adjustment'
    quantity INTEGER NOT NULL,
    reference_type TEXT NOT NULL, -- 'purchase', 'sale', 'return', 'adjustment'
    reference_id INTEGER,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Notifications table
CREATE TABLE notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT 0,
    action_url TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    read_at DATETIME,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- System settings table
CREATE TABLE system_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_key TEXT UNIQUE NOT NULL,
    setting_value TEXT,
    description TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Vendor applications table (for users requesting vendor status)
CREATE TABLE vendor_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    business_name TEXT NOT NULL,
    business_description TEXT,
    business_registration TEXT,
    phone TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    country TEXT DEFAULT 'Brasil',
    status TEXT DEFAULT 'pending', -- 'pending', 'approved', 'rejected'
    rejection_reason TEXT,
    approved_by INTEGER,
    approved_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (approved_by) REFERENCES users(id)
);

-- Vendor commissions table
CREATE TABLE vendor_commissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vendor_id INTEGER NOT NULL,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    commission_rate DECIMAL(5, 4) NOT NULL, -- e.g., 0.15 for 15%
    commission_amount DECIMAL(10, 2) NOT NULL,
    status TEXT DEFAULT 'pending', -- 'pending', 'paid', 'cancelled'
    paid_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (vendor_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(is_admin, is_vendor);
CREATE INDEX idx_categories_slug ON categories(slug);
CREATE INDEX idx_categories_active ON categories(is_active);
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_vendor ON products(vendor_id);
CREATE INDEX idx_products_active ON products(is_active);
CREATE INDEX idx_products_featured ON products(is_featured);
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created ON orders(created_at);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);
CREATE INDEX idx_cart_items_user ON cart_items(user_id);
CREATE INDEX idx_favorites_user ON favorites(user_id);
CREATE INDEX idx_reviews_product ON product_reviews(product_id);
CREATE INDEX idx_reviews_approved ON product_reviews(is_approved);
CREATE INDEX idx_coupons_code ON coupons(code);
CREATE INDEX idx_coupons_active ON coupons(is_active);
CREATE INDEX idx_coupons_expires ON coupons(expires_at);
CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_read ON notifications(is_read);
CREATE INDEX idx_vendor_applications_user ON vendor_applications(user_id);
CREATE INDEX idx_vendor_applications_status ON vendor_applications(status);
CREATE INDEX idx_vendor_commissions_vendor ON vendor_commissions(vendor_id);
CREATE INDEX idx_vendor_commissions_order ON vendor_commissions(order_id);

-- =====================================================
-- INITIAL DATA INSERTION
-- =====================================================

-- Insert default categories
INSERT INTO categories (name, slug, description, sort_order) VALUES
('Moda', 'moda', 'Roupas e acessórios de moda', 1),
('Eletrônicos', 'eletronicos', 'Dispositivos eletrônicos e gadgets', 2),
('Casa', 'casa', 'Produtos para o lar', 3),
('Games', 'games', 'Jogos e acessórios para gamers', 4),
('Esportes', 'esportes', 'Equipamentos esportivos', 5),
('Infantil', 'infantil', 'Produtos para bebês e crianças', 6);

-- Insert default admin user
INSERT INTO users (name, email, password, is_admin, city, state, country) VALUES
('Administrador', 'admin@bossshopp.com', '$2b$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 1, 'São Paulo', 'SP', 'Brasil');

-- Insert default vendor user
INSERT INTO users (name, email, password, is_vendor, city, state, country) VALUES
('Vendedor Padrão', 'vendor@bossshopp.com', '$2b$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 0, 'São Paulo', 'SP', 'Brasil');

-- Insert sample products
INSERT INTO products (name, description, price, old_price, category_id, stock_quantity, sku, rating, review_count, vendor_id) VALUES
-- Moda
('Camiseta Básica', 'Camiseta de algodão 100% confortável e durável', 39.90, 49.90, 1, 100, 'MOD-CAM-001', 4.5, 234, 2),
('Calça Jeans', 'Calça jeans masculina com corte moderno', 89.90, NULL, 1, 50, 'MOD-CAL-001', 4.2, 87, 2),
('Tênis Esportivo', 'Tênis para corrida com tecnologia de amortecimento', 169.90, 199.90, 1, 30, 'MOD-TEN-001', 4.8, 156, 2),
('Boné Estiloso', 'Boné com proteção UV e design moderno', 34.90, NULL, 1, 75, 'MOD-BON-001', 4.0, 45, 2),

-- Eletrônicos
('Smartphone Premium', 'Smartphone com câmera de 108MP e 5G', 1760.00, 2200.00, 2, 25, 'ELE-SMT-001', 4.7, 189, 2),
('Notebook Ultrafino', 'Notebook com processador i7 e SSD 512GB', 2975.00, NULL, 2, 15, 'ELE-NOT-001', 4.6, 92, 2),
('Fone Bluetooth Sem Fio', 'Fone com cancelamento de ruído ativo', 224.90, 299.90, 2, 60, 'ELE-FON-001', 4.4, 267, 2),
('Smart TV 55"', 'TV 4K com HDR e sistema Android', 1750.00, 2100.00, 2, 20, 'ELE-TV-001', 4.5, 134, 2),

-- Casa
('Sofá Confortável', 'Sofá de 3 lugares com estrutura de madeira', 1020.00, 1200.00, 3, 10, 'CAS-SOF-001', 4.3, 78, 2),
('Cama Queen Size', 'Cama com headboard estofado', 899.90, NULL, 3, 8, 'CAS-CAM-001', 4.6, 56, 2),
('Jogo de Talheres', 'Talheres em aço inoxidável 24 peças', 159.90, 199.90, 3, 40, 'CAS-TAL-001', 4.2, 89, 2),
('Kit de Lâmpadas LED', 'Lâmpadas LED econômicas 9W - Kit 4 unidades', 97.40, NULL, 3, 80, 'CAS-LED-001', 4.1, 123, 2),

-- Games
('Console de Videogame', 'Console de última geração com 1TB', 2250.00, NULL, 4, 12, 'GAM-CON-001', 4.9, 345, 2),
('Jogo de Tabuleiro', 'Jogo estratégico para toda família', 89.90, NULL, 4, 35, 'GAM-TAB-001', 4.3, 67, 2),
('Fone Gamer', 'Fone com som surround 7.1 e microfone', 299.90, 399.90, 4, 25, 'GAM-FON-001', 4.5, 178, 2),
('Teclado Mecânico', 'Teclado RGB com switches blue', 319.90, NULL, 4, 18, 'GAM-TEC-001', 4.7, 234, 2),

-- Esportes
('Conjunto de Halteres', 'Halteres ajustáveis de 5 a 25kg', 254.90, NULL, 5, 22, 'ESP-HAL-001', 4.4, 89, 2),
('Tênis para Corrida', 'Tênis com amortecimento especial', 199.90, 249.90, 5, 45, 'ESP-TEN-001', 4.6, 156, 2),
('Bola de Futebol', 'Bola oficial com certificação FIFA', 74.90, NULL, 5, 60, 'ESP-BOL-001', 4.2, 234, 2),
('Bicicleta Mountain Bike', 'Bicicleta para trilhas com 21 marchas', 1299.90, 1599.90, 5, 8, 'ESP-BIC-001', 4.8, 67, 2),

-- Infantil
('Camiseta Infantil', 'Camiseta 100% algodão tamanhos 2 a 12 anos', 33.90, NULL, 6, 90, 'INF-CAM-001', 4.3, 145, 2),
('Meias Coloridas', 'Pacote com 5 pares de meias divertidas', 19.90, NULL, 6, 120, 'INF-MEI-001', 4.1, 89, 2),
('Sapatilha Infantil', 'Sapatilha para festas e ocasiões especiais', 47.90, NULL, 6, 55, 'INF-SAP-001', 4.4, 67, 2),
('Carrinho de Controle Remoto', 'Carrinho com controle remoto e luzes', 89.90, 119.90, 6, 30, 'INF-CAR-001', 4.6, 123, 2);

-- Insert system settings
INSERT INTO system_settings (setting_key, setting_value, description) VALUES
('site_name', 'BOSS SHOPP', 'Nome do site'),
('site_description', 'Sua loja online de confiança', 'Descrição do site'),
('currency', 'BRL', 'Moeda padrão'),
('tax_rate', '0.00', 'Taxa de imposto padrão'),
('free_shipping_minimum', '200.00', 'Valor mínimo para frete grátis'),
('max_cart_items', '50', 'Máximo de itens no carrinho'),
('order_number_prefix', 'BS', 'Prefixo do número do pedido'),
('email_notifications', 'true', 'Ativar notificações por email'),
('sms_notifications', 'false', 'Ativar notificações por SMS'),
('maintenance_mode', 'false', 'Modo de manutenção'),
('vendor_commission_rate', '0.15', 'Taxa de comissão padrão para vendedores');

-- =====================================================
-- TRIGGERS
-- =====================================================

-- Trigger to update timestamp on update
CREATE TRIGGER update_users_timestamp 
    AFTER UPDATE ON users
    FOR EACH ROW
    BEGIN
        UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
    END;

CREATE TRIGGER update_categories_timestamp 
    AFTER UPDATE ON categories
    FOR EACH ROW
    BEGIN
        UPDATE categories SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
    END;

CREATE TRIGGER update_products_timestamp 
    AFTER UPDATE ON products
    FOR EACH ROW
    BEGIN
        UPDATE products SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
    END;

CREATE TRIGGER update_orders_timestamp 
    AFTER UPDATE ON orders
    FOR EACH ROW
    BEGIN
        UPDATE orders SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
    END;

-- =====================================================
-- VIEWS
-- =====================================================

-- View for products with category information
CREATE VIEW products_with_category AS
SELECT 
    p.*,
    c.name as category_name,
    c.slug as category_slug
FROM products p
JOIN categories c ON p.category_id = c.id
WHERE p.is_active = 1 AND c.is_active = 1;

-- View for orders with user information
CREATE VIEW orders_with_user AS
SELECT 
    o.*,
    u.name as user_name,
    u.email as user_email
FROM orders o
JOIN users u ON o.user_id = u.id;

-- View for vendor products
CREATE VIEW vendor_products AS
SELECT 
    p.*,
    u.name as vendor_name,
    c.name as category_name
FROM products p
JOIN users u ON p.vendor_id = u.id
JOIN categories c ON p.category_id = c.id
WHERE p.is_active = 1 AND u.is_active = 1;

-- View for vendor statistics
CREATE VIEW vendor_statistics AS
SELECT 
    u.id as vendor_id,
    u.name as vendor_name,
    COUNT(DISTINCT p.id) as total_products,
    COUNT(DISTINCT vc.order_id) as total_sales,
    SUM(vc.commission_amount) as total_commissions,
    AVG(p.rating) as avg_rating
FROM users u
LEFT JOIN products p ON u.id = p.vendor_id
LEFT JOIN vendor_commissions vc ON u.id = vc.vendor_id
WHERE u.is_vendor = 1
GROUP BY u.id, u.name;

-- =====================================================
-- COMMENTS
-- =====================================================

/*
This SQLite schema extends the BOSS SHOPP database with:

1. Vendor Role Support:
   - Added is_vendor field to users table
   - Created vendor_applications table for vendor registration
   - Created vendor_commissions table for tracking vendor earnings
   - Added vendor_id to products table to link products to vendors

2. Enhanced Role Management:
   - Users can be admins (is_admin = 1)
   - Users can be vendors (is_vendor = 1)
   - Users can be both (though typically not recommended)
   - Vendor applications workflow with approval process

3. Vendor Features:
   - Vendors can own products
   - Commission tracking for vendor sales
   - Vendor statistics views
   - Vendor application management

4. Security & Performance:
   - Proper foreign key constraints
   - Indexes for common queries
   - Timestamps for audit trails
   - Views for simplified reporting

Sample users:
- Admin: admin@bossshopp.com (password: password)
- Vendor: vendor@bossshopp.com (password: password)

The schema maintains backward compatibility with existing code while adding
vendor functionality.
*/