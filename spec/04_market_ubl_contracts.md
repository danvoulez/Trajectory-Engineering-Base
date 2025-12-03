# Comercialização

# O que é

O **mercado do Diamante** comercializa **execuções/atestados** (não o dado cru). Você entrega uma trajetória verificável; o comprador paga por **/verify**, **/attest** ou **/redeem**; a corretora executa sob SLA, registra tudo no **UBL** (partidas dobradas) e emite um **attestation.issue** com provas.

# Quem são os atores

* **Titular**: dono da trajetória (TID). Recebe **royalties**.

* **Corretora/Custodiante**: guarda, verifica, executa e emite atestados. Mantém **Spent-Log** e UBL.

* **Comprador**: contrata verificação/auditoria/score. Recebe relatório assinado.

# O que se compra

* **verify**: prova de integridade e proveniência (P) + cobertura/Merkle.

* **attest**: A/C/R (CPU). Opcional V(T) se houver GPU.

* **redeem**: execução contratada com **U-Notes** como pagamento (anti-double-spend), emissão de **attestation.issue** e lançamentos UBL.

---

## Ciclo de vida (fim-a-fim)

1. **Quote** → comprador pede preço e SLA.

2. **Pagamento/Reserva** → aceita o quote (pode pré-pagar); U-Notes são designadas.

3. **Redeem** → execução contratada; corretora valida **Spent-Log** (não-gasto).

4. **Atestado** → entrega `attestation.issue` (A/R/C[/V]) com recibo.

5. **Contabilidade (UBL)** → receita, receita diferida, royalty, custos, impostos; tudo reconciliado por IDs/hashes.

---

## Autenticação

Todos os endpoints **MUST** exigir:

* **API Key**: header `X-API-Key` ou `Authorization: Bearer <token>`.

* **Assinatura**: **MUST** usar **HMAC-SHA256** ou **Ed25519** sobre o corpo da requisição + timestamp.

* **Idempotency Key**: **MUST** estar presente em `/redeem` (header `Idempotency-Key`) para evitar duplicação.

**Exemplo de headers:**

```
X-API-Key: ak_live_...
X-Signature: ed25519:...
X-Timestamp: 2025-12-03T10:00:00Z
Idempotency-Key: idem_abc123...  (apenas em /redeem)
```

---

## Contratos de API (E/S estáveis)

### /quote

* **Para**: descobrir preço e prazo.

* **Autenticação**: **MUST** ter API Key + assinatura.

* **Entrada**

```json
{"scope":"audit","items":800,"sla_hours":24,"currency":"EUR","counterparty":"buyer_123"}
```

* **Saída**

```json
{"quote_id":"q_123","price_eur":55.0,
 "formula":{"base":15,"alpha":0.05,"beta":10},
 "expires_at":"2025-12-05T23:59:59Z",
 "signature":"<ed25519>","ubl_preview":{"invoice_no":"INV-q_123","due_date":"2025-12-06"}}
```

### /redeem

* **Para**: executar o serviço contratado (consome U-Notes).

* **Autenticação**: **MUST** ter API Key + assinatura + **Idempotency-Key**.

* **Entrada**

```json
{"quote_id":"q_123","payment_ref":"tx_789",
 "manifest":"s3://.../manifest.lot.jsonl",
 "unotes":["u_B","u_C"],"gpu":false,"sample":512}
```

* **Saída**

```json
{"ok":true,
 "attestation":{"span_id":"att_...","metrics":{"A":0.81,"R":1.58,"C":0.73,"P":1.0,"V":null},
                "receipt":{"hash":"b3:...","signature":"ed25519:..."}},
 "ubl_entries":["invoice:INV-q_123","journal:JB-457"],
 "unote_txid":"utx_abc","epoch_root":"er_999"}
```

### /verify

* **Para**: checar integridade/proveniência e reconciliação.

* **Autenticação**: **MUST** ter API Key + assinatura.

* **Entrada**

```json
{"manifest_path":"s3://.../manifest.lot.jsonl",
 "checks":["signature","merkle","coverage","ubl_match","spent"]}
```

* **Saída**

```json
{"ok":true,"P":1.0,"coverage":0.92,
 "ubl_match":{"invoice":"INV-q_123","status":"matched"},
 "spent":{"status":"not_spent","proof":"merkle:..."}}
```

### /attest

* **Para**: calcular métricas A/C/R (e opcionalmente V).

* **Autenticação**: **MUST** ter API Key + assinatura.

* **Entrada**

```json
{"manifest_path":"s3://.../manifest.lot.jsonl",
 "metrics":["A","C","R"],"gpu":false}
```

* **Saída**

```json
{"ok":true,
 "attestation":{"span_id":"att_...","metrics":{"A":0.81,"R":1.58,"C":0.73},
                "receipt":{"hash":"b3:...","signature":"ed25519:..."}}}
```

---

## Schema de Erros

Todos os endpoints **MUST** retornar erros no seguinte formato:

```json
{
  "error": {
    "code": "SPENT_CONFLICT",
    "message": "U-Note already spent",
    "details": {"unote_id": "u_B", "epoch_id": "ep_123"},
    "retry_after": 60
  }
}
```

