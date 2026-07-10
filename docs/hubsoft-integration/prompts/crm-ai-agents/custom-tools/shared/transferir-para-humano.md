# Custom Tool: `transferir_para_humano`

**Tipo:** Custom Tool HTTP
**Aba de configuração:** Custom Tools (não Sub Agents)

> ⚠️ **Atenção:** Esta tool é diferente das tools de roteamento de sub-agentes (`transferir_para_financeiro`, `transferir_para_suporte`, etc.). Aquelas são **Native Tools** configuradas na aba **Sub Agents** do Evo CRM e transferem entre agentes. Esta tool posta o atendimento na **fila humana** do Evo CRM — é um endpoint HTTP real.

## Usado por

- Agente Orquestrador
- Agente de Suporte Técnico
- Agente Financeiro
- Agente de Vendas Fibra
- Agente de Vendas Móvel
- Agente de Retenção

## Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `resumo` | string | ✅ Sim | Resumo estruturado do atendimento para o operador humano |

## Quando usar

- Cliente solicita explicitamente falar com atendente humano
- Falha em qualquer outra tool durante o atendimento
- Diagnóstico inconclusivo após todas as tentativas de resolução
- Orquestrador: intenção não classificada após 2 interações
- Vendas: ao final do fluxo, para o time comercial finalizar a contratação (com resumo completo dos dados coletados)
- Retenção: após OS de cancelamento aberta

## Retorno esperado

```json
{
  "status": "success",
  "msg": "Atendimento transferido para fila humana"
}
```

Em caso de erro:

```json
{
  "status": "error",
  "msg": "Descrição do erro"
}
```

## Exemplo de payload para teste

```json
{
  "resumo": "Cliente João Silva (id_cliente_servico: 2491) com conexão instável há 3 horas. Diagnóstico: conectado=false no HubSoft, extrato mostra desconexões intermitentes. OS #4401 aberta. Cliente solicita acompanhamento humano."
}
```

## Boas práticas para o campo `resumo`

O resumo deve conter informações suficientes para o operador humano não precisar pedir dados já coletados:

- Nome e identificação do cliente (`id_cliente_servico` e/ou `codigo_cliente`)
- Motivo do contato
- O que já foi tentado/verificado
- Status atual (faturas, conexão, OS aberta, etc.)
- Expectativa do cliente
