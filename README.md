# Diamond Baseline v1 — JSON✯Atomic, CLIs & OpenAPI

"Chat & diamonds are forever." Este repositório fixa o baseline v1 do padrão Diamante:

* Schemas JSON✯Atomic (provas, proveniência e execução),
* OpenAPI para /quote, /redeem, /verify, /attest,
* CLIs determinísticos para TCAP, U-Notes e Spent-Log,
* Exemplos canônicos prontos para teste.

## Estrutura

```
/spec          # Especificações técnicas (5 mensagens-âncora)
/schemas       # JSON Schemas canônicos (semver)
/examples      # payloads mínimos e reprodutíveis
/cli           # especificação das interfaces de linha de comando
/openapi       # diamond.yaml — OpenAPI 3.1 (serviços de mercado)
/terms         # Contratos padrão (Custódia, SLA, Licença)
/LICENSES      # LICENSE-CODE (MIT) & LICENSE-SPEC (CC-BY-4.0)
TERMS.md       # Termos de uso (baseline)
```

## Versões & Compatibilidade

**Semver em tudo:** schema_version, pipeline_version, suites (auditset@x.y.z, evalsuite@x.y.z).

Mudanças quebra-contrato ⇒ MAJOR. Campos novos opcionais ⇒ MINOR.

## Invariantes (MUST)

* **Canonicalização JSON** antes de bytes_canon_hash_b3: ordem lexicográfica de chaves, UTF-8, floats com precisão fixa, sem espaços supérfluos.

* **Assinaturas Ed25519** com sig_context (separação de domínio).

* **Limites:** bloco ≤ 1MB; TCAP v1 ≤ 50MB (ajustável por release).

* **Sem venda de dado cru** por padrão — comercializa-se execuções/atestados.

## Quickstart

* **Schemas:** valide payloads com qualquer validador draft-07.

* **OpenAPI:** importe `openapi/diamond.yaml` no seu gateway/ferramenta favorita.

* **CLIs:** siga `/cli/CLIs.md` para empacotar TCAP, emitir/gastar U-Notes e consultar Spent-Log.

* **Exemplos:** copie de `/examples` e ajuste campos (DID, hashes, timestamps).

## Métricas Diamante (v3.1)

Diamante ⇔ `A ≥ 0.70 ∧ R ≥ 1.50 ∧ V_LB95 ≥ 0.30 ∧ C ≥ 0.70 ∧ P ≥ 0.50`

Score = `A × R × V × C × P` (ranking, não certifica sozinho).

## Segurança & Relato

Leia `SECURITY.md` para responsible disclosure.

Não publique PII em manifests/cápsulas.

## Licenças

* **Código:** MIT (`LICENSES/LICENSE-CODE`)
* **Especificações & docs:** CC-BY-4.0 (`LICENSES/LICENSE-SPEC`)

## Contato

LogLine • suporte/logline.world (atualize conforme seu domínio)
