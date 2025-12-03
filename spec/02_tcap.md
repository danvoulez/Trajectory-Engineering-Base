# Cápsula TCAP

# O que é

**TCAP** é a cápsula binária selada da trajetória — um arquivo único, **streamável** (abre sem unzip), que carrega: gênesis+cadeia de blocos (append-only), manifesto, índices e selo criptográfico. É o "container" que qualquer corretora consegue **verificar e operar** offline.

# Por que existe (problemas que resolve)

* **Portabilidade real:** um único arquivo leva tudo o que importa; não depende de banco/servidor.

* **Verificação rápida:** abre, verifica assinaturas/merkle e segue direto para execução.

* **Integridade forte:** cadeia `prev_b3` impede edição; selo (DV25-Seal) confirma autoria.

* **Busca O(1):** índice KV permite `seek(span_id)` instantâneo dentro da cápsula.

* **Operação segura:** políticas de escopo e lastro via U-Notes/UBL (na msg #4) referenciadas no manifesto.

# Estrutura do arquivo `.tcap`

```
[ HEADER 8KB ][ MANIFEST_JSONA ][ INDEX_KV ][ BLOCO_0 ][ BLOCO_1 ] ... [ BLOCO_N ]
```

**Limites:**

* Tamanho máximo da cápsula TCAP v1: **50 MB** (52,428,800 bytes).

**HEADER (8KB fixo, little-endian)**

* `magic`: `"TCAPv1\0"` (8 bytes) — **MUST** estar presente.
* `version`: `1` (uint16, little-endian) — **MUST** estar presente.
* `endianness`: `"LE"` (little-endian) — **MUST** ser little-endian.
* `offsets`: `manifest_off` (uint64), `index_off` (uint64), `first_block_off` (uint64) — **MUST** estar presente.
* `caps`: `compression ("none"|"zstd")`, `encryption (true|false)` — **MUST** estar presente.
* `capsule_b3`: BLAKE3 do corpo (para o selo) — **MUST** ser 32 bytes (64 hex chars).
* `header_b3`: BLAKE3 do HEADER (primeiros 8KB) — **MUST** estar presente para detecção de corrupção.
* `sig_context`: `"diamond:tcap:v1"` — **MUST** estar presente (domain separator).
* `seal`: DV25-Seal (assinatura sobre `sig_context || capsule_b3 || header_b3`) — **MUST** estar presente.

**MANIFEST_JSONA**

* Um `manifest.lot` canônico: partições externas (NDJSON/Parquet) **ou** modo *embedded* (a cápsula é a fonte da verdade).
* Inclui `versions` (semver), `sidecars` (Bloom/KV), `merkle.root`, e **refs UBL** (lançamentos/recebíveis).
* **MUST** seguir canonicidade JSON (ver spec #1).

**INDEX_KV**

* Mapa `{span_id → {byte_offset_block, span_type?, height?}}`.
* Permite carregar **só o bloco** necessário (sem varrer tudo).
* **MAY** incluir `span_type` e `height` para filtros rápidos (ex.: pular direto para `attestation.issue`).

**BLOCOS**

* Sequência *length-prefixed* dos **blocks DNA** (`prev_b3`, `payload_b3`, `tid`, `height`, `sig`).
* *Wire format v1:* **JSONL canônico** (padrão para depuração fácil).
* *Wire format v1.1:* **CBOR** (performance mode, **MAY** ser usado).

**Criptografia**

* Se `encryption=true`, **MUST** cifrar apenas os **blocos**.
* **HEADER+MANIFEST MUST** permanecer visíveis (para metadata & roteamento).
* **MUST** usar KMS por tenant para chaves de criptografia.

# Operações principais

* `tcap pack`: empacota HEADER+MANIFEST+INDEX+BLOCOS e sela (`DV25-Seal`).

* `tcap verify`: valida HEADER (incluindo `header_b3`), **seal**, `manifest.lot`, cadeia `prev_b3`.

* `tcap seek <span_id>`: salto direto ao bloco, via INDEX_KV.

* `tcap extract`: stream dos payloads (para analytics/materializações).

# SLOs (alvos)

* **verify p95 ≤ 1s** (cápsula ≤ 50 MB em CPU comum).

* **seek p95 ≤ 5 ms** por `span_id`.

* **throughput ≥ 50 MB/s** em leitura sequencial.

# Segurança e privacidade

* **Imutabilidade forte:** qualquer byte alterado quebra `prev_b3` e o `seal`.

* **Assinatura do todo:** `DV25-Seal` sobre `sig_context || capsule_b3 || header_b3`.

* **Opcional:** compressão `zstd` por bloco; criptografia por tenant (KMS) sem perder verificabilidade do cabeçalho.

* **Sem PII:** o que precisar de vínculo pessoal entra como **hash/atestado** (ver Gênesis).

* **Domain separation:** `sig_context` **MUST** ser usado para evitar replay cross-app.

# Como a corretora usa (caminho feliz)

1. Recebe `.tcap` → `tcap verify` (HEADER+seal+manifest+cadeia).

2. Se necessário, `tcap seek` em spans específicos (Ex.: `attestation.issue`, `unote.tx`).

3. Executa `/verify` e `/attest` (CPU) e, se houver GPU, mede **V(T)**.

4. Emite recibo/relatório e lança UBL (receita/royalties), referenciando a cápsula por `capsule_b3`.

# Interop com as outras mensagens

* **#1 (TID & Gênesis):** os primeiros blocos vivem dentro da TCAP.

* **#3 (U-Notes & Spent-Log):** os `unote.tx` também são blocos; a cápsula referencia `epoch_root`.

* **#4 (Mercado & UBL):** `attestation.issue` e refs contábeis ficam acessíveis via `seek`.

* **#5 (Métricas):** A/R/C/P (e V) podem ser calculados lendo direto da TCAP.

# Decisões firmes vs pendentes

**Firmes:** formato em camadas (HEADER/manifest/index/blocos), `prev_b3`, `DV25-Seal`, INDEX_KV, modo *embedded* ou externo, endianness little-endian, `header_b3`, `sig_context`, JSONL canônico v1, CBOR v1.1, criptografia apenas em blocos, limite 50MB.

**Pendentes:** política de criptografia por tenant (KMS específico), *sharding* para cápsulas > 50MB.

# Checklist de implementação

* [ ] Especificar HEADER e offsets (struct fixa, little-endian).

* [ ] Definir **JSONL canônico** v1 (padrão) e **CBOR** v1.1 (opcional) com regras de ordenação.

* [ ] Implementar `tcap pack/verify/seek/extract` (CLI).

* [ ] Incluir `manifest.lot` + `index_kv` gerados do NDJSON.

* [ ] Gerar `DV25-Seal` sobre `sig_context || capsule_b3 || header_b3` e verificar assinatura.

* [ ] Validar limite de 50MB.

# Proof of Done

* Uma cápsula `.tcap` com 1 gênesis + 2 blocos + `manifest.lot` + `index_kv` que:

  (i) passa `tcap verify OK` (incluindo `header_b3`),

  (ii) responde a `tcap seek <span_id>` em ≤ 5 ms,

  (iii) permite extrair `attestation.issue` e reconciliar no UBL.