**Códigos de erro:**

* `UNAUTHORIZED`: API Key ou assinatura inválida.
* `BAD_MANIFEST`: manifest inválido ou não encontrado.
* `SPENT_CONFLICT`: U-Note já foi gasto.
* `INVALID_QUOTE`: quote expirado ou inválido.
* `SLA_VIOLATION`: execução excedeu SLA.
* `SEED_MISMATCH`: seed não corresponde ao esperado.
* `SIGNATURE_INVALID`: assinatura do manifest inválida.
* `MERKLE_MISMATCH`: Merkle root não corresponde.
* `IDEMPOTENCY_CONFLICT`: Idempotency-Key já usado (retornar resultado anterior se aplicável).

**Campo `retry_after`**: **MAY** estar presente (segundos) para indicar quando retentar.

---

## Regras de mercado (baseline)

1. **Não vender dado cru** por padrão; vender **execução/atestado**.

2. **Prova antes de preço**: manifestos, selos, Merkle e TID sempre verificados.

3. **Transparência de preços**: curva pública `price = base + α·items + β·SLA`.

4. **Royalties automáticos** ao titular (default 80/20).

5. **Custódia segregada** (sem co-mingling) + logs e KYC/AML básicos.

6. **Slashing** por fraude (caução + log público de sanções).

7. **Revogabilidade & escopo** definidos no Gênesis (msg #1).

8. **Anti-double-spend** via U-Notes + Spent-Log (msg #3).

9. **Privacidade**: atestados/scores; sem exposição de PII.

10. **Reprodutibilidade**: seeds, versões e hashes fixados.

---

## UBL: partidas dobradas canônicas

**Plano de contas mínimo:**

* **Caixa** (ativo)
* **Receita Diferida** (passivo)
* **Receita de Verificação** (receita)
* **Royalty a Pagar** (passivo)
* **Custos** (despesa)
* **Impostos** (passivo/despesa)

**Moeda base:** **MUST** usar **ISO-4217** (ex.: `EUR`, `USD`, `BRL`).

**Campo `tax_regime`:** **MUST** estar presente em cada lançamento (ex.: `"BR"`, `"EU"`, `"US"`).

**Partidas:**

* **Quote pago (pré-execução)**

  D **Caixa** (+) / C **Receita Diferida** (+)

* **Execução concluída**

  D **Receita Diferida** (−) / C **Receita de Verificação** (+)

* **Royalty do titular**

  D **Receita de Verificação** (−x%) / C **Royalty a Pagar** (+x%)

* **Pagamento de royalty**

  D **Royalty a Pagar** (−) / C **Caixa** (−)

* **Custos/Impostos** conforme regime.

> Cada lançamento referencia: `attestation_id`, `manifest_id`, `unote_txid`, `epoch_root`, `capsule_b3`, `currency` (ISO-4217), `tax_regime`.

---

## SLA e SLO

* **/verify** p95 ≤ 1s (cápsula ≤ 50MB, CPU).

* **/attest** (CPU A/C/R) p95 ≤ 30s/100 itens.

* **/redeem** p95 ≤ 24h (SLA padrão).

* **Reexecução**: **MUST** reexecutar **grátis** quando falhar `signature/merkle/seed mismatch`.

---

## Pricing (padrão inicial)

```
price_eur = base + α·items + β·SLA_factor

defaults: base=€15, α=€0.05, β=€10 (SLA 24h)
```

* **GPU (V(T))**: extra por pack (ex.: +€20/512).

* **Descontos** por volume e janela flexível (SLA > 24h).

---

## Anti-fraude e disputas

* **Spent-Log** impede gastos duplos de U-Notes.

* **Logs públicos de sanções** + **caução** do custodiante.

* **Disputa**: janela curta, mediação → arbitragem técnica (hashes/provas decidem).

---

## Decisões firmes vs pendentes

**Firmes:** quatro endpoints, contabilidade UBL (plano de contas, ISO-4217, tax_regime), royalties, não-venda de dados, anti-double-spend, autenticação (API Key + assinatura), idempotency key, schema de erros, reexecução grátis em caso de falha de signature/merkle/seed.

**Pendentes:** parâmetros finais de preço por domínio, texto jurídico dos contratos (Custódia/SLA/Licença).

---

## Checklist de implementação

* [ ] Publicar **OpenAPI** de `/verify`, `/attest`, `/quote`, `/redeem` (com autenticação e erros).

* [ ] CLIs determinísticos (mesmos contratos de E/S).

* [ ] Integração UBL dos eventos (quote, redeem, royalty) com plano de contas, ISO-4217 e tax_regime.

* [ ] Regras de SLA e reexecução (grátis em caso de falha).

* [ ] Painel com **A/R/C/P/V**, custos e taxa de sucesso.

## Proof of Done

* Um **/quote → /redeem** completo gerando **attestation.issue**, com entradas UBL reconciliadas e `spent_proof="not_spent"`.

* Auditor externo valida `attestation_id ↔ UBL ↔ manifest.lot ↔ capsule_b3` e dá **OK**.

* Reexecução grátis testada em caso de `signature/merkle/seed mismatch`.
