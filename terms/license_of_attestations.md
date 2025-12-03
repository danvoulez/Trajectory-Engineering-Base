# Licença de Uso — Atestados (`attestation.issue`)

## 1) Objeto

* A licença cobre **artefatos de atestação** (JSON `attestation.issue`) gerados pelo operador.

## 2) Propriedade & Licença

* O **conteúdo factual** dos atestados é do Titular/Custodiante conforme contrato; o **artefato** é licenciado sob os termos abaixo.

* Concessão ao **Comprador/Usuário**: licença **não exclusiva, mundial, irrevogável** para:

  * (i) usar internamente; (ii) redistribuir **inalterado**; (iii) citar resultados com **atribuição**.

* É **PROIBIDO**:

  * remover/alterar `bytes_canon_hash_b3`, `signature_ed25519`, `sig_context`;

  * falsificar, truncar ou remixar atestados mantendo os mesmos IDs/hashes;

  * usar marcas/nome comercial do operador como endosso.

## 3) Atribuição

* Ao redistribuir, **MUST** incluir: "Atestado emitido por <Operador>, hash <BLAKE3>".

## 4) Comercialização

* Reuso comercial é permitido; **revenda em larga escala** do mesmo artefato **MAY** exigir acordo de revendedor.

* Royalties ao Titular conforme `royalty_split` (aplicável quando o atestado for parte de `/redeem`).

## 5) Garantias & Limitação

* Fornecido "**as is**", sem garantia de adequação a propósito específico.

* Sem responsabilidade por usos fora do escopo técnico definido na spec.

## 6) Revogação técnica

* Se um atestado for comprometido (ex.: chave comprometida), o Operador **MAY** publicar **lista de revogação** (CRL) com hash e data. Reemissão **SHOULD** ser oferecida.
