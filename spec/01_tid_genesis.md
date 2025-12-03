# TID e Bloco Gênesis

# O que é

O **TID (Trajectory ID)** é a placa de carro da trajetória. Ele amarra a identidade criptográfica do titular ao **primeiro bloco** (gênesis) e cria o ponto de partida para uma cadeia **append-only** tipo DNA. A partir daí, cada novo bloco carrega a história, sem reescrever o passado.

# Por que existe (problemas que resolve)

* **Unicidade & lastro:** um ID que não depende de servidor e comprova "é desta pessoa/ente".

* **Anti-double-spend de identidade:** não dá pra "clonar" a trajetória em 3 lugares e dizer que cada uma é a original.

* **Privacidade com prova:** vínculo a documentos/atestados **sem expor PII** (só hashes/assinaturas).

* **Portabilidade:** qualquer corretora/validador consegue verificar **offline**.

* **Compatível com dinheiro-like:** a cadeia permite emitir "direitos de uso" (U-Notes) sem ambiguidade.

# Forma canônica do TID

**Formato regex:**

```
^did:diamond:[a-f0-9]{64}\.[a-f0-9]{64}(:v[0-9]+)?$
```

**Estrutura:**

```
tid = did:diamond:<pkhash>.<genesis_b3>[:v1]
```

* **pkhash** = BLAKE3(pubkey_ed25519 do titular ou círculo) — **MUST** ser 64 caracteres hex.

* **genesis_b3** = BLAKE3 do **bloco gênesis canônico** — **MUST** ser 64 caracteres hex.

* `:v1` versiona o esquema (pra futuras revisões) — **MAY** ser omitido (default v1).

➡️ Resultado: se a chave muda ou o gênesis muda, o TID muda — logo, **não há como forjar** a mesma trajetória com outro conteúdo.

# Canonicidade JSON

Para calcular `bytes_canon_hash_b3`, o JSON **MUST** seguir estas regras:

1. **Ordem de chaves:** alfabética (ordem lexicográfica UTF-8).
2. **Floats:** **MUST** usar notação científica ou decimal fixa; sem trailing zeros; `NaN`/`Infinity` **MUST NOT** ser usados.
3. **UTF-8:** **MUST** ser válido UTF-8; sem BOM.
4. **Espaços:** sem espaços extras; um único espaço após `:` e `,`.
5. **Encoding:** **MUST** ser UTF-8 sem BOM.

**Exemplo de hash canônico:**

```
bytes_canon_hash_b3 = BLAKE3(JSON_canonical(objeto))
```

# Bloco Gênesis (o "bloco #0")

Contém o mínimo necessário para **lastrear** a trajetória sem vazar dados sensíveis.

**Campos essenciais:**

* `span_type: "trajectory.genesis"` — **MUST** estar presente.
* `schema_version`: **MUST** seguir semver (ex.: `"1.0.0"`).
* `pipeline_version`: **MUST** seguir formato `YYYY.MM.DD` (ex.: `"2025.12.03"`).
* `tid`: o TID calculado acima — **MUST** ser calculado após canonicalização.
* `genesis_b3`: **MUST** ser o hash BLAKE3 do bloco gênesis canônico (usado no TID).
* `pubkey_ed25519`: chave pública do titular — **MUST** ser hex de 64 caracteres.
* `owner_id`: **MUST** ser `did:key:...` ou `did:web:...` (máximo 256 caracteres).
* `tenant_id`: **MAY** estar presente para multi-tenancy (formato igual a `owner_id`).
* `intent`: escopo ("audit/score/train?"), `royalty_split` (ex.: 80/20), `revocable: true|false` — **MUST** estar presente.
* `personhood_claims`: **hashes/atestados** (ex.: `gov_doc_hash`, `humanity_attest`), nunca o documento cru — **MAY** estar presente.
* `created_at`: ISO-8601Z — **MUST** estar presente.
* `sig_context`: **MUST** ser `"diamond:genesis:v1"` (domain separator para Ed25519).
* `bytes_canon_hash_b3`: **MUST** ser o hash canônico do objeto (antes da assinatura).
* `signature_ed25519`: **MUST** ser assinatura sobre `sig_context || bytes_canon_hash_b3`.

**Limites:**

* Tamanho máximo do bloco gênesis: **1 MB** (1,048,576 bytes).
* `owner_id`/`tenant_id`: máximo **256 caracteres**.
* `personhood_claims`: máximo **100 itens**.

**Por que assim?**

* Vínculo forte com **pessoa/ente** sem guardar PII.
* Regras econômicas/legais **desde a origem** (royalties, escopo, revogação).

# Cadeia tipo DNA (blocos n>0)

Cada bloco aponta para o anterior:

```
prev_b3 = BLAKE3(block_{n-1})
payload_b3 = BLAKE3(payload JSON✯Atomic)
sig_context = "diamond:block:v1"
sig = ed25519_sign(sig_context || payload_b3 || prev_b3 || tid || height)
```

* **Imutável:** mexeu em 1 byte, quebra a cadeia.
* **Pegada global:** o hash do último bloco resume toda a história.

**Limites:**

* Tamanho máximo por bloco: **1 MB** (1,048,576 bytes).

**Payloads típicos:** `ingest.raw`, `enzyme.apply`, `genetics.spawn`, `manifest.lot`, `audit.run`, `attestation.issue`, `unote.tx` (todos **JSON✯Atomic**).

