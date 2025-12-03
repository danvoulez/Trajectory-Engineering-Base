# SECURITY.md — Responsible Security Policy

## ⚑ Escopo

Este documento cobre schemas, OpenAPI, CLIs e exemplos do repositório "Diamond Baseline v1". Serviços operados por terceiros (custodiantes/corretoras) devem publicar políticas próprias.

## 📬 Como reportar

Envie um e-mail para security@logline.world (ajuste para o seu domínio).

**Assunto:** `[SECURITY] <título curto>`

**Inclua:** passos de reprodução, impacto estimado, versão/commit, POC (se possível), e sugestões de mitigação.

**Criptografia opcional:** PGP pubkey.asc (adicione no repo) • fingerprint: XXXX XXXX XXXX XXXX XXXX XXXX XXXX XXXX XXXX XXXX.

## ⏱️ SLAs de resposta

* **Ack:** 72h úteis
* **Avaliação:** 7 dias corridos
* **Correção/mitigação:** alvo de 30 dias (casos críticos prioridade máxima)

Se precisarmos de mais tempo, atualizaremos você a cada 14 dias.

## 🛡️ Safe Harbor

Pesquisas realizadas de forma boa-fé e sem exploração de dados de terceiros não serão objeto de ação legal. Evite:

* Acesso não autorizado a dados pessoais
* DDoS ou degradação do serviço
* Engenharia social contra usuários/operadores
* Uso de credenciais reais

## 🧪 Escopo técnico

Vulnerabilidades em:

* Validação e canonicalização JSON (bytes_canon_hash_b3)
* Assinaturas (Ed25519; sig_context/domain separation)
* Spent-Log / U-Notes (anti-double-spend, tx_nonce)
* Manifests/Merkle (provas de integridade/cobertura)
* OpenAPI (auth, idempotência, erros estáveis)

**Fora de escopo:** typos, mensagens genéricas de erro, relatórios automatizados sem exploração demonstrável.

## 🧮 Severidade

Seguimos CVSS v3.1:

* **Crítico:** CVSS ≥ 9.0
* **Alto:** 7.0–8.9
* **Médio:** 4.0–6.9
* **Baixo:** ≤ 3.9

## 🔐 Divulgação coordenada

Publicamos advisory após correção/mitigação ou 90 dias do reporte (o que ocorrer primeiro), salvo acordo diferente.

Créditos ao pesquisador (se desejar) na seção "Acknowledgments".

## 💰 Bounty

Sem programa de recompensa ativo neste repositório base. Custodiantes podem ter políticas próprias.

## 📦 Versões afetadas

Reportes devem referenciar tag/commit e schema_version/pipeline_version quando aplicável.

## 📄 Contato alternativo

Se o e-mail principal falhar, crie um issue com o título "SECURITY: please provide contact" (sem detalhes sensíveis). Entraremos em contato por canal reservado.

