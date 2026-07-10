# Custom Tool: `request_desbloqueio_confianca`

**Tipo:** Custom Tool HTTP
**Endpoint:** `POST /api/v1/integracao/...` (desbloqueio temporário no HubSoft)

## Usado por

- **Agente Financeiro**

## Pré-condições

1. Identidade do cliente validada via `get_cliente_by_dados`
2. Cliente **deve ser elegível** para desbloqueio em confiança no painel HubSoft
3. Agente deve oferecer esta opção **somente se habilitada** para o cliente — não oferecer como padrão

## Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `id_cliente_servico` | integer | ✅ Sim | Identificador do serviço do cliente |
| `dias` | integer | ✅ Sim | Prazo em dias da liberação temporária |

## Quando usar

- Cliente solicitou e **está bloqueado** por inadimplência
- Cliente **é elegível** no painel HubSoft (campo de elegibilidade verificado pelo sistema)
- Após validar identidade com `get_cliente_by_dados`

## Comportamento quando cliente não é elegível

Se o cliente não for elegível para desbloqueio em confiança, a API retornará erro. O agente deve informar que não é possível aplicar o desbloqueio temporário e orientar o pagamento via boleto ou PIX.

```json
{
  "status": "error",
  "msg": "Cliente não elegível para desbloqueio em confiança"
}
```

## Retorno esperado (sucesso)

```json
{
  "status": "success",
  "msg": "Desbloqueio em confiança aplicado com sucesso",
  "prazo_dias": 3,
  "validade_ate": "2026-06-02"
}
```

## Exemplo de payload para teste

```json
{
  "id_cliente_servico": 2491,
  "dias": 3
}
```

## O que informar ao cliente após o desbloqueio

Obrigatoriamente informe:
1. O prazo de validade da liberação temporária
2. Que a fatura **continua pendente** — o desbloqueio não quita a dívida
3. Que a baixa bancária pode levar minutos (PIX) ou até 1 dia útil (Boleto)
4. Não prometa reconexão imediata — depende da baixa real no sistema HubSoft
