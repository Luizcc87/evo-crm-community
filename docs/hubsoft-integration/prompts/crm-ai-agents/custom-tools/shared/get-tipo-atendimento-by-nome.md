# Custom Tool: `get_tipo_atendimento_by_nome`

**Tipo:** Custom Tool HTTP
**Endpoint:** HubSoft — busca de tipos de atendimento por nome de setor

## Usado por

- **Agente de Suporte Técnico** — para obter o `id_tipo_atendimento` do setor de suporte antes de `abrir_os_suporte`
- **Agente de Retenção** — para obter o `id_tipo_atendimento` do setor de cancelamento antes de `abrir_os_cancelamento`

## Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `nome_setor` | string | ✅ Sim | Nome do setor de atendimento conforme cadastrado no HubSoft |

## Valores conhecidos de `nome_setor` por agente

| Agente | Valor de `nome_setor` |
|--------|----------------------|
| Suporte Técnico | `"suporte técnico"` |
| Retenção | `"cancelamento"` (ou equivalente cadastrado no HubSoft do tenant) |

> O valor exato depende do cadastro de tipos de atendimento do tenant HubSoft. Confirme com o configurador do sistema se o nome não for encontrado.

## Quando chamar

**Sempre chame esta tool antes de:**
- `abrir_os_suporte` (Agente Suporte)
- `abrir_os_cancelamento` (Agente Retenção)

O `id_tipo_atendimento` retornado por esta tool é parâmetro obrigatório de ambas. Não assuma um valor fixo — busque sempre via tool para garantir que o ID está correto no tenant.

## Retorno esperado

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id_tipo_atendimento` | integer | ID do tipo de atendimento — usar nas tools de abertura de OS |

```json
{
  "status": "success",
  "msg": "Dados consultados com sucesso",
  "id_tipo_atendimento": 7
}
```

## Exemplo de payload para teste

**Suporte:**
```json
{
  "nome_setor": "suporte técnico"
}
```

**Retenção:**
```json
{
  "nome_setor": "cancelamento"
}
```

## Fluxo encadeado típico (Suporte)

```
1. get_cliente_by_cpf(cpf_cnpj) → obtém id_cliente_servico
2. [diagnóstico indica necessidade de OS]
3. get_tipo_atendimento_by_nome("suporte técnico") → obtém id_tipo_atendimento
4. abrir_os_suporte(id_cliente_servico, id_tipo_atendimento, descricao, abrir_os)
```
