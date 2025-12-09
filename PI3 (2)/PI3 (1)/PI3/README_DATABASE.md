# BOSS SHOPP - Sistema de Banco de Dados

Este documento descreve o sistema completo de banco de dados do e-commerce BOSS SHOPP, baseado na análise detalhada de todo o código do projeto.

## 📋 Visão Geral

O sistema de banco de dados foi projetado para suportar todas as funcionalidades identificadas no código:

- **Sistema de usuários** com autenticação segura
- **Catálogo de produtos** com categorias e avaliações
- **Carrinho de compras** e lista de favoritos
- **Sistema de pedidos** completo com múltiplos status
- **Múltiplos endereços** por usuário
- **Sistema de cupons** de desconto
- **Controle de estoque** automatizado
- **Notificações** para usuários
- **Configurações** do sistema

## 🗄️ Estrutura do Banco de Dados

### Tabelas Principais

#### 👥 Usuários (`users`)
- Informações completas do cliente
- Autenticação com senha hash (bcrypt)
- Suporte a múltiplos endereços
- Campos para dados pessoais e de contato

#### 📦 Produtos (`products`)
- Catálogo completo com preços e descrições
- Sistema de categorias
- Controle de estoque
- Avaliações e ratings
- Múltiplas imagens por produto

#### 🛒 Carrinho (`cart_items`)
- Carrinho persistente por usuário
- Atualização automática de quantidades
- Integração com controle de estoque

#### 📋 Pedidos (`orders`, `order_items`)
- Sistema completo de pedidos
- Múltiplos status (pending, processing, shipped, delivered, cancelled)
- Histórico completo de transações
- Integração com endereços e pagamentos

#### ⭐ Avaliações (`product_reviews`)
- Sistema de reviews com ratings 1-5
- Comentários dos usuários
- Cálculo automático de rating médio

### Funcionalidades Avançadas

#### 🎫 Sistema de Cupons
- Cupons de desconto percentual ou valor fixo
- Controle de uso e validade
- Valor mínimo para aplicação

#### 💳 Pagamentos
- Múltiplos métodos de pagamento
- Histórico de transações
- Status de pagamento independente

#### 📊 Relatórios e Estatísticas
- Vendas por período
- Produtos mais vendidos
- Estatísticas de usuários
- Views otimizadas para consultas

## 🚀 Instalação e Configuração

### Pré-requisitos

1. **MySQL 8.0+** instalado e rodando
2. **Python 3.8+**
3. Dependências Python (ver `requirements.txt`)

### Instalação Automática

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar setup automático
python setup_database.py
```

O script irá:
- Conectar ao MySQL
- Criar o banco de dados
- Executar todo o schema SQL
- Inserir dados iniciais
- Verificar a instalação

### Instalação Manual

```bash
# 1. Conectar ao MySQL
mysql -u root -p

# 2. Executar o schema
source database_schema.sql
```

## 💻 Uso da API Python

### Exemplo Básico

```python
from database_manager import BossShoppDatabase, DatabaseConfig

# Configurar conexão
config = DatabaseConfig(
    host='localhost',
    user='root',
    password='sua_senha',
    database='boss_shopp_complete'
)

# Conectar
db = BossShoppDatabase(config)
db.connect()

# Criar usuário
user_id = db.create_user(
    name="João Silva",
    email="joao@example.com",
    password="senha123",
    phone="(11) 99999-9999"
)

# Obter produtos
products = db.get_products(category_slug='eletronicos', limit=10)

# Adicionar ao carrinho
db.add_to_cart(user_id, products[0]['id'], quantity=2)

# Criar pedido
cart_items = db.get_cart_items(user_id)
order_id = db.create_order(
    user_id=user_id,
    items=cart_items,
    shipping_address_id=1,
    payment_method='credit_card'
)

db.disconnect()
```

### Métodos Disponíveis

#### 👥 Usuários
- `create_user()` - Criar novo usuário
- `authenticate_user()` - Autenticar login
- `get_user_by_id()` - Obter dados do usuário
- `update_user()` - Atualizar perfil

#### 📦 Produtos
- `get_products()` - Listar produtos
- `get_product_by_id()` - Detalhes do produto
- `search_products()` - Buscar produtos
- `get_categories()` - Listar categorias

#### 🛒 Carrinho
- `add_to_cart()` - Adicionar item
- `get_cart_items()` - Ver carrinho
- `update_cart_item()` - Atualizar quantidade
- `remove_from_cart()` - Remover item
- `clear_cart()` - Limpar carrinho

#### ❤️ Favoritos
- `add_to_favorites()` - Adicionar favorito
- `remove_from_favorites()` - Remover favorito
- `get_user_favorites()` - Listar favoritos

#### 📋 Pedidos
- `create_order()` - Criar pedido
- `get_user_orders()` - Pedidos do usuário
- `get_order_by_id()` - Detalhes do pedido
- `update_order_status()` - Atualizar status

#### 📊 Relatórios
- `get_sales_statistics()` - Estatísticas de vendas
- `get_top_products()` - Produtos mais vendidos
- `get_user_statistics()` - Estatísticas de usuários

## 🔧 Configuração

### Variáveis de Ambiente

```bash
# .env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=boss_shopp_complete
```

### Configuração Python

```python
from database_manager import DatabaseConfig