# Rotação de chave

**Bloco `trajectory.keyrotate`:**

```json
{
  "span_type": "trajectory.keyrotate",
  "schema_version": "1.0.0",
  "tid": "did:diamond:...",
  "old_pubkey_ed25519": "<hex>",
  "new_pubkey_ed25519": "<hex>",
  "old_sig": "<hex>",  // old_pubkey assina new_pubkey
  "new_sig": "<hex>",  // new_pubkey assina old_pubkey (co-assinatura)
  "quarantine_until": "ISO-8601Z",  // MAY estar presente
  "sig_context": "diamond:keyrotate:v1",
  "bytes_canon_hash_b3": "<hex>",
  "signature_ed25519": "<hex>"  // new_pubkey assina o bloco
}
```

**Regras:**

* **MUST** ter co-assinatura: `old_pubkey` assina `new_pubkey` e vice-versa.
* **MAY** ter período de quarentena (`quarantine_until`): durante este período, blocos **MUST** ser assinados por ambas as chaves.
* Após quarentena, apenas `new_pubkey` **MUST** assinar novos blocos.

# Privacidade & prova (sem PII)

* **Personhood**: só **hash** do documento e assinatura do emissor (quem atesta), nunca o documento.
* **Verificação**: qualquer parte checa se o hash bate e se a assinatura do emissor é válida.
* **Rotas de confiança**: você pode ter múltiplos atestados (governo, instituição, web-of-trust).

# Ciclo de vida (o que pode acontecer e como provar)

1. **Criar**: gerar chave → montar gênesis → calcular `tid` → assinar.
2. **Adicionar**: anexar blocos (append-only).
3. **Rotacionar chave**: bloco `trajectory.keyrotate` coassinado (antiga + nova) — ver seção acima.
4. **Delegar custódia**: incluir custodiante (multisig ou mandato explícito).
5. **Revogar escopo**: se `revocable=true`, registrar `trajectory.revoke_scope`.
6. **Encerrar**: `trajectory.close` (não impede leitura, mas marca final oficial).

# Ameaças & mitigação

* **Clone malicioso**: sem a **chave privada** do titular, o atacante não consegue assinar blocos válidos.
* **TID "colado" com outro gênesis**: muda o `genesis_b3` → **muda o TID**.
* **Perda de chave**: política no gênesis ("custodiante de recuperação"/multisig).
* **Colisão de identidade**: requer colidir BLAKE3 + ED25519 + cadeia — computacionalmente impraticável.
* **Replay cross-app**: `sig_context` **MUST** ser usado para separar domínios.

# Como "funciona como dinheiro"

* O TID é o **ativo-raiz**; a cadeia é o **livro-razão local**.
* Sobre ele, você emite **U-Notes** (direitos de uso) com **conservação** e **spent-log** → impede "gastar duas vezes".
* A trajetória viaja como **cápsula TCAP** selada (streamável), que qualquer corretora abre e verifica.

# Interop com UBL e TCAP (ponte com as próximas mensagens)

* **UBL**: registra **receita, royalty, caução, impostos** de tudo que envolver a trajetória — auditor entende.
* **TCAP**: empacota o gênesis + cadeia + índices + manifest em um binário **verificável sem unzip**.

# Decisões já firmes vs pendentes

**Firmes:** forma do TID (regex acima), gênesis sem PII, cadeia com `prev_b3`, payloads JSON✯Atomic, canonicidade JSON, `sig_context`, limites de tamanho, rotação de chave com co-assinatura.

**Pendentes:** política de `personhood_claims` (quais atestados mínimos), formato exato de multisig/recuperação, e quais campos do `intent` serão obrigatórios.

# Checklist de implementação

* [ ] Gerar par de chaves ed25519 do titular/ente.
* [ ] Montar `trajectory.genesis` canônico (ordem alfabética, UTF-8) e calcular `genesis_b3`.
* [ ] Calcular `tid = did:diamond:<pkhash>.<genesis_b3>:v1` (validar regex).
* [ ] Assinar com `sig_context = "diamond:genesis:v1"`.
* [ ] Publicar gênesis + primeiro `manifest.lot`.
* [ ] Testar encadeamento com 2 blocos e `tcap verify`.
* [ ] Documentar política de rotação/recuperação/escopo.

# Proof of Done

* Um arquivo `genesis.span.jsona` assinado + o `tid` calculado (validado por regex), e **dois blocos** subsequentes verificados (hash e assinatura) com `tcap verify OK`.

# Exemplo (toy)

* `pubkey_ed25519 = 0xABCD…` (64 hex chars)
* `genesis_b3 = b3(trajectory.genesis) = 6f2c…` (64 hex chars)
* `tid = did:diamond: b3(pubkey) . 6f2c… :v1` (valida regex)
* Primeiro bloco: `prev_b3 = genesis_b3`; `payload = ingest.raw`; assinatura sobre `("diamond:block:v1" || payload_b3 || prev_b3 || tid || height=1)`.
* Segundo bloco: `prev_b3 = b3(bloco_1)`; `payload = manifest.lot`; assinar e anexar.

> Resultado: você tem **um ID único** que "segue" a pessoa/ente, uma cadeia que **não regride** e um caminho limpo para transformar trajetória em **ativo com lastro**.
