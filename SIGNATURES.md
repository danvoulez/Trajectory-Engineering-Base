# Assinaturas & Domain Separation

## Campos

* `bytes_canon_hash_b3` = BLAKE3(JSON canônico)
* `sig_context` ∈ {"diamond", "diamond:genesis", "diamond:tcap", "diamond:unote.tx", ...}
* `signature_ed25519` = Ed25519( concat(sig_context, "||", bytes_canon_hash_b3) )

## Regras

* **MUST** usar sig_context correto por tipo de span.
* **MUST** incluir owner_id/tenant_id quando aplicável.
* **Chaves:** Ed25519; armazenamento seguro; rotação conforme KEY-ROTATION.md.
