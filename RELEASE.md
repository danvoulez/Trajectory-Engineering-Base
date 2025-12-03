# Release Process (local, sem CI)

## Freeze

1. Atualizar `schema_version`/`pipeline_version`/`CHANGELOG.md`.
2. **Check local:** `make check` (validação de schemas + exemplos + lint do OpenAPI).
3. **Tag:** `git tag v1.0.0 && git push --tags`

## Artifacts

* **Zip do repo:** `git archive -o diamond-v1.0.0.zip HEAD`
* **BLAKE3:** `b3sum diamond-v1.0.0.zip > diamond-v1.0.0.zip.b3`
* **Release notes:** colar itens do CHANGELOG (resumo objetivo).
