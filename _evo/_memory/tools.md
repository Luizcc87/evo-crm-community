---
title: "Ferramentas do Evo CRM Community"
description: "Inventário de ferramentas de desenvolvimento, Docker, submodules, banco de dados e variáveis de ambiente do projeto Evo CRM Community."
date: 2026-06-01
---

# Ferramentas do Evo CRM Community

## Ferramentas de Desenvolvimento Local (Make)

O projeto usa um `Makefile` raiz para orquestrar todos os serviços. Execute os targets a partir da raiz do repositório.

### Ciclo de Vida do Ambiente

| Target | Descrição | Cenário de Uso | Restrições |
|---|---|---|---|
| `make setup` | Copia `.env`, constrói imagens, inicia serviços e executa seed completo | Primeira execução em uma máquina nova | Execute apenas uma vez; reexecutar sobrescreve dados existentes |
| `make start` | `docker compose up -d` | Iniciar ambiente após parada | Requer imagens já construídas |
| `make stop` | `docker compose down` | Parar todos os serviços | Preserva volumes e dados |
| `make restart` | `down` + `up` | Reiniciar após mudança de configuração | Equivale a `stop` + `start` |
| `make build` | Reconstrói todas as imagens sem cache | Após mudanças em Dockerfiles ou dependências | `--no-cache` — operação custosa; use apenas quando necessário |
| `make status` | `docker compose ps` | Verificar estado dos containers | Somente leitura |
| `make logs` | Exibe logs de todos os serviços | Debugging geral | Use `make logs SERVICE=<nome>` para filtrar por serviço |
| `make clean` | `docker compose down -v` | Limpar ambiente completamente | **DESTRUTIVO** — remove todos os volumes e dados; não reversível |

### Banco de Dados e Seed

| Target | Descrição | Cenário de Uso | Restrições |
|---|---|---|---|
| `make seed` | Executa `seed-crm` e depois `seed-auth` (ordem correta) | Popular banco após `make setup` | A ordem é obrigatória: CRM antes de Auth falha |
| `make seed-crm` | `db:create` + `schema:load` + marca migrations de auth + seed CRM | Recriar dados do CRM isoladamente | Depende do usuário criado pelo seed de auth |
| `make seed-auth` | Seed do serviço de autenticação (cria usuário padrão) | Recriar usuário padrão | Execute após `seed-crm` em setup inicial |

> **Atenção:** A ordem de seed importa. O seed do CRM depende do usuário criado pelo seed de auth. Execute sempre `seed-crm` antes de `seed-auth` em setup inicial, ou use `make seed` que já gerencia a ordem correta.

### Acesso ao Shell dos Containers

| Target | Container | Shell |
|---|---|---|
| `make shell-auth` | `evo-auth-service-community` | bash |
| `make shell-crm` | `evo-ai-crm-community` | bash |
| `make shell-core` | `evo-ai-core-service-community` | sh (Alpine) |
| `make shell-processor` | `evo-ai-processor-community` | bash |
| `make shell-bot-runtime` | `evo-bot-runtime` | sh (Alpine) |

## Ferramentas Docker

O projeto orquestra 6 serviços principais via Docker Compose.

```bash
# Iniciar todos os serviços em background
docker compose up -d

# Parar todos os serviços (preserva volumes)
docker compose down

# Reconstruir imagens sem cache (após mudanças em Dockerfiles)
docker compose build --no-cache

# Ver logs de um serviço específico
docker compose logs -f <nome-do-serviço>
```

Os serviços e suas portas:

| Serviço | Stack | Porta |
|---|---|---|
| `evo-auth-service-community` | Ruby 3.4 / Rails 7.1 | 3001 |
| `evo-ai-crm-community` | Ruby 3.4 / Rails 7.1 | 3000 |
| `evo-ai-frontend-community` | React / TypeScript / Vite | 5173 |
| `evo-ai-processor-community` | Python 3.10 / FastAPI | 8000 |
| `evo-ai-core-service-community` | Go / Gin | 5555 |
| `evo-bot-runtime` | Go / Gin | 8080 |

