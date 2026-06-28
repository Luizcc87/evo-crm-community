# Custom Tool: `registrar_renegociacao`

**Tipo:** Custom Tool HTTP
**Endpoint:** HubSoft — registro de solicitação de renegociação para análise humana

## Usado por

- **Agente de Retenção**

## Regra crítica

> ⚠️ **O agente NÃO oferece desconto diretamente.** Esta tool apenas registra o interesse do cliente em renegociação para análise pela equipe humana. Nunca diga ao cliente "vou aplicar um desconto" — diga "vou registrar para análise da nossa equipe".

## Parâmetros

| Parâmetro | Tipo | Obrigatório | Valores aceitos |
|-----------|------|-------------|-----------------|
| `tipo_dados_cliente` | string (enum) | ✅ Sim | **Apenas** `"codigo_cliente"` ou `"id_cliente"` |
| `dado_cliente` | string | ✅ Sim | Valor real do código ou ID do cliente |
| `motivo` | string | ✅ Sim | Motivo da solicitação de renegociação (preço, concorrência, etc.) |

### ⚠️ Restrição de `tipo_dados_cliente`

Este parâmetro aceita **exatamente dois valores**. Qualquer outro valor causará erro:

| Valor | Uso |
|-------|-----|
| `"codigo_cliente"` | Quando o dado disponível é o `codigo_cliente` (ex: `1888`) |
| `"id_cliente"` | Quando o dado disponível é o `id_cliente` (ex: `1880`) |

Se um valor diferente for enviado, o retorno será:

```json
{
  "status": "error",
  "msg": "Verifique os dados informados e tente novamente!",
  "errors": [
    "O campo tipo dados cliente deve ser codigo_cliente ou id_cliente."
  ]
}
```

## Retorno esperado

```json
{
  "status": "success",
  "msg": "Solicitação de renegociação registrada com sucesso"
}
```

## Exemplos de payload para teste

Usando `codigo_cliente`:
```json
{
  "tipo_dados_cliente": "codigo_cliente",
  "dado_cliente": "1888",
  "motivo": "Cliente relata concorrência com preço menor (R$ 20 abaixo). Contrato em fidelidade, 3 meses restantes. Solicita análise de promoção de retenção."
}
```

Usando `id_cliente`:
```json
{
  "tipo_dados_cliente": "id_cliente",
  "dado_cliente": "1880",
  "motivo": "Cliente insatisfeito com velocidade entregue vs contratada. Quer renegociar plano."
}
```

## Fluxo típico (retenção por preço/concorrência)

```
1. get_cliente_by_id_servico(id_cliente_servico)     → dados contratuais
2. [agente tenta reter: empatia, apresenta benefícios]
3. [cliente insiste em desconto]
4. registrar_renegociacao(tipo_dados_cliente, dado_cliente, motivo)
5. Informar: "Registrei sua solicitação para análise. Nossa equipe entrará em contato."
6. transferir_para_humano(resumo) se necessário
```
