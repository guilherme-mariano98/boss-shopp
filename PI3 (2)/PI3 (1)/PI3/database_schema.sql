-- =====================================================
-- BOSS SHOPP E-COMMERCE DATABASE SCHEMA
-- Banco de dados completo baseado na análise do código
-- =====================================================

-- Criar banco de dados
CREATE DATABASE IF NOT EXISTS boss_shopp_complete;
USE boss_shopp_complete;

-- =====================================================
-- TABELAS PRINCIPAIS
-- =====================================================

-- Tabela de usuários (clientes)
CREATE TABLE users (
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
);

-- Tabela de categorias
CREATE TABLE categories (
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
);

-- Tabela de produtos
CREATE TABLE products (
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
);

-- Tabela de imagens de produtos
CREATE TABLE product_images (
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
);

-- Tabela de endereços dos usuários
CREATE TABLE user_addresses (
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
);

-- Tabela de pedidos
CREATE TABLE orders (
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
);

-- Tabela de itens do pedido
CREATE TABLE order_items (
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
);

-- Tabela de carrinho de compras
CREATE TABLE cart_items (
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
);

-- Tabela de favoritos
CREATE TABLE favorites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_product (user_id, product_id),
    INDEX idx_user (user_id),
    INDEX idx_product (product_id)
);

-- Tabela de avaliações de produtos
CREATE TABLE product_reviews (
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
);

-- Tabela de cupons de desconto
CREATE TABLE coupons (
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
);

-- Tabela de uso de cupons
CREATE TABLE coupon_usage (
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
);

-- Tabela de métodos de pagamento
CREATE TABLE payment_methods (
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
);

-- Tabela de transações de pagamento
CREATE TABLE payment_transactions (
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
);

-- Tabela de histórico de estoque
CREATE TABLE stock_movements (
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
);

-- Tabela de notificações
CREATE TABLE notifications (
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
);

-- Tabela de configurações do sistema
CREATE TABLE system_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_key (setting_key),
    INDEX idx_active (is_active)
);

-- =====================================================
-- INSERÇÃO DE DADOS INICIAIS
-- =====================================================

-- Inserir categorias
INSERT INTO categories (name, slug, description, sort_order) VALUES
('Moda', 'moda', 'Roupas e acessórios de moda', 1),
('Eletrônicos', 'eletronicos', 'Dispositivos eletrônicos e gadgets', 2),
('Casa', 'casa', 'Produtos para o lar', 3),
('Games', 'games', 'Jogos e acessórios para gamers', 4),
('Esportes', 'esportes', 'Equipamentos esportivos', 5),
('Infantil', 'infantil', 'Produtos para bebês e crianças', 6);

-- Inserir produtos
INSERT INTO products (name, description, price, old_price, category_id, stock_quantity, sku, rating, review_count) VALUES
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
('Carrinho de Controle Remoto', 'Carrinho com controle remoto e luzes', 89.90, 119.90, 6, 30, 'INF-CAR-001', 4.6, 123);

-- Inserir usuário administrador padrão
INSERT INTO users (name, email, password, is_admin, city, state, country) VALUES
('Administrador', 'admin@bossshopp.com', '$2b$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', TRUE, 'São Paulo', 'SP', 'Brasil');

-- Inserir configurações do sistema
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
('maintenance_mode', 'false', 'Modo de manutenção');

-- =====================================================
-- TRIGGERS E PROCEDURES
-- =====================================================

-- Trigger para atualizar rating do produto após inserir/atualizar review
DELIMITER //
CREATE TRIGGER update_product_rating_after_review
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
END//

-- Trigger para gerar número do pedido automaticamente
CREATE TRIGGER generate_order_number
BEFORE INSERT ON orders
FOR EACH ROW
BEGIN
    IF NEW.order_number IS NULL OR NEW.order_number = '' THEN
        SET NEW.order_number = CONCAT(
            (SELECT setting_value FROM system_settings WHERE setting_key = 'order_number_prefix'),
            LPAD(FLOOR(RAND() * 1000000000), 9, '0')
        );
    END IF;
END//

-- Trigger para atualizar estoque após inserir item do pedido
CREATE TRIGGER update_stock_after_order
AFTER INSERT ON order_items
FOR EACH ROW
BEGIN
    UPDATE products 
    SET stock_quantity = stock_quantity - NEW.quantity
    WHERE id = NEW.product_id;
    
    INSERT INTO stock_movements (product_id, movement_type, quantity, reference_type, reference_id)
    VALUES (NEW.product_id, 'out', NEW.quantity, 'sale', NEW.order_id);
END//

DELIMITER ;

-- =====================================================
-- VIEWS ÚTEIS
-- =====================================================

-- View para produtos com informações da categoria
CREATE VIEW products_with_category AS
SELECT 
    p.*,
    c.name as category_name,
    c.slug as category_slug
FROM products p
JOIN categories c ON p.category_id = c.id
WHERE p.is_active = TRUE AND c.is_active = TRUE;

-- View para pedidos com informações do usuário
CREATE VIEW orders_with_user AS
SELECT 
    o.*,
    u.name as user_name,
    u.email as user_email
FROM orders o
JOIN users u ON o.user_id = u.id;

-- View para estatísticas de vendas
CREATE VIEW sales_statistics AS
SELECT 
    DATE(o.created_at) as sale_date,
    COUNT(*) as total_orders,
    SUM(o.total_amount) as total_revenue,
    AVG(o.total_amount) as average_order_value
FROM orders o
WHERE o.status IN ('delivered', 'shipped')
GROUP BY DATE(o.created_at)
ORDER BY sale_date DESC;

-- =====================================================
-- ÍNDICES ADICIONAIS PARA PERFORMANCE
-- =====================================================

-- Índices compostos para consultas frequentes
CREATE INDEX idx_products_category_active ON products(category_id, is_active);
CREATE INDEX idx_products_featured_active ON products(is_featured, is_active);
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
CREATE INDEX idx_orders_date_status ON orders(created_at, status);
CREATE INDEX idx_reviews_product_approved ON product_reviews(product_id, is_approved);

-- =====================================================
-- COMENTÁRIOS FINAIS
-- =====================================================

/*
Este schema foi criado baseado na análise completa do código do projeto BOSS SHOPP.
Inclui todas as funcionalidades identificadas:

1. Sistema de usuários com autenticação
2. Catálogo de produtos com categorias
3. Carrinho de compras e favoritos
4. Sistema de pedidos completo
5. Avaliações e reviews
6. Sistema de cupons
7. Múltiplos endereços por usuário
8. Métodos de pagamento
9. Controle de estoque
10. Notificações
11. Configurações do sistema

O banco está otimizado com índices apropriados e inclui triggers
para automatizar operações comuns como atualização de ratings
e controle de estoque.
*/