import os
import re

# Diretório das páginas
frontend_dir = "PI3/PI2/frontend"

# Lista de arquivos de categoria
category_files = [
    "categoria-alimentos.html",
    "categoria-automotivo.html",
    "categoria-beleza.html",
    "categoria-brinquedos.html",
    "categoria-casa.html",
    "categoria-esportes.html",
    "categoria-ferramentas.html",
    "categoria-games.html",
    "categoria-infantil.html",
    "categoria-livros.html",
    "categoria-moda.html",
    "categoria-musica.html",
    "categoria-papelaria.html",
    "categoria-pet-shop.html",
    "categoria-saude.html"
]

# Padrão para encontrar a seção de estilos inline
style_pattern = re.compile(
    r'<link rel="stylesheet" href="pages\.css">.*?<style>.*?</style>',
    re.DOTALL
)

# Novo conteúdo para substituir
new_links = '''<link rel="stylesheet" href="pages.css">
    <link rel="stylesheet" href="categoria-styles.css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">'''

updated_count = 0

for filename in category_files:
    filepath = os.path.join(frontend_dir, filename)
    
    if not os.path.exists(filepath):
        print(f"❌ Arquivo não encontrado: {filename}")
        continue
    
    try:
        # Ler o arquivo
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Substituir a seção de estilos
        new_content = style_pattern.sub(new_links, content)
        
        # Salvar o arquivo atualizado
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        updated_count += 1
        print(f"✅ Atualizado: {filename}")
        
    except Exception as e:
        print(f"❌ Erro ao processar {filename}: {str(e)}")

print(f"\n🎉 Total de páginas atualizadas: {updated_count}/{len(category_files)}")
