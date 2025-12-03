.PHONY: check schemas openapi examples

SCHEMAS_DIR=schemas
EXAMPLES_DIR=examples

check: schemas openapi examples
	@echo "✓ all checks passed (local)"

schemas:
	@echo "→ validate schemas (jsonlint only)"; \
	for f in $(SCHEMAS_DIR)/*.json; do \
		python -m json.tool $$f > /dev/null || exit 1; \
	done

openapi:
	@echo "→ lint OpenAPI (syntax only)"; \
	python - <<'PY' || exit 1; \
	import sys, yaml; \
	with open('openapi/diamond.yaml','r',encoding='utf-8') as f: \
		yaml.safe_load(f); \
	print('openapi ok'); \
	PY

examples:
	@echo "→ validate example JSON syntax"; \
	for f in $(EXAMPLES_DIR)/*.json; do \
		python -m json.tool $$f > /dev/null || exit 1; \
	done

