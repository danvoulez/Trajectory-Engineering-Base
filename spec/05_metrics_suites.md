# Diamante

# O que é

Este é o "régua e compasso" do Diamante: define **como medir** Autenticidade, Robustez, Valor Intrínseco, Capacidade de Auditoria e Proveniência — e **quando** um ativo passa a ser **Diamante**.

## Definição (v3.1)

Diamante ⇔ `A ≥ 0.70 ∧ R ≥ 1.50 ∧ V_LB95 ≥ 0.30 ∧ C ≥ 0.70 ∧ P ≥ 0.50`

Score = `A × R × V × C × P` (usado para ranking, não para certificar sozinho).

---

# Por que existe (problemas que resolve)

* **Tira da opinião e leva ao teste:** "valor intrínseco" = ganho medido em suite selada.

* **Evita gamificação barata:** média geométrica e testes adversariais punem atalho.

* **Permite auditoria de terceiros:** qualquer parte replica as métricas com seeds, hashes e versões.

---

# A(T) — Autenticidade (0–1)

**O que mede:** traços humanos e consistência estrutural da trajetória.

**Cálculo:** média geométrica **(GM)** das sub-dimensões, com clipping ε=1e-6.

```
A = GM( V_temporal, V_contextual, V_causal, V_esforço, V_u-chaos )
```

**Normalização dos subscores (per-domain min-max, recalibrado trimestralmente):**

Cada `V_*` **MUST** ser normalizado para [0,1] usando:

1. **Min-max por domínio:** `V_norm = (V_raw - V_min_domain) / (V_max_domain - V_min_domain)`
2. **Recalibração trimestral:** limites `V_min_domain` e `V_max_domain` **MUST** ser recalculados a cada trimestre com base em corpus de referência.
3. **Clipping:** valores fora de [0,1] **MUST** ser clippados (ε=1e-6).

**Sinais típicos**

* **Temporal:** ritmo humano, latência entre eventos, jitter plausível.

* **Contextual:** coesão intra-sessão, progressão por objetivos.

* **Causal:** cadeia de implicações sem "saltos mágicos".

* **Esforço:** correções, tentativas, refatorações — custo cognitivo.

* **u-chaos:** entropia/ruído ambiental "na medida" (nem esterilizado, nem caótico demais).

**Boas práticas**

* Enzimas: `segment`, `causal-weave`, `entropy-balance`, `effort-signals`.

* Normalize cada subscore (0–1) e documente o método.

---

# R(T) — Robustez (≥1.0)

**O que mede:** resiliência quando perturbamos a trajetória.

**Cálculo:**

1. Gere variantes `T_δ` (warp temporal, ruído contextual, adversarial leve).

2. `ρ(δ) = A(T_δ) / A(T)`; agregue pela **média harmônica**.

3. `R = 1 + min(1, ρ̄)`  (cap em 2.0)

   **Critério:** `R ≥ 1.50` (mantém ≥50% da autenticidade sob estresse alto).

**Distribuições de perturbação (default perturbation params):**

* **Temporal warp:** `δ ~ U[0.2, 0.4]` (uniforme entre 0.2 e 0.4) — compressão/expansão local.

* **Contextual noise:** proporção de inserções neutras = `0.05 ± 0.02` (5% ± 2% dos eventos).

* **Reorder mínimo:** máximo 3% dos eventos podem ser reordenados (mantendo dependências causais).

* **Adversarial:** instruções contraditórias leves (1–2 por 100 eventos, escolhidas aleatoriamente).

**Perturbações sugeridas**

* **Temporal:** compressão/expansão local (δ ∈ [0.2, 0.4]).

* **Contextual:** inserções neutras, reorder mínimo.

* **Adversarial:** instruções contraditórias leves.

---

# V(T) — Valor Intrínseco (≥0.0)

**O que mede:** **quanto** T melhora um modelo na prática.

**Cálculo:** fine-tune curto (ou rehearsal) em **pack** de T e avalie:

```
V = max(0, (L_pre − L_pos) / L_pre)  // ou ΔAccuracy
```

**Decisão usa IC-95%:** `V_LB95` via bootstrap estratificado.

**Bootstrap:**

* **n_boot = 2000** — **MUST** usar 2000 iterações.

* **Estratificação por domínio** — **MUST** estratificar por domínio para garantir representatividade.

* **IC-95%:** usar limite inferior (LB95) do intervalo de confiança.

**Critério:** `V_LB95 ≥ 0.30` (≥30% de ganho com 95% de confiança).

**Setup prático**

* **Modelo:** Gemma-9B (LoRA curto).

* **Hiperparâmetros (defaults):** r=8, α=16, steps=200, lr=1.5e-4, wd=0.1, batch=8, grad_accum=4.

* **Pack size:** 512 (variar 256–1024 conforme domínio).

* **EvalSuite:** seeds fixos, prompts estáveis, splits selados.

---

# C(T) — Capacidade de Auditoria (0–1)

**O que mede:** se T "verifica" trajetórias similares de forma confiável.

