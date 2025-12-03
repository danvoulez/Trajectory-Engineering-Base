.PHONY: check schemas openapi examples

SCHEMAS_DIR=schemas
EXAMPLES_DIR=examples

check: schemas openapi examples
	@echo "✓ all checks passed (local)"

schemas:
	@echo "→ validate schemas (jsonlint only)"; \
	for f in $(SCHEMAS_DIR)/*.json; do \
		python3 -m json.tool $$f > /dev/null || exit 1; \
	done

openapi:
	@echo "→ lint OpenAPI (syntax only)"; \
	python3 scripts/validate_openapi.py

examples:
	@echo "→ validate example JSON syntax"; \
	for f in $(EXAMPLES_DIR)/*.json; do \
		python3 -m json.tool $$f > /dev/null || exit 1; \
	done

