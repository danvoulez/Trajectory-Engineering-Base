# SLA — Verificação, Atestados e Resgate (v1)

## 1) Métricas & Alvos

* **/verify** (cápsula ≤ 50 MB, CPU):

  * p95 ≤ **1s**, p99 ≤ **2s**, **Disponibilidade** ≥ **99.9%/mês**.

* **/attest** (A/C/R/P, CPU; amostra ≤ 1 k itens):

  * p95 ≤ **30s/100 itens**, p99 ≤ **60s/100 itens**, **99.5%**.

* **/redeem** (execução com U-Notes):

  * **SLA default: 24h** para conclusão; filas GPU podem ampliar janela por cotação.

* **Spent-Log**:

  * **epoch**: 15 min; publicação do Merkle root ≤ **+2 min** após fim do epoch.

## 2) Itens Incluídos

* Verificação de **assinaturas, Merkle, cobertura**, conferência UBL e status de gasto.

* Reexecução gratuita quando houver:

  * `signature` inválida por falha do operador,

  * `merkle/seed mismatch`,

  * **corrupção** detectada em trânsito sob custódia.

## 3) Créditos & Erro Orçamentário

* **Erro orçamentário** mensal: 43 min para 99.9%.

* Crédito automático no próximo ciclo:

  * 99.0–99.9% → **10%**,

  * 95.0–99.0% → **25%**,

  * <95.0% → **50%**.

* Créditos não são reembolsáveis em dinheiro.

## 4) Idempotência & Retries

* `/redeem` **MUST** usar `Idempotency-Key` (UUID v4).

* Retries exponenciais com jitter; **Retry-After** em caso de `RATE_LIMIT`/conflito.

## 5) Exclusões

* Força maior, dependências externas fora do controle (ex.: cloud region outage), uso além de cotas contratadas, dados inválidos do cliente.

## 6) Observabilidade

* Export de métricas (Prometheus/OpenMetrics) **SHOULD** estar disponível.

* Relatórios mensais de disponibilidade **MUST** incluir p95/p99 e incidentes.
