# Custom Tool: `get_cpe_info`

**Tipo:** Custom Tool HTTP
**Endpoint:** `GET /api/v1/integracao/rede/cpe/todos`

## Usado por

- **Agente de Suporte Técnico**

## Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `id_cliente_servico` | integer | ✅ Sim | Identificador do serviço do cliente |
| `pagina` | integer | ✅ **Obrigatório** | Número da página (base 0 — a primeira página é `0`) |
| `itens_por_pagina` | integer | ✅ **Obrigatório** | Quantidade de itens por página |

> ⚠️ **`pagina` e `itens_por_pagina` são obrigatórios.** A API HubSoft retorna erro de validação se qualquer um for omitido. Esses parâmetros **não estão documentados na collection Postman original** — foram descobertos por testes (ver `cpe-params-discovery.json`).

## Erro quando parâmetros são omitidos

Se `pagina` ou `itens_por_pagina` forem omitidos, o retorno será:

```json
{
  "status": "error",
  "msg": "Verifique os dados informados e tente novamente!",
  "errors": [
    "O campo pagina é obrigatório.",
    "O campo itens por pagina é obrigatório."
  ]
}
```

## Estrutura do retorno

```json
{
  "status": "success",
  "paginacao": {
    "primeira_pagina": 0,
    "ultima_pagina": 0,
    "pagina_atual": 0,
    "total_registros": 0
  },
  "cpes": [
    {
      "id_cpe": 123,
      "modelo": "TP-Link EAP110",
      "mac": "64:5E:10:63:D3:FC",
      "serial": "..."
    }
  ]
}
```

> Tenant sem CPEs cadastrados retorna `cpes: []` com `status: "success"` — não é erro.

## Exemplo de payload para teste

```json
{
  "id_cliente_servico": 2491,
  "pagina": 0,
  "itens_por_pagina": 10
}
```

## Paginação

- Primeira página: `pagina: 0` (não `1`)
- Verificar `paginacao.ultima_pagina` para saber se há mais páginas
- Para a maioria dos diagnósticos, `pagina: 0, itens_por_pagina: 10` é suficiente
