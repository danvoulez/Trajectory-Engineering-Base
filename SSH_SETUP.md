# 🔐 Configuração SSH - Guia Rápido

## Chave SSH Gerada

**Chave pública:**
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEn2LZKvw/QbmXy9AE8bi9BEB6BAzYNAmX9DpuPR6dmN github-trajectory-engineering
```

**Localização:** `~/.ssh/id_ed25519_github`

## Passo 1: Adicionar chave ao GitHub

### Opção A: Deploy Key (recomendado - apenas este repositório)

1. Acesse: https://github.com/danvoulez/Trajectory-Engineering-Base/settings/keys
2. Clique em **"Add deploy key"**
3. **Title:** `Trajectory Engineering - Local`
4. **Key:** Cole a chave pública acima
5. ✅ Marque **"Allow write access"**
6. Clique em **"Add key"**

### Opção B: SSH Key da Conta (todos os repositórios)

1. Acesse: https://github.com/settings/keys
2. Clique em **"New SSH key"**
3. **Title:** `Trajectory Engineering`
4. **Key:** Cole a chave pública acima
5. Clique em **"Add SSH key"**

## Passo 2: Configurar SSH no seu computador

```bash
# Adicionar ao ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519_github

# Testar conexão
ssh -T git@github.com
# Deve retornar: "Hi danvoulez! You've successfully authenticated..."
```

## Passo 3: Atualizar remote para SSH

```bash
git remote set-url origin git@github.com:danvoulez/Trajectory-Engineering-Base.git
git remote -v  # Verificar
```

## Passo 4: Testar push

```bash
git push origin main
```

## 🔒 Proteção do Repositório

### Branch Protection

Configure em: https://github.com/danvoulez/Trajectory-Engineering-Base/settings/branches

**Configurações recomendadas:**
- ✅ Require a pull request before merging
- ✅ Require approvals: **1**
- ✅ Require review from Code Owners
- ✅ Require conversation resolution before merging
- ✅ Require linear history
- ❌ Allow force pushes
- ❌ Allow deletions

### Segurança Adicional

1. **2FA:** Habilite autenticação de dois fatores na sua conta GitHub
2. **Secret Scanning:** Já habilitado automaticamente
3. **Dependabot:** Já habilitado para security updates

## ✅ Status Atual

- ✅ Chave SSH gerada
- ✅ Remote configurado (HTTPS temporário)
- ⏳ Aguardando adição da chave SSH no GitHub
- ⏳ Branch protection a configurar

