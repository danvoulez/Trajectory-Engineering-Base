#!/usr/bin/env bash
# Script de release - valida, cria tag, gera artifacts e publica release

set -euo pipefail

REPO="danvoulez/Trajectory-Engineering-Base"

if [ -z "${1:-}" ]; then
    echo "Uso: $0 <version>"
    echo "Exemplo: $0 v1.0.1"
    exit 1
fi

TAG="${1}"
TAG_NAME="$TAG"
ZIP_NAME="diamond-${TAG}.zip"
B3_NAME="${ZIP_NAME}.b3"

echo "🚀 Criando release $VERSION..."

# 1. Validar
echo "1. Validando (make check)..."
make check || {
    echo "✗ make check falhou"
    exit 1
}

# 2. Verificar se tag já existe
if git rev-parse "$TAG_NAME" >/dev/null 2>&1; then
    echo "⚠ Tag $TAG_NAME já existe"
    read -p "Continuar mesmo assim? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 3. Atualizar CHANGELOG (se necessário)
if ! grep -q "## \[${VERSION#v}\]" CHANGELOG.md 2>/dev/null; then
    echo "⚠ Adicione entrada para $VERSION no CHANGELOG.md"
    read -p "Continuar mesmo assim? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 4. Criar tag
echo "2. Criando tag $TAG_NAME..."
git tag -s "$TAG_NAME" -m "release $TAG" 2>/dev/null || git tag "$TAG_NAME" -m "release $TAG" || {
    echo "✗ Erro ao criar tag"
    exit 1
}
git push origin "$TAG_NAME"

# 5. Gerar artifacts
echo "3. Gerando artifacts..."
git archive -o "$ZIP_NAME" HEAD
python3 scripts/b3sum.py "$ZIP_NAME" > "$B3_NAME"

echo "   ✓ $ZIP_NAME criado"
echo "   ✓ $B3_NAME criado"
ls -lh "$ZIP_NAME" "$B3_NAME"

# 6. Extrair notas do CHANGELOG
NOTES_FILE=$(mktemp)
if grep -q "## \[${VERSION#v}\]" CHANGELOG.md; then
    # Extrai seção do changelog
    sed -n "/## \[${VERSION#v}\]/,/## \[/p" CHANGELOG.md | sed '$d' > "$NOTES_FILE"
else
    echo "Release $VERSION" > "$NOTES_FILE"
fi

# 7. Criar release no GitHub
echo "4. Criando release no GitHub..."
gh release create "$TAG" \
    --title "$TAG" \
    --notes-file "$NOTES_FILE" \
    --repo "$REPO" \
    "$ZIP_NAME" \
    "$B3_NAME" || {
    echo "✗ Erro ao criar release"
    rm -f "$NOTES_FILE"
    exit 1
}

rm -f "$NOTES_FILE"

echo ""
echo "✅ Release $TAG criada com sucesso!"
echo "   📦 Artifacts: $ZIP_NAME, $B3_NAME"
echo "   🔗 https://github.com/$REPO/releases/tag/$TAG"
