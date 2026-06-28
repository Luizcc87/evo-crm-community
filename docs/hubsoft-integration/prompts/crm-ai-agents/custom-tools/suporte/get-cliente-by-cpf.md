# Custom Tool: `get_cliente_by_cpf`

**Tipo:** Custom Tool HTTP
**Endpoint:** `GET /api/v1/integracao/cliente?busca=cpf_cnpj&termo_busca={cpf}&limit=1&cancelado=nao&ultima_conexao=sim`

## Usado por

- **Agente de Suporte Técnico** — quando `id_cliente_servico` não vem no handoff do Orquestrador

## Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `cpf_cnpj` | string | ✅ Sim | CPF ou CNPJ do cliente — **apenas dígitos, sem formatação** |

### ⚠️ Regra crítica: CPF/CNPJ sem máscara

Remova toda formatação **antes** de chamar a tool:

| Input do cliente | Enviar para a tool |
|------------------|--------------------|
| `"123.456.789-09"` | `"12345678909"` |
| `"12.345.678/0001-99"` | `"12345678000199"` |
| `"12345678909"` | `"12345678909"` (já correto) |

Enviar CPF com pontuação causará resultado incorreto ou sem retorno.

## Campos do retorno relevantes para o agente

O retorno vem dentro de `clientes[0]` (array, mas limit=1). Campos críticos:

| Campo | Caminho | Uso |
|-------|---------|-----|
| `id_cliente_servico` | `clientes[0].servicos[0].id_cliente_servico` | **Chave universal** — usar em todas as tools seguintes |
| `alerta` | `clientes[0].alerta` | `true` = há comunicado a informar ao cliente antes do diagnóstico |
| `alerta_mensagens` | `clientes[0].alerta_mensagens[]` | Textos do comunicado (massiva, manutenção) |
| `status_prefixo` | `clientes[0].servicos[0].status_prefixo` | Status do serviço — ver tabela abaixo |
| `ultima_conexao.conectado` | `clientes[0].servicos[0].ultima_conexao.conectado` | `true` = online no HubSoft, `false` = offline |
| `ultima_conexao.status_txt` | `clientes[0].servicos[0].ultima_conexao.status_txt` | Texto pronto para enviar ao cliente |

### Valores de `status_prefixo` e ação

| `status_prefixo` | Significado | Ação do agente |
|-----------------|-------------|----------------|
| `"servico_habilitado"` | Serviço ativo | Prosseguir diagnóstico |
| `"suspenso_inadimplencia"` | Bloqueado por inadimplência | Informar e transferir para Financeiro — não abrir OS |
| Outros | Verificar com supervisor | Transferir para humano |

### Lógica pós-retorno

```
1. alerta == true → informar alerta_mensagens[] antes do diagnóstico
2. status_prefixo == "suspenso_inadimplencia" → encaminhar para Financeiro
3. ultima_conexao.conectado == true → equipamento online no HubSoft; orientar testes no lado do cliente
4. ultima_conexao.conectado == false → equipamento offline; chamar get_extrato_conexao
5. Em qualquer caso: usar status_txt para comunicar tempo de conexão/desconexão ao cliente
```

## Retorno esperado

```json
{
  "status": "success",
  "msg": "Dados consultados com sucesso",
  "clientes": [
    {
      "id_cliente": 1880,
      "nome_razaosocial": "NOME COMPLETO DO CLIENTE",
      "alerta": false,
      "alerta_mensagens": [],
      "servicos": [
        {
          "id_cliente_servico": 2491,
          "status": "Serviço Habilitado",
          "status_prefixo": "servico_habilitado",
          "ultima_conexao": {
            "conectado": true,
            "ultima_conexao_datetime": "2026-05-25 19:14:26-03",
            "status_txt": "CONECTADO HÁ 0 MES(ES), 1 DIA(S), 22 HORA(S) e 44 MINUTO(S) - 100.65.1.57"
          }
        }
      ]
    }
  ]
}
```

## Exemplo de payload para teste

```json
{
  "cpf_cnpj": "12345678909"
}
```

## Edge case: CPF com formatação

Se o cliente enviar `"123.456.789-09"` e o agente não remover a máscara antes de chamar a tool, o retorno será `clientes: []` ou erro. O agente deve sempre sanitizar o input antes de chamar a tool.
