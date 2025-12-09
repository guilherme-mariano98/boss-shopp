# Script PowerShell para remover produtos de exemplo do index.html

$filePath = "PI3/PI2/frontend/index.html"

Write-Host "🔄 Lendo arquivo..." -ForegroundColor Yellow

# Ler o conteúdo do arquivo
$content = Get-Content $filePath -Raw -Encoding UTF8

# Contar produtos antes
$produtosBefore = ([regex]::Matches($content, '<div class="product-card">')).Count

Write-Host "📦 Produtos encontrados: $produtosBefore" -ForegroundColor Cyan

# Mensagem para substituir produtos
$emptyMessage = @"
                <!-- Produtos serão carregados dinamicamente do banco de dados -->
                <div class="empty-products-message" style="text-align: center; padding: 60px 20px; grid-column: 1 / -1;">
                    <i class="fas fa-box-open" style="font-size: 64px; color: #ccc; margin-bottom: 20px;"></i>
                    <h3 style="color: #666; margin-bottom: 10px;">Nenhum produto disponível</h3>
                    <p style="color: #999;">Adicione produtos pelo painel administrativo</p>
                </div>
"@

# Padrão regex para encontrar products-grid com produtos
$pattern = '(<div class="products-grid">)(.*?)(</div>\s*(?:</div>\s*</section>|<div class="view-all-container">))'

# Substituir usando regex
$content = [regex]::Replace($content, $pattern, "`$1`n$emptyMessage`n            `$3", [System.Text.RegularExpressions.RegexOptions]::Singleline)

# Salvar o arquivo
$content | Out-File -FilePath $filePath -Encoding UTF8 -NoNewline

# Contar produtos depois
$produtosAfter = ([regex]::Matches($content, '<div class="product-card">')).Count

Write-Host ""
Write-Host "✅ Limpeza concluída!" -ForegroundColor Green
Write-Host "📊 Produtos removidos: $($produtosBefore - $produtosAfter)" -ForegroundColor Green
Write-Host "📄 Arquivo atualizado: $filePath" -ForegroundColor Green
Write-Host ""
Write-Host "🎯 Próximos passos:" -ForegroundColor Cyan
Write-Host "1. Acesse: http://localhost:3000/admin-panel.html"
Write-Host "2. Faça login como administrador"
Write-Host "3. Adicione seus produtos reais"
Write-Host "4. Os produtos aparecerão automaticamente"
