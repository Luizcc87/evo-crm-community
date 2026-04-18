# README de Operacoes

Guia operacional do fork `Luizcc87/evo-crm-community` para manter customizacoes sincronizadas com o projeto oficial, publicar imagens no Docker Hub e atualizar o ambiente via Portainer ou Docker Swarm.

## Objetivo

- Manter a `main` alinhada ao upstream `EvolutionAPI/evo-crm-community`
- Reaplicar customizacoes em branches proprias com historico limpo
- Publicar imagens versionadas no Docker Hub
- Atualizar a stack no Portainer ou via CLI do Swarm com previsibilidade

## Remotes

Este repositorio usa a seguinte configuracao:

- `origin` -> `https://github.com/Luizcc87/evo-crm-community.git`
- `upstream` -> `https://github.com/EvolutionAPI/evo-crm-community.git`

## Primeira Configuracao

Se voce clonou o fork pela primeira vez, execute isto antes de qualquer update:

```bash
git clone https://github.com/Luizcc87/evo-crm-community.git
cd evo-crm-community
git remote add upstream https://github.com/EvolutionAPI/evo-crm-community.git
git remote -v
```

## 1. Fluxo de Codigo

### Sincronizar a base oficial na `main`

Use `merge` na branch `main` para preservar rastreabilidade do que veio do repositorio oficial.

```bash
git remote set-url origin https://github.com/Luizcc87/evo-crm-community.git
git remote set-url upstream https://github.com/EvolutionAPI/evo-crm-community.git
git remote -v
git checkout main
git fetch upstream
git merge upstream/main
git push origin main
```

### Reaplicar customizacoes em branch propria

Use `rebase` nas branches de customizacao para manter seus commits no topo da base atualizada.

```bash
git checkout -b feature/uazapi
git rebase main
# Se houver conflito:
# git add .
# git rebase --continue
git push --force-with-lease origin feature/uazapi
```

## 2. Build e Publicacao no Docker Hub

Depois de validar a alteracao localmente, gere e publique a imagem da versao customizada.

### Build e tag

Prefira tags imutaveis para homologacao e producao.

```bash
docker login
docker buildx create --name evo-builder --use
docker buildx inspect --bootstrap
```

### Publicacao multi-arquitetura

Use este padrao para publicar imagens ARM64 e AMD64 no Docker Hub com uma unica tag:

```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t luizcc87/evo-crm:1.0.0-uazapi \
  -t luizcc87/evo-crm:latest \
  --push \
  .
```

### Imagens do stack

Use a tabela abaixo para publicar cada imagem principal do fork com a mesma estrategia multi-arquitetura.

| Servico | Contexto | Comando |
| --- | --- | --- |
| `evo-auth-service-community` | `./evo-auth-service-community` | `docker buildx build --platform linux/amd64,linux/arm64 -t luizcc87/evo-auth-service-community:1.0.0-uazapi -t luizcc87/evo-auth-service-community:latest --push ./evo-auth-service-community` |
| `evo-auth-sidekiq` | `./evo-auth-service-community` | `docker buildx build --platform linux/amd64,linux/arm64 -t luizcc87/evo-auth-service-community:1.0.0-uazapi -t luizcc87/evo-auth-service-community:latest --push ./evo-auth-service-community` |
| `evo-ai-crm-community` | `./evo-ai-crm-community` | `docker buildx build --platform linux/amd64,linux/arm64 -t luizcc87/evo-ai-crm-community:1.0.0-uazapi -t luizcc87/evo-ai-crm-community:latest --push ./evo-ai-crm-community` |
| `evo-crm-sidekiq` | `./evo-ai-crm-community` | `docker buildx build --platform linux/amd64,linux/arm64 -t luizcc87/evo-ai-crm-community:1.0.0-uazapi -t luizcc87/evo-ai-crm-community:latest --push ./evo-ai-crm-community` |
| `evo-ai-core-service-community` | `./evo-ai-core-service-community` | `docker buildx build --platform linux/amd64,linux/arm64 -t luizcc87/evo-ai-core-service-community:1.0.0-uazapi -t luizcc87/evo-ai-core-service-community:latest --push ./evo-ai-core-service-community` |
| `evo-ai-processor-community` | `./evo-ai-processor-community` | `docker buildx build --platform linux/amd64,linux/arm64 -t luizcc87/evo-ai-processor-community:1.0.0-uazapi -t luizcc87/evo-ai-processor-community:latest --push ./evo-ai-processor-community` |
| `evo-bot-runtime` | `./evo-bot-runtime` | `docker buildx build --platform linux/amd64,linux/arm64 -t luizcc87/evo-bot-runtime:1.0.0-uazapi -t luizcc87/evo-bot-runtime:latest --push ./evo-bot-runtime` |
| `evo-ai-frontend-community` | `./evo-ai-frontend-community` | `docker buildx build --platform linux/amd64,linux/arm64 -t luizcc87/evo-ai-frontend-community:1.0.0-uazapi -t luizcc87/evo-ai-frontend-community:latest --push ./evo-ai-frontend-community` |
| `evo-crm-gateway` | imagem base do gateway no Docker Hub | `docker buildx build --platform linux/amd64,linux/arm64 -t luizcc87/evo-crm-gateway:1.0.0-uazapi -t luizcc87/evo-crm-gateway:latest --push .` |

