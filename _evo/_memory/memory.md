---
title: "Contexto Persistente do Projeto Evo CRM Community"
description: "Memória de contexto para continuidade entre sessões: arquitetura, decisões, estado atual e próximos passos."
date: 2026-06-01
---

# Contexto Persistente — Evo CRM Community

## Stack e Arquitetura

O Evo CRM Community é um monorepo-orquestrador que agrega 6 serviços via `docker-compose.yml` + `Makefile` raiz.

### Serviços

| Submodule | Stack | Porta |
|---|---|---|
| `evo-auth-service-community` | Ruby 3.4 / Rails 7.1 | 3001 |
| `evo-ai-crm-community` | Ruby 3.4 / Rails 7.1 | 3000 |
| `evo-ai-frontend-community` | React / TypeScript / Vite | 5173 |
| `evo-ai-processor-community` | Python 3.10 / FastAPI | 8000 |
| `evo-ai-core-service-community` | Go / Gin | 5555 |
| `evo-bot-runtime` | Go / Gin | 8080 |

### Companion Submodules

Três submodules com versionamento independente (não pinados ao tag do CRM):

| Submodule | Descrição |
|---|---|
| `evolution-api` | WhatsApp engine (Node.js) |
| `evolution-go` | WhatsApp engine (Go, alternativa de alta performance) |
| `evo-nexus` | Camada multi-agent operacional |

## Decisões Arquiteturais

### Single-Tenant por Design

O sistema foi construído para um único tenant por instalação. Multi-tenancy não é suportado e não está no roadmap.

**Impacto:** Não há lógica de isolamento de dados por conta em código — o isolamento é por instalação (deploy separado por cliente).

### Sem Super-Admin

Não existe role de super-admin. Configuração administrativa é feita via:

- Seed data (dados iniciais no banco)
- Variáveis de ambiente

**Impacto:** Novas configurações globais exigem alteração de seed ou nova variável de ambiente — não existe painel de administração global.

### Resolução de Conta via Token

Serviços internos não precisam enviar o header `account-id` nas chamadas entre si. A conta é resolvida a partir do token JWT.

**Impacto:** Simplifica chamadas service-to-service; o token deve ser sempre propagado corretamente.

### Hierarquia de Roles Simplificada

Apenas dois roles existem:

- `account_owner` — acesso total
- `agent` — acesso restrito ao escopo de atendimento

**Impacto:** Qualquer nova funcionalidade deve ser categorizada em um destes dois roles. Não criar roles intermediários.

### PostgreSQL Compartilhado com pgvector

Os serviços Rails (`evo-auth-service-community` e `evo-ai-crm-community`) compartilham a mesma instância PostgreSQL com a extensão pgvector ativa.

Os serviços Go (`evo-ai-core-service-community`, `evo-bot-runtime`) usam schemas separados gerenciados por golang-migrate.

**Impacto:** Migrations Rails e Go são gerenciadas por ferramentas distintas e não devem se misturar.

### JWT Signing Secret Compartilhado

O mesmo JWT signing secret deve estar configurado em `evo-auth-service-community`, `evo-ai-crm-community` e `evo-ai-core-service-community`. Divergência causa falhas de autenticação silenciosas.

## Estado Atual do Desenvolvimento

**Branch ativa:** `feat/hubsoft-api-tests-and-agent-prompts`

Esta branch contém trabalho em andamento relacionado a:

- Documentação técnica e testes para integração HubSoft API
- Refinamento de prompts para agentes de IA do CRM

## Trabalho Recente Relevante

### HubSoft API — Integração e Documentação

- **14 tools documentadas** com tech-spec completa
- **15 arquivos MD** produzidos (documentação compartilhada + por agente)
- **15 tasks** e **9 Acceptance Criteria** definidos
- **Bugs LGPD corrigidos:**
  - `get_faturas_pendentes` — parâmetros corrigidos para conformidade LGPD
  - `get_cliente_by_dados` — parâmetros corrigidos para conformidade LGPD
- **Deprecação:** `get_cliente_by_cpf_cnpj` foi depreciada; substituída por `get_cliente_by_dados`

### evolution-go — Refactor NativeFlowMessage

- Refactor de `CarouselMessage` → `NativeFlowMessage` em `send_service.go`
- Motivação: compatibilidade com clientes WhatsApp atuais (Impa365)
- Imagem Docker multi-arch publicada: `lc1868/evolution-go:latest` (amd64 + arm64)
- Mudanças registradas em `docs/CHANGES-LOCAL.md` para manutenção contra upstream

## Preferências do Projeto

| Preferência | Valor |
|---|---|
| Idioma de comunicação | Português (PT) |
| Pasta de output | `_evo-output/` |
| Estimativas de tempo em docs | Proibidas (nunca documentar duração ou esforço) |
| Padrão de documentação | CommonMark estrito |
| Decisões arquiteturais | Registrar via ADR |

## Configuração do Git & WSL

- **Helper de Credenciais no WSL:** Para permitir que operações do Git dentro do WSL (como `git push` ou `git fetch` em submodules) consumam as credenciais autenticadas do Windows Host automaticamente, use:
  ```bash
  git config --global credential.helper "/mnt/c/Program\ Files/Git/mingw64/bin/git-credential-manager.exe"
  ```
- **Prevenção de Travamentos (Hanging):** Ao rodar scripts automatizados de Git que executam push/pull/fetch, desative prompts de terminal com `env GIT_TERMINAL_PROMPT=0` para que falhem imediatamente caso falte autenticação, impedindo que o script trave indefinidamente.

## Próximos Passos Conhecidos

- **Reconfiguração do Evo CRM** para integração com HubSoft API — o sistema precisa ser reconfigurado para consumir as tools documentadas na branch atual.
