# Versionamento (semver)

## Schemas

`schema_version` = MAJOR.MINOR.PATCH

* **MAJOR:** quebra de campos/semântica.
* **MINOR:** novo campo opcional; sem quebra.
* **PATCH:** fix de texto/descrição.

## Pipeline

`pipeline_version` acompanha mudanças de tooling/enzimas/test harness.

## Suites

`auditset@x.y.z`, `evalsuite@x.y.z` — mudar seed/prompt ⇒ bump MINOR; mudar métrica ⇒ MAJOR.
