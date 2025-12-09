#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para limpar TODOS os produtos de exemplo do index.html
"""

import re

def limpar_produtos():
    """Remove todos os produtos de exemplo mantendo a estrutura"""
    
    # Ler o arquivo
    with open('PI3/PI2/frontend/index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Mensagem vazia padrão
    empty_msg = '''                <!-- Produtos serão carregados dinamicamente do banco de dados -->
                <div class="empty-products-message" style="text-align: center; padding: 60px 20px; grid-column: 1 / -1;">
                    <i class="fas fa-box-open" style="font-size: 64px; color: #ccc; margin-bottom: 20px;"></i>
                    <h3 style="color: #666; margin-bottom: 10px;">Nenhum produto disponível</h3>
                    <p style="color: #999;">Adicione produtos pelo painel administrativo</p>
                </div>'''
    
    # Padrão para encontrar e limpar products-grid com produtos
    # Remove tudo entre <div class="products-grid"> e </div> (fechamento do grid)
    pattern = r'(<div class="products-grid">)(.*?)(</div>\s*(?:</div>\s*</section>|<div class="view-all-container">))'
    
    def replace_products(match):
        before = match.group(1)
        after = match.group(3)
        return before + '\n' + empty_msg + '\n            ' + after
    
    # Aplicar substituição
    content_new = re.sub(pattern, replace_products, content, flags=re.DOTALL)
    
    # Salvar
    with open('PI3/PI2/frontend/index.html', 'w', encoding='utf-8') as f:
        f.write(content_new)
    
    print("✅ TODOS os produtos foram removidos!")
    print("📄 Arquivo atualizado: PI3/PI2/frontend/index.html")
    print("\n🎯 Próximos passos:")
    print("1. Acesse: http://localhost:3000/admin-panel.html")
    print("2. Faça login como administrador")
    print("3. Adicione seus produtos reais")
    print("4. Os produtos aparecerão automaticamente na página")

if __name__ == "__main__":
    limpar_produtos()
