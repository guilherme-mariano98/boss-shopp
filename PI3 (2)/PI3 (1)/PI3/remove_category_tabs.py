#!/usr/bin/env python3
"""
Script para remover a seção Category Tabs do index.html
"""

# Ler o arquivo
with open('PI3 (2)/PI3 (1)/PI3/PI2/frontend/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Encontrar início e fim da seção
start_idx = None
end_idx = None
in_category_tabs = False

for i, line in enumerate(lines):
    if '<!-- Category Tabs - Removida -->' in line or '<!-- Category Tabs -->' in line:
        start_idx = i
        in_category_tabs = True
    elif in_category_tabs and '<!-- Newsletter -->' in line:
        end_idx = i
        break

if start_idx is not None and end_idx is not None:
    # Remover as linhas entre start_idx e end_idx
    new_lines = lines[:start_idx] + ['\n', '    <!-- Newsletter -->\n'] + lines[end_idx+1:]
    
    # Escrever de volta
    with open('PI3 (2)/PI3 (1)/PI3/PI2/frontend/index.html', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"✓ Seção removida com sucesso!")
    print(f"  Linhas removidas: {end_idx - start_idx}")
else:
    print("✗ Não foi possível encontrar a seção")
