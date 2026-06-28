# Custom Tool: `link_product_to_pipeline_item`

**Tipo:** Native Tool (não HTTP)
**Aba de configuração:** Produtos do agente no Evo CRM

> ⚠️ **Esta é uma Native Tool**, não uma Custom Tool HTTP. Não possui endpoint HTTP configurado na aba Custom Tools. É configurada diretamente na aba **Produtos** do agente no Evo CRM.

## Usado por

- **Agente de Vendas Fibra**
- **Agente de Vendas Móvel**

## Como funciona

O catálogo de planos (produtos) é injetado automaticamente no contexto do agente em runtime pelo Evo CRM, via aba Produtos. Cada produto tem um `product_id` que corresponde ao `id_servico` no HubSoft. O agente não "busca" o catálogo — ele está disponível no contexto quando o agente é invocado.

## Parâmetros

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `product_id` | integer | ✅ Sim | ID do produto escolhido — vem do catálogo injetado no contexto (aba Produtos do agente) |

> **`product_id` = `id_servico` no HubSoft.** Não oferte planos fora do catálogo injetado em runtime.

## Quando chamar

Após o cliente **confirmar o plano escolhido**, antes de chamar `transferir_para_humano`. Sequência obrigatória:

```
1. Cliente confirma o plano
2. link_product_to_pipeline_item(product_id)  ← vincula ao pipeline
3. transferir_para_humano(resumo)              ← time comercial finaliza
```

## Retorno

Native Tools do Evo CRM não retornam payload a processar. A tool apenas registra a associação entre o item de pipeline ativo e o produto selecionado.

## Exemplo de payload para teste

```json
{
  "product_id": 32
}
```

(Onde `32` é o `id_servico` do plano escolhido no catálogo HubSoft injetado no agente.)

## Notas de configuração

- Não criar endpoint HTTP para esta tool
- Configurar na aba **Produtos** do agente no Evo CRM
- O catálogo deve estar sincronizado com os planos ativos do HubSoft (`id_servico`)
