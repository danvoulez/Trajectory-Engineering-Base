# Política de Dados (baseline)

## Sem dado cru por padrão

Comercializam-se execuções/atestados.

## Minimização

Manifests devem excluir PII; se imprescindível, pseudoanonimize.

## Retenção

Defina janela por domínio (ex.: 12 meses) e publique no serviço.

## Criptografia

Se `encryption=true`, cifrar apenas blocos; header/manifest legíveis.

## Acesso

Todo endpoint requer Authorization + assinatura (X-Signature, X-Timestamp, X-Sig-Context).

## Logs

Manter `attestation_id`, `manifest_id`, `epoch_root`, `unote_txid` (sem conteúdo sensível).

