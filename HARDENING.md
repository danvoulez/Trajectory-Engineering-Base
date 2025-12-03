# 🔒 Hardening Final - Checklist

## ✅ Concluído

### 1. ✅ Labels Criados
- `spec`, `schema`, `openapi`, `cli`, `examples`, `terms`, `security`, `breaking-change`, `good-first-issue`

### 2. ✅ CODEOWNERS & Templates
- `.github/CODEOWNERS` - Configurado
- `.github/ISSUE_TEMPLATE.md` - Criado
- `.github/pull_request_template.md` - Criado

### 3. ✅ Release Script
- `scripts/release.sh` - Script completo para releases
- Gera zip + b3sum automaticamente
- Valida com `make check` antes de criar release

### 4. ✅ Pre-commit Hooks
- `.pre-commit-config.yaml` - Configurado
- Valida schemas, examples, OpenAPI
- Instalar: `pip install pre-commit && pre-commit install`

### 5. ✅ Roadmap → Issues
- Milestone `v1.1.0` criado
- 6 issues do roadmap criadas (#4-#9)

### 6. ✅ Artifacts da Release
- `diamond-v1.0.0.zip` - Gerado
- `diamond-v1.0.0.zip.b3` - Hash BLAKE3 gerado
- Anexados à release v1.0.0

## ⏳ Pendente (Manual)

### 1. Branch Protection
**Acesse:** https://github.com/danvoulez/Trajectory-Engineering-Base/settings/branches

Configure para branch `main`:
- ✅ Require a pull request before merging
- ✅ Require approvals: **1**
- ✅ Require review from Code Owners
- ✅ Require status checks: `make check` (quando Actions estiver configurado)
- ✅ Require conversation resolution before merging
- ✅ Require linear history
- ❌ Allow force pushes
- ❌ Allow deletions

### 2. Status Check (Actions - Opcional)
Criar `.github/workflows/check.yml`:
```yaml
name: Check
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: make check
```

### 3. Security Polish
- Atualizar `SECURITY.md` com email real (se necessário)
- Atualizar `.well-known/security.txt` com URLs reais
- Substituir `pubkey.asc` placeholder por chave PGP real

### 4. Pre-commit Installation
```bash
pip install pre-commit
pre-commit install
```

## 📊 Status Final

- ✅ Labels: 9 criados
- ✅ Issues: 9 total (3 iniciais + 6 do roadmap)
- ✅ Milestone: v1.1.0 criado
- ✅ Release: v1.0.0 com artifacts
- ✅ Scripts: release, labels, roadmap issues
- ⏳ Branch protection: configurar manualmente
- ⏳ Actions: opcional (se quiser CI)

## 🚀 Próximos Passos

1. **Configurar branch protection** (manual via UI)
2. **Instalar pre-commit**: `pip install pre-commit && pre-commit install`
3. **Testar release script**: `./scripts/release.sh v1.0.1`
4. **Atualizar security files** com informações reais (se necessário)

