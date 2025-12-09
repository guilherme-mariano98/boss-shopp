#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para remover produtos de exemplo do index.html
Mantém a estrutura das seções, mas remove os cards de produtos
"""

import re

def remove_products_from_html():
    """Remove todos os produtos de exemplo do index.html"""
    
    # Ler o arquivo
    with open('PI3/PI2/frontend/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Padrão para remover product-cards dentro de products-grid
    # Remove desde <div class="product-card"> até o </div> correspondente
    pattern_product_card = r'<div class="product-card">.*?</div>\s*</div>\s*</div>'
    
    # Substituir produtos na seção Flash Sale
    # Encontrar a seção flash-sale e limpar os produtos
    flash_sale_pattern = r'(<section class="flash-sale[^>]*>.*?<div class="products-grid">)(.*?)(</div>\s*</div>\s*</section>)'
    
    def replace_flash_sale(match):
        before = match.group(1)
        after = match.group(3)
        # Adicionar mensagem de "sem produtos"
        empty_message = '''
                <div class="empty-products-message">
                    <i class="fas fa-box-open"></i>
                    <p>Nenhum produto em oferta no momento.</p>
                    <p class="small-text">Adicione produtos pelo painel administrativo.</p>
                </div>
            '''
        return before + empty_message + after
    
    content = re.sub(flash_sale_pattern, replace_flash_sale, content, flags=re.DOTALL)
    
    # Substituir produtos na seção Popular Products
    popular_pattern = r'(<section class="popular-products">.*?<div class="products-grid">)(.*?)(</div>\s*</div>\s*</section>)'
    
    def replace_popular(match):
        before = match.group(1)
        after = match.group(3)
        empty_message = '''
                <div class="empty-products-message">
                    <i class="fas fa-box-open"></i>
                    <p>Nenhum produto popular no momento.</p>
                    <p class="small-text">Adicione produtos pelo painel administrativo.</p>
                </div>
            '''
        return before + empty_message + after
    
    content = re.sub(popular_pattern, replace_popular, content, flags=re.DOTALL)
    
    # Salvar o arquivo modificado
    with open('PI3/PI2/frontend/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Produtos removidos com sucesso!")
    print("📝 Arquivo atualizado: PI3/PI2/frontend/index.html")
    print("\n🎯 Próximos passos:")
    print("1. Acesse o painel administrativo: http://localhost:3000/admin-panel.html")
    print("2. Adicione seus produtos reais")
    print("3. Os produtos aparecerão automaticamente na página inicial")

if __name__ == "__main__":
    remove_products_from_html()
