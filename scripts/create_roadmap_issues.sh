#!/bin/bash
# Cria issues do ROADMAP.md

REPO="danvoulez/Trajectory-Engineering-Base"

echo "🗺️  Criando issues do roadmap..."

# Milestone v1.1.0
gh api repos/$REPO/milestones \
  --method POST \
  -f title="v1.1.0" \
  -f description="CBOR mode, AuditSet v1, EvalSuite v1" \
  -f due_on="2026-03-31T00:00:00Z" 2>/dev/null || echo "  ⚠ Milestone já existe ou erro"

MILESTONE="v1.1.0"

# Q1 Issues
gh issue create \
  --title "AuditSet v1 (chatlogs)" \
  --body "Criar AuditSet v1 para chatlogs:
- Seeds/hashes selados
- 1k pares por domínio
- Casos positivos/negativos balanceados
- Contraexemplos adversariais leves" \
  --milestone "$MILESTONE" \
  --label "spec" \
  --repo "$REPO" 2>/dev/null || echo "  ⚠ Issue já existe"

gh issue create \
  --title "EvalSuite v1: NLI/FEVER/QA/coerência" \
  --body "Criar EvalSuite v1:
- NLI/FEVER/QA estruturado
- Coerência, extrativismo vs geração
- Bootstrap 2k, IC-95%
- Seeds fixos, prompts imutáveis" \
  --milestone "$MILESTONE" \
  --label "spec" \
  --repo "$REPO" 2>/dev/null || echo "  ⚠ Issue já existe"

gh issue create \
  --title "Spent-Log v0: epochs (15 min), Merkle root, proof API" \
  --body "Implementar Spent-Log v0:
- Epochs de 15 minutos
- Merkle root por epoch
- API de proof (GCS/Merkle frontier)
- Endpoints submit/proof/epoch" \
  --milestone "$MILESTONE" \
  --label "spec" \
  --repo "$REPO" 2>/dev/null || echo "  ⚠ Issue já existe"

# Q2 Issues
gh issue create \
  --title "tcap CBOR (v1.1 performance mode)" \
  --body "Implementar modo CBOR para TCAP v1.1:
- Performance mode alternativo ao JSONL
- Canonicalização idêntica
- Compatibilidade com v1 (JSONL)" \
  --milestone "$MILESTONE" \
  --label "spec" \
  --label "cli" \
  --repo "$REPO" 2>/dev/null || echo "  ⚠ Issue já existe"

gh issue create \
  --title "U-Notes split/merge/stats; GCS para non-membership" \
  --body "Melhorias em U-Notes:
- Split/merge operations
- Estatísticas e tracking
- GCS (Golomb-coded sets) para non-membership proofs" \
  --milestone "$MILESTONE" \
  --label "spec" \
  --repo "$REPO" 2>/dev/null || echo "  ⚠ Issue já existe"

gh issue create \
  --title "UBL integração mínima (journal templates)" \
  --body "Integração UBL básica:
- Templates de journal entries
- Partidas dobradas canônicas
- Reconciliação automática" \
  --milestone "$MILESTONE" \
  --label "spec" \
  --repo "$REPO" 2>/dev/null || echo "  ⚠ Issue já existe"

echo "✓ Issues do roadmap criadas"

