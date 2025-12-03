# Assinatura de Documentos — Demonstração do Fluxo

Este documento demonstra o fluxo completo de assinatura Ed25519 conforme o padrão Diamond Baseline v1.

## Fluxo Demonstrado

O arquivo `CHANGELOG.md` foi assinado seguindo o processo:

1. **Canonicalização**: Conteúdo normalizado (UTF-8, sem espaços extras)
2. **Hash BLAKE3**: `bytes_canon_hash_b3 = BLAKE3(conteúdo_canônico)`
3. **Domain Separation**: `message = sig_context || bytes_canon_hash_b3`
4. **Assinatura Ed25519**: `signature_ed25519 = Ed25519_sign(message)`

## Arquivos Gerados

- `CHANGELOG.md.sig` — Assinatura hexadecimal
- `CHANGELOG.md.proof.json` — Prova completa (hash, assinatura, chave pública, contexto)

## Verificação

Para verificar a assinatura:

```python
import nacl.signing
import nacl.encoding
from pathlib import Path

# Carrega prova
proof = json.loads(Path("CHANGELOG.md.proof.json").read_text())

# Carrega chave pública
verify_key = nacl.signing.VerifyKey(
    proof["pubkey_ed25519"],
    encoder=nacl.encoding.HexEncoder
)

# Reconstrói mensagem
message = (proof["sig_context"] + "||" + proof["bytes_canon_hash_b3"]).encode()

# Verifica
try:
    verify_key.verify(message, bytes.fromhex(proof["signature_ed25519"]))
    print("✓ Assinatura válida")
except:
    print("✗ Assinatura inválida")
```

## Regenerar Assinatura

Execute o script:

```bash
python3 scripts/generate_keys_and_sign.py
```

**Nota:** A chave privada (`.diamond_signing_key`) está no `.gitignore` e **NÃO** deve ser commitada.

## PGP (pubkey.asc)

O arquivo `pubkey.asc` é um placeholder. Para gerar uma chave PGP real:

```bash
gpg --full-generate-key
gpg --armor --export > pubkey.asc
```
