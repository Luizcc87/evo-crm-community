# AGENTS

Guia de seguranca operacional para agentes que trabalham neste fork.

## Antes de editar

- Confirme se a mudanca pertence ao repositorio principal ou a um submodulo.
- Verifique `git status` e nao sobrescreva alteracoes locais que nao sejam suas.
- Nao mexa em submodulos ignorados pelo usuario.

## Regras de separacao

- `*.upstream.*` e referencia da origem.
- `*.local.*` e a area de customizacao do fork.
- `docs/local/` e `deploy/local/` armazenam guias e overlays locais.

## Regras de deploy

- O stack deve continuar compativel com `docker-compose.swarm.yaml`.
- Qualquer imagem publicada para o fork deve sair em `amd64` e `arm64`.
- Use `docker buildx` para builds multi-arquitetura.
- Nao quebre os nomes dos services usados no Swarm e no Portainer.

## Regras de integridade

- Nao misture arquivos do upstream com arquivos locais no mesmo nome sem sufixo claro.
- Nao apague configs do stack sem verificar impacto nos services relacionados.
- Nao converta uma mudanca local em espelho do upstream por acidente.
- Se houver duvida sobre autoria da mudanca, pare e pergunte.

## Fluxo recomendado

1. Ler o contexto local e o estado do git.
2. Identificar se a mudanca e local, upstream ou de deploy.
3. Editar apenas o escopo necessario.
4. Validar o impacto no stack e nas imagens.
5. Commitar apenas o que pertence ao escopo da tarefa.

