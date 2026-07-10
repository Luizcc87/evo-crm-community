# Custom Tool: `abrir_os_suporte`

**Tipo:** Custom Tool HTTP
**Endpoint:** `POST /api/v1/integracao/atendimento`

## Usado por

- **Agente de Suporte Técnico**

## Pré-requisito

Antes de chamar esta tool, obrigatoriamente chame `get_tipo_atendimento_by_nome("suporte técnico")` para obter o `id_tipo_atendimento`. Nunca assuma um valor fixo para esse ID.

## Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `id_cliente_servico` | integer | ✅ Sim | Identificador do serviço do cliente |
| `id_tipo_atendimento` | integer | ✅ Sim | Obtido via `get_tipo_atendimento_by_nome("suporte técnico")` |
| `descricao` | string | ✅ Sim | Sintomas detalhados: problema relatado, dados de conexão, resultado do diagnóstico |
| `abrir_os` | boolean | ✅ Sim | `true` = gerar OS para técnico; `false` = apenas protocolo de atendimento |

## Quando usar `abrir_os: true` vs `false`

| Situação | `abrir_os` |
|----------|------------|
| `conectado == false` + problema confirmado no HubSoft | `true` |
| Cliente relata problema mas `conectado == true` (problema intermitente ou local) | `false` (protocolo apenas) |
| Problema confirmado que requer visita técnica | `true` |

## Retorno esperado

```json
{
  "status": "success",
  "id_atendimento": 9901,
  "protocolo": "202605270001",
  "ordens_servico": [
    {
      "id_ordem_servico": 4401,
      "numero_ordem_servico": "OS-2026-4401",
      "status": "Aguardando",
      "tecnico": null
    }
  ]
}
```

> `ordens_servico[]` **só aparece** quando `abrir_os: true`. Com `abrir_os: false`, o array não é retornado.

## Campos relevantes do retorno

| Campo | Uso |
|-------|-----|
| `protocolo` | Número a informar ao cliente como comprovante |
| `id_atendimento` | Referência interna do atendimento |
| `ordens_servico[0].numero_ordem_servico` | Número da OS (quando gerada) |

## Exemplo de payload para teste

Com OS (problema confirmado offline):
```json
{
  "id_cliente_servico": 2491,
  "id_tipo_atendimento": 7,
  "descricao": "Cliente relata falta total de conexão. Diagnóstico: conectado=false no HubSoft desde 25/05/2026 19:14. Extrato mostra queda abrupta sem reconexão. Sinal ONU perdido. Necessária visita técnica.",
  "abrir_os": true
}
```

Sem OS (só protocolo):
```json
{
  "id_cliente_servico": 2491,
  "id_tipo_atendimento": 7,
  "descricao": "Cliente relata lentidão ocasional. HubSoft mostra conectado=true. Orientado a reiniciar roteador e verificar cabos. Problema persiste segundo cliente.",
  "abrir_os": false
}
```

## Fluxo completo encadeado

```
1. get_cliente_by_cpf(cpf_cnpj)                      → id_cliente_servico
2. [diagnóstico: conectado=false]
3. get_extrato_conexao(id_cliente_servico)            → histórico
4. get_tipo_atendimento_by_nome("suporte técnico")    → id_tipo_atendimento
5. abrir_os_suporte(id_cliente_servico, id_tipo_atendimento, descricao, abrir_os=true)
6. Informar protocolo ao cliente
```

## Nota

Não prometa previsão de restabelecimento. Informe apenas o número do protocolo e, se OS aberta, que um técnico entrará em contato.