### Push para o Docker Hub

```bash
docker buildx imagetools inspect luizcc87/evo-crm:1.0.0-uazapi
```

### Padrao recomendado de tags

- `:1.0.0-uazapi` para release identificavel e rollback rapido
- `:latest` apenas como conveniencia operacional, nao como referencia principal de producao

## 3. Deploy com Portainer e Swarm

### Atualizar via Portainer

1. Acesse `Stacks` no Portainer.
2. Abra a stack do `evo-crm`.
3. Confirme que a imagem do servico aponta para a tag desejada no Docker Hub.
4. Se estiver usando `:latest`, habilite `Pull latest image`.
5. Clique em `Update the stack`.

### Atualizar via CLI no manager do Swarm

Se quiser atualizar somente um servico sem recriar a stack inteira:

```bash
docker service update --image luizcc87/evo-crm:1.0.0-uazapi evo-crm_service-name
```

Se a stack usa `:latest`, o update pode apontar para essa tag, mas o recomendado continua sendo usar uma tag fixa:

```bash
docker service update --image luizcc87/evo-crm:latest evo-crm_service-name
```

## 4. Boas Praticas

- Use `merge` na `main` e `rebase` apenas nas branches de trabalho.
- Em producao, prefira tags fixas no Compose ou no Portainer.
- Mantenha `:latest` apenas como atalho, nao como origem de verdade operacional.
- Antes de atualizar a stack, confirme no Docker Hub que a imagem nova foi publicada com sucesso.
- Para rollback, troque a imagem para a tag estavel anterior e reaplique a stack ou rode novo `docker service update`.

## 5. Fluxo Resumido

```bash
# 1. Atualizar base
git remote set-url origin https://github.com/Luizcc87/evo-crm-community.git
git remote set-url upstream https://github.com/EvolutionAPI/evo-crm-community.git
git checkout main
git fetch upstream
git merge upstream/main
git push origin main

# 2. Atualizar branch customizada
git checkout -b feature/uazapi
git rebase main
git push --force-with-lease origin feature/uazapi

# 3. Build e push
docker login
docker buildx create --name evo-builder --use
docker buildx inspect --bootstrap
docker buildx build --platform linux/amd64,linux/arm64 -t luizcc87/evo-crm:1.0.0-uazapi -t luizcc87/evo-crm:latest --push .

# 4. Deploy no Swarm
docker service update --image luizcc87/evo-crm:1.0.0-uazapi evo-crm_service-name
```

## 6. Decisao Operacional

Se a prioridade for estabilidade e rollback simples, publique com tag fixa no Docker Hub e use essa mesma tag no Portainer/Swarm.
