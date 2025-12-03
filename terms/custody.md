# Contrato de Custódia — Diamond Baseline v1

**Partes.** "Titular" (dono da Trajetória/TID) e "Custodiante" (operador do serviço).

## 1) Escopo

* Custódia de **Trajetórias** (TCAPs/manifestos), emissão/gestão de **U-Notes**, execução de **/verify, /attest, /redeem**, e reconciliação **UBL**.

* Não inclui venda de dado cru; o serviço comercializa **execuções/atestados**.

## 2) Propriedade & Direitos

* O Titular mantém **toda a propriedade** da Trajetória.

* O Titular concede ao Custodiante **licença não exclusiva** para processar T **única e exclusivamente** para:

  * (i) verificação/auditoria/score; (ii) geração de atestados; (iii) reconciliação contábil; (iv) segurança/fraude.

* Subprocessadores **MUST** seguir os mesmos controles de segurança (ver SECURITY.md/DATA-POLICY.md).

## 3) Proveniência & Integridade (MUST)

* TCAP/manifestos com `bytes_canon_hash_b3`, assinaturas Ed25519 (`sig_context` correto), Merkle root e, quando aplicável, **Spent-Log**.

* Custodiante **MUST** recusar cargas sem prova válida.

## 4) Controle de Acesso

* Autenticação via `Authorization` + `X-Signature` (Ed25519), `X-Timestamp`, `X-Sig-Context`.

* Registros de acesso **append-only** por 12 meses (mínimo) com hash diário.

## 5) U-Notes & Anti-Double-Spend

* Emissão, split, spend conforme schemas `unote.tx` (com `tx_nonce` 128-bit).

* Submissão em **Spent-Log** (epochs, Merkle). Não-gasto via **GCS/Merkle frontier**.

## 6) Responsabilidades

* **Titular**: (i) legalidade da origem dos dados; (ii) remoção de PII quando exigido; (iii) chaves/rotação.

* **Custodiante**: (i) segurança operacional; (ii) execução dentro do **SLA**; (iii) reexecução nos casos previstos.

## 7) Preços & Royalties

* Preço = público (fórmula `base + α·items + β·SLA`).

* Royalties ao Titular conforme `royalty_split` da **Gênesis**; repasse mensal com extrato UBL.

## 8) Confidencialidade

* Atores concordam com confidencialidade sobre materiais não públicos. Exceções: ordem legal, auditoria independente sob NDA.

## 9) Conformidade

* Operação em conformidade com leis locais (ex.: proteção de dados, consumer law). Pedidos legais devem referenciar **hashes e IDs**.

## 10) Garantias, Responsabilidade & Limites

* Fornecido "**as is**". Sem garantias de adequação específica.

* Limite agregado de responsabilidade do Custodiante: **12 meses de taxas** pagas.

* Exclusões: força maior, dados fornecidos com falsidade ou sem direito.

## 11) Vigência & Término

* Vigente enquanto houver saldo de serviço ou custódia ativa.

* Término com aviso de 30 dias ou por violação material não sanada em 15 dias.

* Na rescisão: export NDJSON canônico + TCAP; deleção segura em até 30 dias (logs retidos conforme lei).

## 12) Auditoria & Disputas

* Auditoria técnica por terceiro independente (com NDA) **MAY** ocorrer 1x/ano.

* Disputas técnicas priorizam **provas criptográficas** e registros UBL.
