# TBAC v1 — Trajectory Batch Aggregation Capsule

## O que é

**TBAC** é um formato para agregar múltiplas trajetórias TCAP em batches mensais, permitindo distribuição confiável, verificação barata via Merkle trees e encadeamento temporal para auditoria all-time.

## Por que existe

* **Distribuição confiável:** batches ≤8MB bruto (≤2MB gzip) com ≤50k entries por capsula.
* **Verificação barata:** Merkle trees permitem verificar inclusão sem baixar tudo.
* **Encadeamento mensal:** ROOT de cada mês referencia o anterior → cadeia all-time.
* **Compute-to-data:** compatível com políticas "derived-only" (não expõe dados crus).
* **Sharding:** múltiplas capsulas por mês se necessário (shard_id).

## Limites (v1)

* **Tamanho bruto:** ≤8MB por capsula TBAC.
* **Tamanho comprimido:** ≤2MB gzip por capsula TBAC.
* **Entries:** ≤50,000 trajetórias por capsula.
* **Sharding:** **MAY** usar múltiplas capsulas por mês (identificadas por `shard_id`).

## Estrutura

```json
{
  "span_type": "tbac.batch",
  "schema_version": "1.0.0",
  "period": "2025-12",
  "shard_id": 0,
  "entries": [
    {
      "tid": "did:diamond:...",
      "capsule_b3": "<hex64>",
      "manifest_b3": "<hex64>",
      "metrics": { "A": 0.81, "R": 1.58, "C": 0.73, "P": 1.0 }
    }
  ],
  "merkle": {
    "algorithm": "blake2s" | "sha256" | "blake3",
    "root": "<hex>",
    "tree_depth": 16
  },
  "prev_root": "<hex>",
  "bytes_canon_hash_b3": "<hex64>",
  "signature_ed25519": "<hex>",
  "sig_context": "diamond:tbac:v1"
}
```

## Campos obrigatórios

* `span_type`: **MUST** ser `"tbac.batch"`.
* `schema_version`: **MUST** seguir semver (ex.: `"1.0.0"`).
* `period`: **MUST** ser formato `YYYY-MM` (ex.: `"2025-12"`).
* `shard_id`: **MUST** ser inteiro ≥0 (0 se não houver sharding).
* `entries`: **MUST** ser array de objetos com `tid`, `capsule_b3`, `manifest_b3`, `metrics`.
* `merkle`: **MUST** conter `algorithm`, `root`, `tree_depth`.
* `prev_root`: **MUST** estar presente (hash do ROOT do mês anterior, ou `null` se primeiro mês).
* `bytes_canon_hash_b3`: **MUST** ser BLAKE3 do JSON canônico.
* `signature_ed25519`: **MUST** ser assinatura sobre `sig_context || bytes_canon_hash_b3`.
* `sig_context`: **MUST** ser `"diamond:tbac:v1"`.

## Merkle Tree

**Algoritmos suportados:**

* `blake2s`: padrão (32 bytes, rápido).
* `sha256`: alternativo (32 bytes, amplamente suportado).
* `blake3`: opcional (32 bytes, mais rápido, mas menos comum).

**Construção:**

1. Cada entry **MUST** ser serializado canonicamente.
2. Hash de cada entry usando o algoritmo escolhido.
3. Construir árvore binária (bottom-up).
4. Root **MUST** ser o hash do nó raiz.

**Verificação:**

* **MUST** poder verificar inclusão de uma entry sem baixar toda a capsula.
* **MUST** fornecer proof path (hashes dos irmãos até a raiz).

## Encadeamento ROOT

**Regra:**

* `prev_root` do mês N referencia o `merkle.root` do mês N-1.
* Primeiro mês: `prev_root = null`.
* Cria cadeia all-time: `ROOT_2025-01 → ROOT_2025-02 → ... → ROOT_2025-12`.

**Uso:**

* Permite verificar que nenhum mês foi omitido ou alterado.
* Auditoria temporal completa.

## Sharding

**Quando usar:**

* Se entries > 50k ou tamanho > 8MB bruto, **MUST** dividir em múltiplas capsulas.
* Cada shard **MUST** ter `shard_id` único (0, 1, 2, ...).

**Regras:**

* Todos os shards do mesmo período **MUST** ter mesmo `period` e `prev_root`.
* **MUST** poder reconstruir o ROOT completo combinando todos os shards.

## Compatibilidade

**Compute-to-data:**

* TBAC **MAY** conter apenas `capsule_b3` e `manifest_b3` (hashes).
* Dados crus **MUST NOT** estar presentes (policy "derived-only").
* Verificação **MUST** funcionar apenas com hashes.

**Policy "derived-only":**

* TBAC **MUST** poder ser gerado sem acesso aos dados crus das trajetórias.
* Apenas `capsule_b3`, `manifest_b3` e `metrics` agregadas são necessárias.

## Verificação

**Passos:**

1. Validar JSON Schema.
2. Verificar `bytes_canon_hash_b3` (canonicalização).
3. Verificar `signature_ed25519` (sig_context || bytes_canon_hash_b3).
4. Verificar Merkle tree (reconstruir e comparar root).
5. Verificar encadeamento (prev_root bate com mês anterior).

**Ferramenta:**

* `tools/verify_tbac.py` — verificador completo.

## Geração mensal

**Processo:**

1. Coletar todos os `manifest.lot` do mês (de TCAPs verificados).
2. Extrair `tid`, `capsule_b3`, `manifest_b3`, `metrics` (de `attestation.issue`).
3. Construir Merkle tree.
4. Calcular `prev_root` (do TBAC do mês anterior).
5. Canonicalizar e assinar.

**Ferramenta:**

* `tools/generate_tbac.py` — gerador (próximo passo).

## Integração com Spent-Log

**Próximos passos:**

* Spent-Log v0 **MAY** referenciar `tbac_root` para vincular economics → agregados.
* IDs de TBAC **MAY** ser usados em `mint/reserve/consume` operations.

## Checklist de implementação

* [x] Especificação TBAC v1 (este documento).
* [x] JSON Schema (`schemas/tbac.schema.json`).
* [x] Verificador Merkle (`tools/verify_tbac.py`).
* [ ] Gerador mensal (`tools/generate_tbac.py`).
* [ ] Integração Spent-Log v0.
* [ ] Adicionar `tbac_root` nos certificados.

## Proof of Done

* Uma capsula TBAC v1 com:
  (i) ≤50k entries, ≤8MB bruto, ≤2MB gzip,
  (ii) Merkle tree verificável (blake2s/sha256/blake3),
  (iii) `prev_root` encadeado corretamente,
  (iv) assinatura válida,
  (v) passa `verify_tbac.py` com sucesso.

