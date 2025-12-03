# Canonicalização JSON — Regra Canônica

## Objetivo

Produzir `bytes_canon_hash_b3` determinístico.

## Regras (MUST)

1. **Codificação:** UTF-8 sem BOM.
2. **Chaves:** ordem lexicográfica binária (Unicode code points).
3. **Espaços:** nenhum (sem pretty-print).
4. **Nulos:** somente quando permitido por schema.
5. **Floats:** representação decimal curta e exata; sem NaN/Infinity; use string ou número conforme schema (recomenda-se evitar floats).
6. **Boolean/Integers:** padrão JSON.
7. **Arrays:** ordem preservada.
8. **Escapes:** apenas os exigidos pela especificação JSON (sem normalização de whitespace dentro de strings).
9. **Normalização de texto:** NFC (Unicode).

## Pseudocódigo

```
canon = json_canonicalize(obj)  // aplica regras 1–9
hash  = BLAKE3(canon)
```