## Ferramentas de Submodules

O repositório contém dois tipos de submodules com estratégias de atualização distintas.

### Submodules Pinados (Serviços Core)

Estes submodules são pinados na tag `v1.0.0-rc2` e **não devem ser atualizados automaticamente**:

- `evo-auth-service-community`
- `evo-ai-crm-community`
- `evo-ai-frontend-community`
- `evo-ai-processor-community`
- `evo-ai-core-service-community`
- `evo-bot-runtime`

### Submodules Companion (Versionamento Independente)

Estes submodules têm versionamento próprio e podem ser atualizados para a última versão:

- `evolution-api` — WhatsApp engine (Node.js)
- `evolution-go` — WhatsApp engine (Go, alternativa de alta performance)
- `evo-nexus` — camada multi-agent

```bash
# Inicializar todos os submodules (primeira vez)
git submodule update --init --recursive

# Atualizar apenas os companion submodules para latest
git submodule update --remote

# Atualizar um submodule específico
git submodule update --remote evolution-go
```

> **Importante:** `git submodule update --remote` atualiza **todos** os submodules para o HEAD remoto. Para atualizar apenas companions sem afetar os pinados, especifique o nome do submodule explicitamente.

## Variáveis de Ambiente Críticas

Copie `.env.example` → `.env` para desenvolvimento local. Os defaults funcionam sem edição.

### Variáveis Obrigatórias em Produção

| Variável | Serviço | Descrição | Restrição |
|---|---|---|---|
| `BACKEND_URL` | CRM | URL pública do backend do CRM | **Não pode ser `localhost` em produção** — o CRM recusa inicialização |
| `FRONTEND_URL` | CRM | URL pública do frontend | Usada em redirects OAuth e fallbacks de webhook |

### Segredos Compartilhados Entre Serviços

Estas variáveis devem ter **valores idênticos** nos serviços listados:

| Segredo | Serviços que compartilham |
|---|---|
| JWT signing secret | `evo-auth-service-community`, `evo-ai-crm-community`, `evo-ai-core-service-community` |
| API key encryption secret | `evo-ai-core-service-community`, `evo-ai-processor-community` |
| Service-to-service auth secret | `evo-auth-service-community`, `evo-ai-crm-community`, `evo-ai-processor-community` |

> **Segurança:** Nunca commite o arquivo `.env` com valores reais. Use `.env.example` para documentar variáveis sem expor segredos.

## Ferramentas de Banco de Dados

### Rails Services (Ruby)

Os serviços Rails (`evo-auth-service-community` e `evo-ai-crm-community`) compartilham a mesma instância PostgreSQL com pgvector e usam migrations Rails:

```bash
# Aplicado automaticamente via make seed-crm
rails db:create
rails db:schema:load
rails db:seed
```

### Go Services

Os serviços Go (`evo-ai-core-service-community`, `evo-bot-runtime`) usam **golang-migrate** com arquivos SQL numerados em `migrations/`:

```
migrations/
  000001_initial_schema.up.sql
  000001_initial_schema.down.sql
  000002_add_feature.up.sql
  000002_add_feature.down.sql
```

Cada Go service tem seu próprio `Makefile` interno para desenvolvimento local fora do Docker.

### Extensão pgvector

O PostgreSQL compartilhado usa a extensão **pgvector** para armazenamento e busca de embeddings vetoriais — requisito dos serviços de IA.

## Restrições Gerais

- **Ordem de seed é obrigatória:** `seed-crm` deve rodar antes de `seed-auth`. O seed do CRM depende do usuário criado pelo seed de auth.
- **`BACKEND_URL` em produção** não pode conter `localhost` — o serviço CRM valida isso na inicialização e recusa boot.
- **`make clean` é destrutivo** — remove todos os volumes Docker. Todos os dados do banco são perdidos.
- **Submodules pinados** (`v1.0.0-rc2`) não devem receber `--remote` update inadvertido.
- **Go services** usam schemas separados no PostgreSQL — não compartilham schemas com os serviços Rails.
