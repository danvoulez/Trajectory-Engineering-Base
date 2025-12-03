# CLIs v1.0 — Especificação de Interface

## tcap (Trajectory Capsule)
- `tcap pack --manifest <path> --index <path> --blocks <dir|ndjson> --out <file.tcap> --compression [none|zstd] --encrypt [true|false]`
- `tcap verify --file <file.tcap>`
- `tcap seek --file <file.tcap> --span-id <id>`
- `tcap extract --file <file.tcap> --out <ndjson> [--filter-span-type <type>]`

## diamante (serviços de mercado)
- `diamante-verify --manifest <path> --checks signature,merkle,coverage,ubl_match,spent`
- `diamante-attest --targets <ids|file> --metrics A,C,R[,V] --gpu [true|false] --sample <n> --out <attest.jsonl>`
- `diamante-quote --items <n> --sla <hours> --currency <ISO4217> --counterparty <id> --out <quote.json>`
- `diamante-redeem --quote <quote.json> --payment-ref <ref> --manifest <path> --unotes <id1,id2,...> --idempotency-key <uuid> --out <report.json>`

## unote (direitos de uso)
- `unote-issue --tid <tid> --policy-id <id> --amount <n> --serial <n> --out <tx.json>`
- `unote-split --tx <in.json> --outputs <33,33,34> --out <tx.json>`
- `unote-spend --tx <in.json> --spent-endpoint <url> --out <receipt.json>`

## spent-log (transparência)
- `spent-submit --tx <tx.json> --endpoint <url> --out <proof.json>`
- `spent-proof --unote-id <id> --endpoint <url> --out <proof.json>`
- `spent-epoch --id <epoch_id> --endpoint <url> --out <epoch.json>`

### Requisitos comuns
- `--auth <api_key>` (ou cabeçalho `Authorization`)
- `--tenant <did:...>` (quando aplicável)
- Saída determinística (ordem lexicográfica de chaves).
- Códigos de erro estáveis: `SPENT_CONFLICT`, `BAD_MANIFEST`, `UNAUTHORIZED`, `RATE_LIMIT`, `INTERNAL`.
