# Mapeamento UBL ↔ JSON✯Atomic (essencial)

| UBL (origem) | JSON✯Atomic (span) | Campo canônico | Observações |
|--------------|-------------------|----------------|-------------|
| entry_id / invoice # | ingest.raw | span_id / data.invoice_number | span_id único; número original preservado |
| date / datetime | ingest.raw | timestamp | ISO-8601Z |
| account / gl_account | ingest.raw | data.account | Plano de contas mapeado em tabela separada |
| debit / credit | ingest.raw | data.debit / data.credit | Números normalizados; moeda em currency |
| amount / total | ingest.raw | data.amount | Para invoices/orders |
| currency | ingest.raw | data.currency | ISO 4217 |
| counterparty | ingest.raw | data.counterparty | Cliente/fornecedor/terceiro |
| memo / description | ingest.raw | data.memo | Texto livre |
| batch_id | manifest.lot | lot.name / merkle.proofs | Lote contábil (dia/mês) |
| payment_ref | attestation.issue | economics.payment_ref | Atrela receita/royalty |

**Regra:** todo lançamento UBL que derive de /redeem **MUST** carregar `attestation_id`, `manifest_id`, `epoch_root`, `unote_txid`, `capsule_b3` no memo/refs.

