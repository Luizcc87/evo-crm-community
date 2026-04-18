# Docs Local

Pasta para documentacao local do fork.

## Convencao

- Use esta pasta para guias, decisoes e notas que pertencem ao seu fork.
- Documentos do upstream devem permanecer fora daqui ou ser mantidos como referencia, nunca como fonte principal da sua customizacao.
- Exemplo de arquivos:
  - `README-OPERACOES.md`
  - `fluxo-fork.md`
  - `padroes-local.md`

## Regra pratica

- `upstream`: documentacao oficial ou espelho da origem.
- `local`: documentacao criada para suas operacoes e customizacoes.

## Convencao de nomes

- `*.upstream.*` para arquivos que espelham a origem oficial sem modificacoes locais.
- `*.local.*` para arquivos com customizacoes, ajustes ou overlays seus.
- Se o arquivo for derivado do upstream, mantenha o nome original e acrescente o sufixo apropriado.

## Referencia

Consulte [padroes-local.md](./padroes-local.md) para a regra de decisao entre `upstream`, `local` e overlay.
