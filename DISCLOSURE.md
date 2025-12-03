# DISCLOSURE.md — Política de Divulgação

## Objetivo

Equilibrar tempo para correção com transparência pública, mantendo os usuários protegidos e incentivando pesquisa responsável.

## Princípios

* **Cooperação:** trabalhamos com pesquisadores para confirmar impacto e priorizar correções.
* **Mínimo necessário:** detalhes técnicos completos após correção, para reduzir risco de exploração.
* **Rastreabilidade:** cada advisory referencia commits, versões e hashes (Merkle/bytes_canon_hash_b3).

## Processo resumido

1. **Recebimento** (via security@...) → ack em até 72h úteis.
2. **Triagem** → classificação CVSS + escopo.
3. **Correção** → patch ou mitigação; versões afetadas documentadas.
4. **Advisory** → publicado aqui e/ou no site do operador com:
   * Título e CVE (se aplicável)
   * Impacto e vetores
   * Versões afetadas
   * Fix/mitigação (commits/tags)
   * Créditos (opt-in)
   * Timeline (recebido/confirmado/corrigido/publicado)

## Linha do tempo padrão

Público em até **90 dias** do reporte inicial, ou antes se:

* Patch estiver disponível e amplamente distribuído; ou
* Exploração ativa confirmada (divulgação acelerada, com mitigação).

## Embargo

Pesquisadores concordam em não divulgar detalhes ou POCs publicamente até:

* o patch/mitigação estar disponível, ou
* o prazo de 90 dias expirar, salvo acordo escrito.

## Créditos

Com consentimento, listamos o(s) pesquisador(es) em "Acknowledgments" do advisory.

## Atualizações

Mudanças nesta política serão versionadas e datadas neste arquivo.

