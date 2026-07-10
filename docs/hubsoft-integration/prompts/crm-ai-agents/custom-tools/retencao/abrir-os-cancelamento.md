# Custom Tool: `abrir_os_cancelamento`

**Tipo:** Custom Tool HTTP
**Endpoint:** HubSoft — abertura de OS de cancelamento/encerramento de serviço

## Usado por

- **Agente de Retenção**

## Pré-requisitos (em ordem)

1. `get_cliente_by_id_servico` executada — dados contratuais obtidos
2. Tentativas de retenção realizadas (empatia, benefícios, renegociação registrada se preço)
3. **Confirmação explícita do cliente coletada** — o agente DEVE perguntar e receber "sim" antes de chamar esta tool
4. `get_tipo_atendimento_by_nome` executada — `id_tipo_atendimento` obtido

## Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `id_cliente_servico` | integer | ✅ Sim | Identificador do serviço do cliente |
| `id_tipo_atendimento` | integer | ✅ Sim | Obtido via `get_tipo_atendimento_by_nome("cancelamento")` |
| `motivo_detalhado` | string | ✅ Sim | Motivo completo do cancelamento relatado pelo cliente |

## ⚠️ Confirmação explícita obrigatória

**Nunca chame esta tool sem confirmação do cliente.** O prompt do agente exige:

> "Antes de finalizar, você DEVE pedir a confirmação explícita do cliente (ex: 'Confirma a abertura do pedido de cancelamento?'). Só depois de ouvir o SIM, abra a OS."

Se o cliente disser "sim" → chamar a tool.
Se o cliente hesitar ou não responder → não chamar, continuar tentativa de retenção.

## Retorno esperado

```json
{
  "status": "success",
  "msg": "OS de cancelamento aberta com sucesso",
  "protocolo": "202605270002",
  "id_atendimento": 9902
}
```

## Exemplo de payload para teste

```json
{
  "id_cliente_servico": 2491,
  "id_tipo_atendimento": 12,
  "motivo_detalhado": "Cliente solicitou cancelamento por mudança de cidade. Contrato com 3 meses de fidelidade restantes — cliente foi informado sobre possível multa rescisória e confirmou ciência. Confirmação explícita de cancelamento recebida."
}
```

## Fluxo completo encadeado

```
1. get_cliente_by_id_servico(id_cliente_servico)          → dados contratuais, vigência
2. [tentativas de retenção: empatia, benefícios]
3. [se motivo preço] registrar_renegociacao(...)           → registra para equipe
4. [cliente confirma cancelamento explicitamente]
5. get_tipo_atendimento_by_nome("cancelamento")            → id_tipo_atendimento
6. abrir_os_cancelamento(id_cliente_servico, id_tipo_atendimento, motivo_detalhado)
7. Informar protocolo ao cliente
8. transferir_para_humano(resumo)                          → equipe finaliza processo
```

## Pós-cancelamento

Após abrir a OS, sempre chamar `transferir_para_humano` com resumo completo: nome do cliente, motivo, protocolo gerado, multa informada ou não.
