# U-Notes

# O que é

**U-Notes** são "direitos de uso" emitidos a partir da trajetória (TID). Pensar como **unidades fracionáveis** que autorizam execuções (ex.: auditoria de 512 itens). O **Spent-Log** é o livro de transparência que impede gastar a mesma U-Note duas vezes — o equivalente ao "anti-double-spend".

# Por que existe

* **Dinheiro-like sem confusão:** você não pode usar o mesmo direito em três lugares.

* **Divisão controlada:** transforma 100 → 33/33/34 sem perder lastro.

* **Reconciliação contábil:** cada uso gera rastro direto no **UBL**.

* **Portabilidade:** qualquer corretora valida off-line com prova pública do gasto.

# Estrutura da U-Note

**Identidade**

```
unote_id = BLAKE3( tid || policy_id || serial )
```

* `tid`: Trajectory ID (mensagem #1).

* `policy_id`: identifica a política (ex.: "audit_exec_512_v1").

* `serial`: número sequencial (evita colisão).

**Política (exemplos)**

* `unit`: "audit_exec" | "verify_only" | "train_pack"

* `pack_size`: 512 (itens por execução)

* `expiry`: ISO-8601Z ou `null`

* `split_allowed`: true/false

* `split_min_unit`: granularidade mínima (ex.: 1) — **MUST** estar presente se `split_allowed=true`.

* `expiry_behavior`: "auto-invalidate" | "warn" — **MUST** estar presente se `expiry` não for `null`.

* `fee`: opcional (percentual ou valor fixo)

# Transação U-Note (JSON✯Atomic)

Representa **emissão**, **split/merge** ou **gasto**.

```json
{
  "span_type": "unote.tx",
  "schema_version": "1.0.0",
  "tid": "did:diamond:...",
  "spent_chain_id": "default",
  "tx_nonce": "<hex128>",
  "inputs": [ { "unote_id":"u_A", "amount":100, "sig_owner":"<hex>" } ],
  "outputs":[
    { "unote_id":"u_B", "amount":33 },
    { "unote_id":"u_C", "amount":33 },
    { "unote_id":"u_D", "amount":34 }
  ],
  "policy": { "unit":"audit_exec", "pack_size":512 },
  "fee": 0,
  "timestamp": "ISO-8601Z",
  "sig_issuer": "<hex>",
  "sig_context": "diamond:unote.tx:v1",
  "bytes_canon_hash_b3": "<hex>",
  "signature_ed25519": "<hex>"
}
```

**Campos obrigatórios:**

* `tx_nonce`: **MUST** ser 128-bit (16 bytes, 32 hex chars) — blindagem contra replay cross-epoch.
* `spent_chain_id`: **MUST** estar presente (ex.: `"default"`) — identifica o Spent-Log se houver múltiplos.
* `sig_context`: **MUST** ser `"diamond:unote.tx:v1"` (domain separator).

**Regras de conservação**

* Σ`inputs.amount` = Σ`outputs.amount` + `fee` — **MUST** ser válido.

* **Cada `unote_id` só pode aparecer 1× como *input* globalmente** (verificação no Spent-Log).

# Spent-Log (transparência)

É o **registro público append-only** de transações U-Note consolidadas em **épochs**.

**Ciclo**

1. Corretora recebe uma `unote.tx` → valida assinaturas, saldo e `tx_nonce` (único no epoch).

2. Inclui a transação num **epoch atual**, computa **Merkle root**, assina.

3. Publica: `epoch_id`, `merkle_root`, assinatura, e (opcional) âncora externa.

**Parâmetros de finalidade (defaults):**

* `epoch_duration`: **15 minutos** (default) — **MAY** ser configurável (10/30/60 min).

* `confirmations`: **2 epochs** (default) — **MUST** aguardar 2 epochs para considerar final.

**APIs**

* `POST /spent/submit { tx }` → valida e inclui no epoch atual (retorna `tx_proof`).

* `GET /spent/proof?unote_id=...` → prova de gasto ou não-gasto (inclusão/ausência).

* `GET /spent/epoch/:id` → header do epoch (root, assinatura, janela temporal).

**Prova de não-gasto**

* **MUST** usar **GCS (Golomb-coded sets)** ou **Merkle frontier** para non-membership proofs (mais sólidos que só Bloom).

* **SHOULD** retornar prova verificável de que `unote_id` não está no spent-set.

**Finalidade**

* Uma tx é **final** quando o `epoch_root` correspondente está publicado, assinado e **confirmado** (2 epochs).

# Exemplo: 100 → 33/33/34 (três custodiais)

1. Emissor detém `u_A:100`.

2. Cria `unote.tx` de **split** com saídas `u_B:33`, `u_C:33`, `u_D:34` (com `tx_nonce` único).

3. Publica no Spent-Log (epoch X).

4. Entrega `u_B` para a Corretora 1, `u_C` para a 2, `u_D` para a 3.

5. Cada corretora, ao **gastar**, posta a sua *input* no Spent-Log (epoch Y/Z/…) com `tx_nonce` único.

   Resultado: **ninguém consegue** gastar `u_B` duas vezes — o endpoint `/spent/proof` acusaria duplicidade.

# Como isso conversa com a TCAP e o UBL

* **TCAP (mensagem #2):** as `unote.tx` vivem como **blocos** na cápsula; `attestation.issue` referencia `unote_txid` e `epoch_root`.

* **UBL (mensagem #4):** cada gasto gera lançamentos: receita/royalty/custos, com `memo = {unote_txid, epoch_root}` para reconciliação.

# Operações do dia-a-dia

* **Emitir** U-Notes iniciais (suprimento) — `unote.tx` sem inputs, assinada pelo emissor.

* **Split/Merge** conforme necessidade do mercado (respeitando `split_min_unit`).

* **Spend** numa `/redeem`: a corretora coleta a(s) U-Note(s) e submete a tx; só entrega o atestado quando o Spent-Log confirmar **não-gasto prévio**.

* **Revogar** (se política permitir): publicar `unote.tx` de invalidação e contabilizar **compensação** no UBL.

* **Expiry**: se `expiry_behavior="auto-invalidate"` e `expiry` vencer, **MUST** rejeitar em `/spent/submit`.

# Segurança & bordas

* **Reorg/atraso de publicação:** usar épochs curtos (ex.: 15 min default) e fila de pendências; só dar **finalidade** após 2 confirmations.

* **Chave comprometida:** "freeze" via política de revogação definida no gênesis (mensagem #1) + lista de negação no Spent-Log.

* **Replay de tx:** protegido por `tx_nonce` (único no epoch) e inclusão; recusado se *input* já for gasto ou `tx_nonce` duplicado.

* **Caducidade:** se `expiry` vencer, a U-Note vira inválida automaticamente (checado em `/spent/submit` conforme `expiry_behavior`).

# Decisões firmes vs pendentes

**Firmes:** ID da U-Note (hash de `tid||policy||serial`), conservação, Spent-Log com épochs+Merkle, prova de gasto/não-gasto (GCS/Merkle frontier), referências cruzadas com TCAP/UBL, `tx_nonce`, `spent_chain_id`, `sig_context`, `epoch_duration=15min`, `confirmations=2`, `split_min_unit`, `expiry_behavior`.

**Pendentes:** política de taxas (`fee`), política de revogação padrão, e **se haverá âncora pública** (transparency log ou chain).

# Checklist de implementação

* [ ] Esquema `unote.tx` (JSON✯Atomic) com `tx_nonce`, `spent_chain_id`, `sig_context` e verificador de conservação/assinaturas.

* [ ] Spent-Log v0: épochs (15 min), Merkle root, assinatura, endpoints `submit/proof/epoch`, GCS/Merkle frontier para non-membership.

* [ ] Integração `/redeem`: só concluir se `proof(status="not_spent")` e `confirmations >= 2`.

* [ ] Reconciliação UBL: partidas padrão com `unote_txid` no memo.

* [ ] Validação de `expiry` e `split_min_unit`.

# Proof of Done

* Uma emissão → split (100 → 33/33/34) → três gastos separados, **todos** aceitos com `proof="not_spent"` e **contabilizados** no UBL.

* Tentativa de **gasto duplo** rejeitada por `/spent/proof` (ou por inclusão anterior no epoch).

* Tentativa de **replay** (mesmo `tx_nonce`) rejeitada.
