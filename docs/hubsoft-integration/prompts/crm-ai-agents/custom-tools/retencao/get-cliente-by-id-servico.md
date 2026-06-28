# Custom Tool: `get_cliente_by_id_servico`

**Tipo:** Custom Tool HTTP
**Endpoint:** HubSoft — dados do cliente por ID de serviço

## Usado por

- **Agente de Retenção**

## Diferença em relação a `get_cliente_by_cpf` (Suporte)

| Aspecto | `get_cliente_by_id_servico` (Retenção) | `get_cliente_by_cpf` (Suporte) |
|---------|----------------------------------------|-------------------------------|
| Input | `id_cliente_servico` (já conhecido do handoff) | `cpf_cnpj` (buscado quando não veio no handoff) |
| Contexto | Cliente chegou transferido com ID já disponível | Identificação necessária antes do diagnóstico |
| Foco dos campos | `data_inicio_contrato`, `vigencia_meses` (fidelidade/multa) | `status_prefixo`, `ultima_conexao` (diagnóstico técnico) |

O Agente de Retenção **recebe o `id_cliente_servico` no handoff** do Orquestrador. Usa esta tool para enriquecer o contexto com dados contratuais, não para identificar o cliente.

## Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `id_cliente_servico` | integer | ✅ Sim | Identificador do serviço — vem do handoff do Orquestrador |

## Campos relevantes para retenção

| Campo | Tipo | Uso |
|-------|------|-----|
| `data_inicio_contrato` | string | Data de início — para calcular tempo de contrato |
| `vigencia_meses` | integer | Prazo de fidelidade em meses — para avaliar multa rescisória |

### Cálculo de multa rescisória

```
meses_decorridos = diferença entre data_inicio_contrato e hoje
está_em_fidelidade = meses_decorridos < vigencia_meses
```

Se `está_em_fidelidade == true`, o agente deve avisar sobre possível multa antes de prosseguir com o cancelamento.

## Retorno esperado

```json
{
  "status": "success",
  "msg": "Dados consultados com sucesso",
  "cliente": {
    "id_cliente_servico": 2491,
    "nome_razaosocial": "NOME DO CLIENTE",
    "data_inicio_contrato": "2024-01-15",
    "vigencia_meses": 12,
    "valor": 120,
    "nome_plano": "PLANO_NOME"
  }
}
```

## Exemplo de payload para teste

```json
{
  "id_cliente_servico": 2491
}
```
