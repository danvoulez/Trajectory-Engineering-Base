# Contributing

## Filosofia

* **Compatibilidade primeiro:** mudanças que quebram contrato = MAJOR.
* **Determinismo acima de tudo:** nada entra sem canonicidade e hashes reprodutíveis.

## Fluxo

1. Abra uma Issue descrevendo o problema, não a solução.
2. Proponha PR com mudanças mínimas + CHANGELOG e schema_version/pipeline_version atualizados.
3. Inclua exemplos e comandos de verificação local (Makefile).

## Regras

* Não adicionar dependências de CI neste repo (preferência: CLI-only).
* Tests locais **MUST** passar (`make check`).
* Evite bikeshedding: nomes e enums curtos e estáveis.
