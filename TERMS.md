# Terms of Use — Diamond Baseline v1

## 1) Escopo

Estes Termos regem o uso dos esquemas JSON✯Atomic, OpenAPI, CLIs e exemplos deste repositório ("Projeto"). Serviços operados por custodiante/corretora são regidos também pelos contratos comerciais específicos (SLA e preço).

## 2) Definições

**Trajetória (T):** conjunto de spans/cápsulas TCAP.

**Atestado:** attestation.issue com métricas A/R/C/P(/V).

**U-Notes:** direitos de uso/execução; anti-double-spend via Spent-Log.

**UBL:** Universal Business Ledger (partidas dobradas do ciclo /quote→/redeem).

**Titular:** dono de T (TID).

**Custodiante:** corretora/operadora dos serviços.

## 3) Propriedade & Licenças

**Código** (CLIs, tooling): licenciado sob MIT (ver LICENSES/LICENSE-CODE).

**Especificações** (schemas, OpenAPI, docs): CC-BY-4.0 (ver LICENSES/LICENSE-SPEC), com attribution para "LogLine Foundation / LogLine".

**Marcas:** nomes e logotipos não são licenciados.

## 4) Dados & Proveniência

O Projeto define formatos e provas; não vende dados crus por padrão. A comercialização é de execuções/atestados.

**Proveniência MUST:** bytes_canon_hash_b3, sig_context, signature_ed25519, manifestos assinados e cobertura Merkle.

**Privacidade** é responsabilidade do operador: remova PII ou use escopos restritos.

## 5) Anti-Double-Spend (U-Notes)

Transações **MUST** conter tx_nonce (128-bit), sig_context e registro em Spent-Log.

Provas de não-gasto **MUST:** GCS ou Merkle frontier. Âncoras públicas são **MAY**.

## 6) UBL & Contabilidade

Toda execução /redeem gera partidas: receita diferida, receita, royalties, custos, impostos. Lançamentos **MUST** referenciar IDs de prova (attestation_id, manifest_id, unote_txid, epoch_root, capsule_b3).

## 7) SLA & Reexecução

/verify p95 ≤ 1s (cápsula ≤ 50MB, CPU); /attest p95 ≤ 30s/100 itens; /redeem SLA padrão 24h.

Falha de integridade/proveniência/seed ⇒ reexecução obrigatória sem custo.

## 8) Limites & Uso Aceitável

TCAP v1 ≤ 50MB por cápsula (padrão). Blocos ≤ 1MB.

Proibido burlar spent-log, falsificar métricas ou remover attribution.

## 9) Royalties & Preços

Royalties ao Titular conforme royalty_split do Gênesis (ex.: 80/20). Preços seguem fórmula pública (base + α·items + β·SLA).

## 10) Garantias & Responsabilidade

O Projeto é fornecido "as is", sem garantias. Nem autores nem mantenedores serão responsáveis por danos indiretos, especiais ou consequenciais.

## 11) Atualizações & Versionamento

Alterações compatíveis → MINOR; quebra → MAJOR. Schemas, suites e CLIs usam semver.

Alterações materiais nos Termos serão registradas no CHANGELOG com data de vigência.

## 12) Lei Aplicável & Disputas

Na ausência de contrato comercial específico, aplica-se a lei do domicílio do operador. Disputas técnicas priorizam provas criptográficas (hashes, assinaturas, logs de execução).

## 13) Contato de Segurança

Relate vulnerabilidades em SECURITY.md (responsible disclosure).

