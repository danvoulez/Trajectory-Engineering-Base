#!/bin/bash
# Cria labels no repositório GitHub

REPO="danvoulez/Trajectory-Engineering-Base"

echo "🏷️  Criando labels..."

labels=(
    'spec:"Especificações técnicas"#0e8a16'
    'schema:"JSON Schemas"#1d76db'
    'openapi:"OpenAPI specs"#0052cc'
    'cli:"Command-line interfaces"#f9d0c4'
    'examples:"Exemplos de código"#fef2c0'
    'terms:"Contratos e termos"#b60205'
    'security:"Segurança e vulnerabilidades"#d93f0b'
    'breaking-change:"Mudanças que quebram compatibilidade"#b60205'
    'good-first-issue:"Bom para iniciantes"#0e8a16'
)

for label in "${labels[@]}"; do
    IFS=':' read -r name desc color <<< "$label"
    gh label create "$name" --description "$desc" --color "$color" --repo "$REPO" 2>/dev/null || \
    gh label edit "$name" --description "$desc" --color "$color" --repo "$REPO" 2>/dev/null || \
    echo "  ⚠ Label '$name' já existe ou erro"
done

echo "✓ Labels criados"

