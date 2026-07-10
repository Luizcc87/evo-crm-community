# Custom Tool: `get_faturas_pendentes`

**Tipo:** Custom Tool HTTP
**Endpoint:** `GET /api/v1/integracao/cliente/financeiro`

## Usado por

- **Agente de Suporte Técnico** — para verificar se causa da queda é inadimplência (`status_prefixo == "suspenso_inadimplencia"`) antes de abrir OS
- **Agente Financeiro** — para listar faturas em aberto e fornecer linha digitável, PIX e link do boleto

## Argumento exposto ao agente

| Argumento | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `id_cliente_servico` | integer | ✅ Sim | Identificador do serviço do cliente |

## Configuração HTTP no Evo CRM (query params)

| Query param | Valor | Tipo |
|-------------|-------|------|
| `busca` | `id_cliente_servico` | Fixo (hardcoded na config da tool) |
| `termo_busca` | `{id_cliente_servico}` | Dinâmico — mapeado do argumento `id_cliente_servico` |
| `apenas_pendente` | `sim` | Fixo (hardcoded na config da tool) |

> ⚠️ **`busca` deve ser hardcoded na config da tool, não exposto ao agente.** Sem ele o endpoint retorna faturas de **todos os clientes** — vazamento LGPD. O agente passa apenas `id_cliente_servico`.

## Edge Cases

| Cenário | Comportamento |
|---------|---------------|
| `busca` omitido na config | Retorna faturas de **todos** os clientes — crítico, configurar corretamente |
| `apenas_pendente` omitido | Retorna todas as faturas, incluindo quitadas (`quitado: true`) |
| `apenas_pendente: "sim"` | Retorna apenas faturas com `quitado: false` e `status: "aguardando"` |
| Cliente sem faturas pendentes | `faturas: []` com `status: "success"` |

## Campos do retorno relevantes para o agente

| Campo | Tipo | Uso |
|-------|------|-----|
| `id_fatura` | integer | Identificador da fatura |
| `linha_digitavel` | string | Código de barras legível para pagamento em banco/lotérica |
| `pix_copia_cola` | string | Payload PIX completo — copiar e enviar ao cliente sem modificar |
| `link` | string | URL do PDF do boleto (expira conforme configuração do provedor) |
| `valor` | number | Valor da fatura em R$ |
| `data_vencimento` | string | Data de vencimento (formato `"DD/MM/AAAA"`) |
| `status` | string | Status textual (`"aguardando"`, etc.) |
| `quitado` | boolean | `false` = pendente, `true` = quitada |

> **Atenção PIX:** Não altere o conteúdo de `pix_copia_cola` — o payload é gerado com hash de integridade e qualquer modificação o invalida.

## Contexto por agente

**Suporte Técnico:** Chama esta tool **apenas** quando `status_prefixo` não for claramente `"suspenso_inadimplencia"` mas houver dúvida. Fatura pendente + serviço suspenso → encaminhar para Financeiro sem abrir OS.

**Financeiro:** Chama esta tool **após** validação de identidade via `get_cliente_by_dados`. Deve listar **todas as faturas em aberto** de forma resumida antes de perguntar qual o cliente quer pagar.

## Retorno esperado

```json
{
  "status": "success",
  "msg": "Dados consultados com sucesso",
  "faturas": [
    {
      "id_fatura": 155491,
      "quitado": false,
      "status": "aguardando",
      "linha_digitavel": "74891.12529 11288.203075 20007.811027 6 14830000012000",
      "pix_copia_cola": "00020101021226850014BR.GOV.BCB.PIX...",
      "link": "https://<host>/pdf/fatura/<hash>",
      "valor": 120,
      "data_vencimento": "20/06/2026",
      "data_pagamento": null
    }
  ]
}
```

## Exemplo de payload para teste (botão Testar do Evo CRM)

```json
{
  "id_cliente_servico": 2491
}
```
