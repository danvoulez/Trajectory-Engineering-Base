# TBAC v1 — Normas e Ferramentas

## Arquivos adicionados

* `docs/TBAC-SPEC.md` — norma v1 (caps, sharding, merkle, encadeamento ROOT)
* `schemas/tbac.schema.json` — JSON Schema v1
* `tools/verify_tbac.py` — verificador de Merkle (blake2s/sha256; blake3 opcional)

## Motivação

* **Distribuição confiável** (≤8MB bruto / ≤2MB gzip / ≤50k entries)
* **Verificação barata** (Merkle) e encadeamento mensal → all-time
* **Compatível com compute-to-data** e policy "derived-only"

## Próximos passos

* `tools/generate_tbac.py` (gerar mensal a partir dos manifests TCAP)
* spent-log v0 (mint/reserve/consume) com IDs de TBAC
* adicionar `tbac_root` nos certificados para vincular economics → agregados