config = DatabaseConfig(
    host=os.getenv('DB_HOST', 'localhost'),
    port=int(os.getenv('DB_PORT', 3306)),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME', 'boss_shopp_complete')
)
```

## 📈 Performance e Otimização

### Índices Criados

O schema inclui índices otimizados para:
- Consultas por email e telefone
- Busca de produtos por categoria
- Listagem de pedidos por usuário
- Consultas de carrinho e favoritos
- Relatórios de vendas

### Views Otimizadas

- `products_with_category` - Produtos com dados da categoria
- `orders_with_user` - Pedidos com dados do usuário
- `sales_statistics` - Estatísticas de vendas por data

### Triggers Automáticos

- **Atualização de rating**: Recalcula rating médio após nova avaliação
- **Geração de número do pedido**: Cria número único automaticamente
- **Controle de estoque**: Atualiza estoque após venda

## 🔒 Segurança

### Autenticação
- Senhas com hash bcrypt (salt automático)
- Validação de força da senha no frontend
- Tokens JWT para sessões

### Proteção de Dados
- Validação de entrada em todos os métodos
- Prepared statements para prevenir SQL injection
- Logs de auditoria para operações críticas

### Backup
```python
# Backup automático
db.backup_database('/path/to/backup.sql')
```

## 📊 Dados Iniciais

O sistema vem com dados de exemplo:

### Categorias (6)
- Moda
- Eletrônicos  
- Casa
- Games
- Esportes
- Infantil

### Produtos (24)
- 4 produtos por categoria
- Preços realistas
- Descrições detalhadas
- Ratings e reviews simulados

### Configurações
- Configurações padrão do sistema
- Valores para frete grátis
- Prefixos de pedidos
- Limites do carrinho

## 🐛 Troubleshooting

### Problemas Comuns

**Erro de conexão MySQL:**
```bash
# Verificar se MySQL está rodando
sudo systemctl status mysql

# Verificar porta
netstat -tlnp | grep :3306
```

**Erro de permissões:**
```sql
-- Criar usuário específico
CREATE USER 'bossshopp'@'localhost' IDENTIFIED BY 'senha_forte';
GRANT ALL PRIVILEGES ON boss_shopp_complete.* TO 'bossshopp'@'localhost';
FLUSH PRIVILEGES;
```

**Erro de charset:**
```sql
-- Verificar charset
SHOW VARIABLES LIKE 'character_set%';

-- Alterar se necessário
ALTER DATABASE boss_shopp_complete CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 📝 Logs e Monitoramento

### Configuração de Logs

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bossshopp.log'),
        logging.StreamHandler()
    ]
)
```

### Monitoramento de Performance

```sql
-- Consultas lentas
SHOW VARIABLES LIKE 'slow_query_log';
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;

-- Análise de queries
EXPLAIN SELECT * FROM products_with_category WHERE category_slug = 'eletronicos';
```

## 🔄 Migração e Atualizações

### Backup Antes de Atualizações

```bash
# Backup completo
mysqldump -u root -p boss_shopp_complete > backup_$(date +%Y%m%d).sql

# Backup apenas estrutura
mysqldump -u root -p --no-data boss_shopp_complete > structure_backup.sql
```

### Versionamento do Schema

O sistema suporta versionamento através da tabela `system_settings`:

```sql
INSERT INTO system_settings (setting_key, setting_value, description)
VALUES ('schema_version', '1.0.0', 'Versão atual do schema do banco');
```

## 📞 Suporte

Para dúvidas ou problemas:

1. Verifique os logs em `bossshopp.log`
2. Execute `python setup_database.py` novamente
3. Consulte a documentação do MySQL
4. Verifique as permissões do usuário do banco

## 📄 Licença

Este sistema de banco de dados faz parte do projeto BOSS SHOPP e segue a mesma licença do projeto principal.

---

**Desenvolvido com base na análise completa do código do projeto BOSS SHOPP** 🚀