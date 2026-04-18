# Padroes Locais

Regras praticas para separar arquivos do upstream e customizacoes do fork.

## Quando usar `*.upstream.*`

- Use para espelhar arquivo original do repositorio oficial.
- Mantenha como referencia de comparacao.
- Nao trate este arquivo como fonte de edicao principal.

## Quando usar `*.local.*`

- Use para qualquer customizacao sua.
- Inclui ajustes de deploy, variaveis, imagens, portas e comandos.
- Deve ser o arquivo usado no dia a dia para operacao local e homologacao.

## Quando criar overlay

- Use overlay quando quiser manter o original intacto e aplicar ajustes por cima.
- Exemplo: `docker-compose.local.yml` e `stack.local.yml`.
- Prefira overlay quando a diferenca for pequena e precisar ficar visivel.

## Regra de decisao

- Se veio do upstream sem alteracao: `*.upstream.*`
- Se e seu e pode mudar: `*.local.*`
- Se depende do original e aplica ajustes: overlay local

## Exemplo

- `deploy/local/docker-compose.local.yml`
- `deploy/local/stack.local.yml`
- `docs/local/README.md`
