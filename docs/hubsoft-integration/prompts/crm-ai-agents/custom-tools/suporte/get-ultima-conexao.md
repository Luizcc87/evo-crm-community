# Custom Tool: `get_ultima_conexao`

**Tipo:** Custom Tool HTTP
**Endpoint:** `GET /api/v1/integracao/cliente?busca=id_cliente_servico&termo_busca={id_cliente_servico}&ultima_conexao=sim`

## Usado por

- **Agente de Suporte Técnico**

## Parâmetros de Query

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `busca` | string | ✅ Sim | Fixo: `"id_cliente_servico"` — obrigatório, sem ele a API retorna erro |
| `termo_busca` | string | ✅ Sim | Valor do `id_cliente_servico` do cliente |
| `ultima_conexao` | string | ✅ Sim | Fixo: `"sim"` |

> ⚠️ **`busca` é obrigatório.** Enviar `id_cliente_servico` como parâmetro direto (sem `busca`/`termo_busca`) resulta em `"Favor preencher o atributo (busca)"`.

## Exemplo de configuração no Evo CRM (Query params)

```json
{
  "busca": "id_cliente_servico",
  "termo_busca": "{id_cliente_servico}",
  "ultima_conexao": "sim"
}
```

## Campos do retorno relevantes

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `conectado` | boolean | `true` = online no HubSoft, `false` = offline/sem sinal |
| `ultima_conexao_datetime` | string | Datetime da última conexão registrada no Radius |
| `status_txt` | string | Texto formatado para enviar diretamente ao cliente (ex: `"CONECTADO HÁ 0 MES(ES), 1 DIA(S)..."`) |

## Quando usar vs `get_extrato_conexao`

| Situação | Tool correta |
|----------|--------------|
| Verificar se o cliente está conectado agora | `get_ultima_conexao` |
| Cliente relata instabilidade intermitente (conecta e desconecta) | `get_extrato_conexao` |
| `conectado == false` e suspeita de quedas frequentes | `get_extrato_conexao` após `get_ultima_conexao` |

> **Prefira `get_ultima_conexao` como primeira verificação.** Chame `get_extrato_conexao` apenas quando `conectado == false` e houver suspeita de instabilidade — não como rotina.

## Retorno esperado

```json
{
  "status": "success",
  "conectado": false,
  "ultima_conexao_datetime": "2026-05-25 19:14:26-03",
  "status_txt": "DESCONECTADO HÁ 0 MES(ES), 2 DIA(S), 3 HORA(S) e 12 MINUTO(S)"
}
```

## Exemplo de payload para teste

```json
{
  "id_cliente_servico": 2491
}
```

## Nota

Os dados de `ultima_conexao` também estão disponíveis no retorno de `get_cliente_by_cpf` (campo `servicos[0].ultima_conexao`). Se o cliente já foi identificado via CPF, use os dados já retornados sem chamar esta tool novamente desnecessariamente.
