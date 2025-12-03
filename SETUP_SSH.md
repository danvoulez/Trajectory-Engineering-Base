# Configuração SSH para o Repositório

## Chave SSH Gerada

Uma chave SSH Ed25519 foi gerada em: `~/.ssh/id_ed25519_github`

## Como Usar

### 1. Adicionar chave ao ssh-agent

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519_github
```

### 2. Adicionar ao GitHub

**Opção A: Deploy Key (apenas este repositório)**
1. Acesse: https://github.com/danvoulez/Trajectory-Engineering-Base/settings/keys
2. Clique em "Add deploy key"
3. Cole o conteúdo de `~/.ssh/id_ed25519_github.pub`
4. Marque "Allow write access" se quiser push via SSH

**Opção B: SSH Key da Conta (todos os repositórios)**
1. Acesse: https://github.com/settings/keys
2. Clique em "New SSH key"
3. Cole o conteúdo de `~/.ssh/id_ed25519_github.pub`

### 3. Atualizar remote para SSH

```bash
git remote set-url origin git@github.com:danvoulez/Trajectory-Engineering-Base.git
```

### 4. Testar conexão

```bash
ssh -T git@github.com
```

## Segurança

- **Nunca compartilhe a chave privada** (`~/.ssh/id_ed25519_github`)
- A chave privada está no `.gitignore` e não será commitada
- Use senha forte se adicionar passphrase: `ssh-keygen -p -f ~/.ssh/id_ed25519_github`