**Cálculo:** Macro-F1 em **AuditSet** (mesmo domínio) para tarefas:

* NLI/entailment de alegações,

* consistência temporal,

* checagem causal básica.

  **Critério:** `C ≥ 0.70`.

---

# P(T) — Proveniência (0 | 0.5 | 1.0)

**O que mede:** lastro e cadeia de custódia.

```
1.0: assinatura + manifest + cobertura Merkle/Seals completa

0.5: assinatura presente, lacunas na cadeia

0.0: sem prova verificável
```

**Critério:** `P ≥ 0.50`.

---

# Suites oficiais

## AuditSet v1 (para C/R/P)

* **Tamanho:** 1k pares por domínio (mínimo).

* **Conteúdo:** casos positivos/negativos balanceados, contraexemplos adversariais leves.

* **Publicação:** NDJSON com hashes; manifest assinado; versão congelada.

* **Versão:** **MUST** seguir semver (ex.: `auditset@1.0.0`).

* **Hash dos prompts:** **MUST** publicar BLAKE3 de cada prompt usado.

* **Seed global:** **MUST** publicar seed global usado para geração/ordenação.

* **Lista de versões:** **MUST** manter changelog público de versões.

## EvalSuite v1 (para V)

* **Tarefas:** NLI/FEVER/QA estruturado, coerência, extrativismo vs geração.

* **Seeds:** fixos; prompts imutáveis; splits por domínio.

* **Relato:** média + IC-95% por métrica; guardar checkpoints e logs.

* **Versão:** **MUST** seguir semver (ex.: `evalsuite@1.0.0`).

* **Hash dos prompts:** **MUST** publicar BLAKE3 de cada prompt usado.

* **Seed global:** **MUST** publicar seed global usado para splits/ordenação.

* **Lista de versões:** **MUST** manter changelog público de versões.

---

# Relatórios e transparência

Cada **attestation.issue** deve conter:

* `metrics`: `{A, R, C, P, V?, V_LB95?}`

* `ic`: intervalos de confiança (ao menos para V).

* `versions`: `{atomic_schema, enzymes, gen_ops, auditset, evalsuite}` (semver)

* `refs`: `manifest_id`, `capsule_b3`, `epoch_root`, `unote_txid` (se houver).

* `receipt`: hash e assinatura.

* `reproducibility`: **MUST** incluir:
  * `random_seed`: seed usado para todas as operações aleatórias.
  * `framework`: framework usado (ex.: `"pytorch@2.1.0"`, `"tensorflow@2.13.0"`).
  * `precision`: precisão numérica (ex.: `"fp16"`, `"bf16"`, `"fp32"`).

**Reprodutibilidade alvo:** ≥99% (mesmo seed/hyper → variação ≤1% da perda).

---

# SLOs de execução (baseline)

* `/verify` (P/integ./Merkle): **p95 ≤ 1s** por cápsula ≤ 50MB (CPU).

* `/attest` (A/C/R): **p95 ≤ 30s** a cada 100 itens (CPU).

* `/redeem` (entrega do atestado): **p95 ≤ 24h** (SLA padrão).

* `V(T)` real: fila GPU, preço separado; packs de 256–1024.

---

# Controles anti-gamificação

* **GM em A:** um subscore baixo derruba o todo.

* **R adversarial:** força estabilidade; proíbe "overfit em A estático".

* **V com IC-95%:** melhora precisa ser **estatisticamente sustentada** (n_boot=2000, estratificado).

* **C por domínio:** sem generalizar indevidamente entre domínios.

* **Proveniência obrigatória:** sem P não tem Diamante.

---

# Governança mínima

* Versões de **AuditSet/EvalSuite** públicas e **imutáveis** (manifest + seals), seguindo semver.

* **Change log** de enzimas e operações genéticas.

* **Depósito de caução** e sanções para custodiais que burlarem provas.

---

# Checklist de implementação

* [ ] Implementar extratores para V_temporal/contextual/causal/esforço/u-chaos com normalização per-domain min-max.

* [ ] Implementar harness de **R** (warp/ruído/adversarial + média harmônica) com distribuições especificadas.

* [ ] Preparar **EvalSuite v1** (seeds, splits) + bootstrap IC-95% para **V** (n_boot=2000, estratificado).

* [ ] Preparar **AuditSet v1** (domínios e pares) para **C** com hash de prompts e seed global.

* [ ] Pipeline de **/attest** gerar `attestation.issue` com métricas + versões (semver) + recibo + reproducibility (random_seed, framework, precision).

* [ ] Painel com U, A, R, V_LB95, C, P, custo/1k itens, taxa de FP.

# Proof of Done

* Um lote que:

  (i) atinge `A≥0.70`, `R≥1.50`, `C≥0.70`, `P≥0.50`;

  (ii) tem **V_LB95 ≥ 0.30** em EvalSuite v1 (n_boot=2000, estratificado);

  (iii) publica **attestation.issue** com hashes, versões (semver), recibo e reproducibility (random_seed, framework, precision);

  (iv) é **reproduzido** por terceiro com variação ≤1% e dá **OK**.
