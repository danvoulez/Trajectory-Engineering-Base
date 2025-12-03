#!/bin/bash
# Configura repositório GitHub via GitHub CLI

set -e

REPO="danvoulez/Trajectory-Engineering-Base"

echo "🔧 Configurando repositório GitHub..."

# 1. Descrição e topics
echo "1. Configurando descrição e topics..."
gh repo edit "$REPO" \
  --description "Baseline for Trajectory Engineering: JSON✯Atomic schemas, OpenAPI, CLIs, examples" \
  --add-topic "trajectory" \
  --add-topic "json-atomic" \
  --add-topic "diamond" \
  --add-topic "audit" \
  --add-topic "ai-training" \
  --add-topic "merkle" \
  --add-topic "blake3" \
  --add-topic "ed25519" || echo "⚠ Erro ao configurar (pode precisar de permissões)"

# 2. Release v1.0.0
echo ""
echo "2. Criando release v1.0.0..."
if gh release view v1.0.0 --repo "$REPO" &>/dev/null; then
    echo "   ✓ Release v1.0.0 já existe"
else
    gh release create v1.0.0 \
      --title "Diamond Baseline v1.0.0" \
      --notes-file CHANGELOG.md \
      --repo "$REPO" || echo "⚠ Erro ao criar release"
fi

# 3. Issues iniciais
echo ""
echo "3. Criando issues iniciais..."

gh issue create \
  --title "Spec Freeze v1 (breaking só na v2)" \
  --body "Congelar especificações da v1. Mudanças breaking apenas na v2." \
  --repo "$REPO" || echo "⚠ Issue já existe ou erro"

gh issue create \
  --title "AuditSet/EvalSuite v1 (chatlogs)" \
  --body "Criar AuditSet e EvalSuite v1 para chatlogs com seeds/hashes selados." \
  --repo "$REPO" || echo "⚠ Issue já existe ou erro"

gh issue create \
  --title "Proto-CLIs (tcap/unote/spent/diamante; dry-run)" \
  --body "Implementar CLIs prototipais para tcap, unote, spent e diamante (modo dry-run)." \
  --repo "$REPO" || echo "⚠ Issue já existe ou erro"

echo ""
echo "✓ Configuração concluída!"

