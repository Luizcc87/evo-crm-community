# Context

Este repositorio e um fork de `EvolutionAPI/evo-crm-community`.

## Remotes

- `origin`: `https://github.com/Luizcc87/evo-crm-community.git`
- `upstream`: `https://github.com/EvolutionAPI/evo-crm-community.git`

## Convencao de arquivos

- `*.upstream.*` para espelho da origem oficial.
- `*.local.*` para customizacoes e overlays locais.
- Arquivos locais ficam em `docs/local/` e `deploy/local/` quando forem de documentacao ou deploy.

## Topologia de deploy

- O stack principal e o `docker-compose.swarm.yaml`.
- `deploy/local/docker-compose.local.yml` e um overlay local para desenvolvimento e ajuste.
- `deploy/local/stack.local.yml` e um overlay local para Swarm.
- O fluxo de producao usa Portainer ou Swarm com imagens publicadas no Docker Hub.

## Imagens

- Publishe imagens para `linux/amd64` e `linux/arm64`.
- Use `docker buildx build --platform linux/amd64,linux/arm64`.
- Prefira tag fixa para producao e use `latest` apenas como conveniencia operacional.

## Regras de trabalho

- Nao misture mudancas locais com espelhos do upstream.
- Nao altere submodulos sem necessidade explicita.
- Se um arquivo for copiado da origem, mantenha o sufixo `.upstream`.
- Se um arquivo for alterado por voce, mantenha o sufixo `.local`.
- Preserve a topologia de services e nomes do stack ao editar deploy.

