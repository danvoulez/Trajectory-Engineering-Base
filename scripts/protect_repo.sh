#!/bin/bash
# Configura proteção do repositório GitHub

set -e

REPO="danvoulez/Trajectory-Engineering-Base"

echo "🔒 Configurando proteção do repositório..."

# 1. Branch Protection Rules para main
echo "1. Configurando branch protection para 'main'..."
gh api repos/$REPO/branches/main/protection \
  --method PUT \
  -f required_status_checks='{"strict":true,"contexts":[]}' \
  -f enforce_admins=true \
  -f required_pull_request_reviews='{"required_approving_review_count":1,"dismiss_stale_reviews":true,"require_code_owner_reviews":true}' \
  -f restrictions=null \
  -f required_linear_history=false \
  -f allow_force_pushes=false \
  -f allow_deletions=false \
  -f block_creations=false \
  -f required_conversation_resolution=true || echo "⚠ Erro ao configurar branch protection (pode precisar de permissões)"

# 2. Configurar SSH para git operations (se preferir)
echo ""
echo "2. Configurando SSH..."
if [ -f ~/.ssh/id_ed25519_github.pub ]; then
    echo "   ✓ Chave SSH encontrada: ~/.ssh/id_ed25519_github.pub"
    echo ""
    echo "   Para usar SSH, atualize o remote:"
    echo "   git remote set-url origin git@github.com:$REPO.git"
    echo ""
    echo "   Chave pública:"
    cat ~/.ssh/id_ed25519_github.pub
    echo ""
    echo "   Adicione esta chave como Deploy Key no GitHub:"
    echo "   https://github.com/$REPO/settings/keys"
else
    echo "   ⚠ Chave SSH não encontrada"
fi

# 3. Configurar repository settings de segurança
echo ""
echo "3. Configurando settings de segurança..."
gh api repos/$REPO \
  --method PATCH \
  -f allow_squash_merge=true \
  -f allow_merge_commit=false \
  -f allow_rebase_merge=true \
  -f delete_branch_on_merge=true \
  -f allow_auto_merge=true || echo "⚠ Erro ao configurar settings"

# 4. Habilitar vulnerability alerts
echo ""
echo "4. Habilitando vulnerability alerts..."
gh api repos/$REPO/vulnerability-alerts \
  --method PUT || echo "⚠ Erro (pode precisar habilitar no Settings > Security)"

echo ""
echo "✓ Proteção configurada!"
echo ""
echo "📝 Próximos passos:"
echo "   1. Adicione a chave SSH como Deploy Key no GitHub"
echo "   2. Configure 2FA na sua conta GitHub"
echo "   3. Revise as branch protection rules em:"
echo "      https://github.com/$REPO/settings/branches"
