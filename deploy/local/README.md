# Deploy Local

Pasta para artefatos de deploy mantidos por voce.

## Convencao

- Arquivos nesta pasta sao customizacoes locais ou ajustes de operacao.
- Nao coloque aqui arquivos copiados diretamente do upstream sem necessidade de edicao.
- Use nomes claros e previsiveis, por exemplo:
  - `docker-compose.local.yml`
  - `stack.local.yml`
  - `env.local.example`
  - `docker-compose.upstream.yml`

## Regra pratica

- `upstream`: base oficial do projeto.
- `local`: tudo que for seu, de operacao, ajuste ou overlay.

## Convencao de nomes

- `*.upstream.*` para arquivos copiados da origem e mantidos como referencia.
- `*.local.*` para arquivos de deploy com alteracoes suas.
- Use o mesmo prefixo base do arquivo original para facilitar comparacao e revisao.

## Exemplo pratico

- `deploy/local/docker-compose.local.yml` como overlay local.
- `deploy/local/stack.local.yml` como overlay local para Swarm.
- `deploy/local/docker-compose.upstream.yml` como espelho da origem.
- Se precisar espelhar a origem, use algo como `docker-compose.upstream.yml` para deixar claro que o arquivo nao e a sua versao editada.
