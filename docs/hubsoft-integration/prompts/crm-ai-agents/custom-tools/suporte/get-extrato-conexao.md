# Custom Tool: `get_extrato_conexao`

**Tipo:** Custom Tool HTTP
**Endpoint:** `GET /api/v1/integracao/cliente/extrato_conexao`

## Usado por

- **Agente de Suporte Técnico**

## Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `id_cliente_servico` | integer | ✅ Sim | Identificador do serviço do cliente |

## Quando usar

**Apenas quando `conectado == false`** (retornado por `get_cliente_by_cpf` ou `get_ultima_conexao`) e houver suspeita de instabilidade intermitente (quedas frequentes, reconexões).

Não chamar como primeira opção — é uma tool de investigação aprofundada, não de triagem inicial.

| Situação | Usar `get_extrato_conexao`? |
|----------|-----------------------------|
| `conectado == true` | ❌ Não — equipamento está online |
| `conectado == false`, causa única suspeita | ✅ Sim — verificar histórico |
| Cliente relata desconexões frequentes | ✅ Sim — análise de padrão |
| Primeira verificação de suporte | ❌ Não — use `get_cliente_by_cpf` primeiro |

## Retorno esperado

Histórico de eventos de conexão/desconexão do Radius. Útil para identificar padrões (ex: queda a cada 30 minutos, sinal perdido desde ontem às 3h, etc.).

```json
{
  "status": "success",
  "msg": "Dados consultados com sucesso",
  "extrato": [
    {
      "tipo": "desconexao",
      "datetime": "2026-05-27 03:22:00-03",
      "motivo": "Lost-Carrier"
    },
    {
      "tipo": "conexao",
      "datetime": "2026-05-27 03:23:45-03"
    }
  ]
}
```

## Exemplo de payload para teste

```json
{
  "id_cliente_servico": 2491
}
```

## Uso pós-extrato

Após analisar o extrato, o agente deve:

1. Identificar padrão (quedas intermitentes vs queda única prolongada)
2. Usar as informações na `descricao` ao abrir OS via `abrir_os_suporte`
3. Informar ao cliente o que foi identificado de forma simples (ex: "Identificamos 5 quedas nas últimas 3 horas")
