# Custom Tool: `get_cliente_by_dados`

**Tipo:** Custom Tool HTTP
**Endpoint:** `GET /api/v1/integracao/cliente`

## Usado por

- **Agente Financeiro**

## Como funciona a validação de 2 fatores

Esta tool **não valida 2 fatores automaticamente** — ela faz uma busca por CPF/CNPJ e retorna os dados do cliente. A validação do segundo fator é feita pelo **agente**, comparando o dado informado pelo cliente com os campos do retorno.

**Fluxo:**
1. Agente coleta CPF + segundo fator (data de nascimento, nome ou telefone) do cliente
2. Agente chama `get_cliente_by_dados(cpf_cnpj=<CPF sem máscara>)`
3. Agente compara o segundo fator informado com `data_nascimento`, `nome_razaosocial` ou `telefone_primario` do retorno
4. Se conferir → usa `id_cliente_servico` nas próximas tools
5. Se não conferir → não prossegue, pede os dados novamente

## Argumento exposto ao agente

| Argumento | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `cpf_cnpj` | string | ✅ Sim | CPF ou CNPJ — **apenas dígitos, sem máscara** |

## Configuração HTTP no Evo CRM (query params)

| Query param | Valor | Tipo |
|-------------|-------|------|
| `busca` | `cpf_cnpj` | Fixo (hardcoded na config da tool) |
| `termo_busca` | `{cpf_cnpj}` | Dinâmico — mapeado do argumento `cpf_cnpj` |

> O agente passa apenas `cpf_cnpj`. A tool injeta `busca=cpf_cnpj` automaticamente. Não expor `busca` como argumento do agente.

## Campos do retorno para validação do segundo fator

| Campo | Caminho | Segundo fator validado |
|-------|---------|----------------------|
| `data_nascimento` | `clientes[0].data_nascimento` | Data de nascimento |
| `nome_razaosocial` | `clientes[0].nome_razaosocial` | Nome completo |
| `telefone_primario` | `clientes[0].telefone_primario` | Telefone cadastrado |
| `id_cliente_servico` | `clientes[0].servicos[0].id_cliente_servico` | Usar após validação |

## Quando usar

**Sempre antes de:**
- `get_faturas_pendentes`
- `request_desbloqueio_confianca`

## Exemplo de payload para teste (botão Testar do Evo CRM)

```json
{
  "cpf_cnpj": "00096437022"
}
```

## Nota LGPD

Nas respostas ao cliente, mascare CPFs e CNPJs (ex: `***.456.789-**`). Não exiba o CPF completo mesmo que disponível no retorno.
