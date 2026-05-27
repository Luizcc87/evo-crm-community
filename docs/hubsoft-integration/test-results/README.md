# HubSoft API — Resultados de Teste

Payloads reais capturados e sanitizados durante validação da integração HubSoft × Evo CRM.  
Execução: **2026-05-27** | Tenant: `api.log.hubsoft.com.br` | Suite: **27 passed, 5 skipped, 0 failed**

---

## Arquivos de payload

| Arquivo | Endpoint | Módulo | Status |
|---|---|---|---|
| `auth-response.example.json` | `POST /oauth/token` | Auth | ✅ real |
| `cliente-cpf-response.example.json` | `GET /api/v1/integracao/cliente` | Clientes | ✅ real |
| `financeiro-response.example.json` | `GET /api/v1/integracao/cliente/financeiro` | Financeiro | ✅ real |
| `suporte-os-response.example.json` | `GET /api/v1/integracao/cliente/ordem_servico` | Suporte | ✅ real |
| `suporte-atendimento-response.example.json` | `POST /api/v1/integracao/atendimento` | Suporte | ⏸ sandbox only |
| `viabilidade-response.example.json` | `POST /api/v1/integracao/mapeamento/viabilidade/consultar` | Mapeamento | ✅ real |
| `crms-response.example.json` | `GET /api/v1/integracao/crm/all` | Vendas | ✅ real |
| `planos-cep-response.example.json` | `GET /api/v1/integracao/prospecto/create` | Vendas | ⏸ CEP sem cobertura |
| `vendas-prospecto-response.example.json` | `POST /api/v1/integracao/prospecto` | Vendas | ⏸ sandbox only |
| `cpe-params-discovery.json` | `GET /api/v1/integracao/rede/cpe/todos` | Rede | 🔍 discovery |

---

## Descobertas durante execução

### CPE — params obrigatórios não documentados

O endpoint `GET /api/v1/integracao/rede/cpe/todos` **requer** `pagina` e `itens_por_pagina` na query string. Sem eles retorna `status=error`. A collection Postman não documenta esses params. Ver `cpe-params-discovery.json`.

### Renegociação — campo `tipo_dados_cliente` aceita valores específicos

O campo aceita apenas `"codigo_cliente"` ou `"id_cliente"`. Tentativa com `"cpf_cnpj"` retorna erro de validação. O campo complementar é `dado_cliente` (não `documento_cliente`).

### Viabilidade — retorna `projetos` como string descritiva

Quando nenhum projeto cobre a localização, `resultado.projetos` retorna a string `"Nenhum Projeto foi compatível com a localização."` em vez de array vazio. Tratar como string no parser.

---

## Como executar os testes

```bash
cd scripts/hubsoft-api-tests
cp .env.example .env
# preencher .env com credenciais reais do tenant

pip install -r requirements.txt

# rodar testes sem side-effects (recomendado em produção)
pytest -v

# rodar tudo incluindo testes marcados skip (sandbox apenas)
# remover pytest.skip() nos testes desejados antes de executar
pytest -v -p no:skip
```

## Dados necessários no `.env`

| Variável | Como obter |
|---|---|
| `HUBSOFT_HOST` | URL da API fornecida pelo HubSoft |
| `HUBSOFT_CLIENT_ID` | Criado pelo admin do provedor no painel HubSoft |
| `HUBSOFT_CLIENT_SECRET` | Criado junto com client_id |
| `HUBSOFT_USERNAME` | Usuário técnico criado para a integração |
| `HUBSOFT_PASSWORD` | Senha do usuário técnico |
| `TEST_CPF_CNPJ` | CPF/CNPJ de cliente real ativo no tenant |
| `TEST_CODIGO_CLIENTE` | `codigo_cliente` do mesmo cliente |
| `TEST_ID_CLIENTE_SERVICO` | `id_cliente_servico` de um serviço ativo do cliente |
| `TEST_ID_TIPO_ATENDIMENTO` | ID obtido via `GET /api/v1/integracao/configuracao/tipo_atendimento` |
| `TEST_CEP` | CEP com cobertura no tenant (planos disponíveis) |

## Convenções dos arquivos `.example.json`

- Dados pessoais mascarados: CPF com `***.***.***-**`, nomes como `NOME DO CLIENTE`
- Tokens e hashes substituídos por `<token-omitido>` e `<hash>`
- UUIDs truncados com `<uuid-omitido>`
- Campo `_meta` documenta endpoint, parâmetros, data e notas — não faz parte da resposta real
- Atualizar os arquivos após cada validação com novo tenant, mantendo dados fictícios
