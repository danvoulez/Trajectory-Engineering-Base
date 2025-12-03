# Rotação de Chaves — Trajectory

## Span trajectory.keyrotate (resumo)

* `old_pubkey`, `new_pubkey`
* `sig_old_on_new`, `sig_new_on_old`
* `effective_after` (ISO-8601Z) — quarentena opcional
* `reason` (enum curto)

## Regra

**MUST** aceitar ambas as chaves durante a quarentena.

**Auditoria:** manter trilha em manifest da trajetória (capsule index).

