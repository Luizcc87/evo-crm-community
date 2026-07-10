# Guia: Cadastro do Catálogo de Produtos ISP no Evo CRM

> **Requer:** Evo CRM v1.0.0-rc3+  
> **Permissão necessária:** `products.manage`

Os agentes de Vendas (Fibra e Móvel) consultam o catálogo de Produtos do Evo CRM em runtime via Native Tool `link_product_to_pipeline_item`. Não é preciso manter listas de planos nos prompts — qualquer alteração de preço ou descrição reflete na próxima conversa automaticamente.

---

## Conceitos-chave

| Conceito | Uso no ISP |
|---|---|
| **Produto** | Um plano de internet ou celular (ex: "Fibra 300MB Residencial") |
| **Variante** | Opcional — use se o mesmo plano tiver versões (ex: mensal vs anual) |
| **SKU** | Coloque o `id_servico` do HubSoft — é o identificador que o agente repassa na venda |
| **Status** | Apenas produtos `ativo` ficam visíveis para vinculação ao agente |
| **Descrição** | O agente usa esse texto para o pitch de up-sell — seja descritivo com benefícios |

---

## Passo a Passo: Criar um Produto

1. Menu principal → **Produtos** → **Novo Produto**
2. Preencha os campos:

| Campo | Orientação |
|---|---|
| **Nome** | Nome comercial do plano (ex: `Fibra 300MB LOG BLACK`) |
| **Descrição** | Benefícios que o agente deve destacar (ex: `Ideal para streaming 4K e home office. Inclui roteador Wi-Fi 6 sem custo.`) |
| **Preço** | Valor mensal em R$ |
| **SKU** | `id_servico` do HubSoft (consulte `GET /api/v1/integracao/configuracao/servico`) |
| **Status** | `Ativo` — obrigatório para aparecer na vinculação ao agente |

3. Clique em **Salvar**

---

## Estrutura Recomendada para ISP

### Fibra Residencial

| Nome do Produto | SKU (id_servico) | Preço | Descrição resumida |
|---|---|---|---|
| Fibra 100MB Residencial | `id_servico HubSoft` | R$ XX | Plano entrada, até 3 dispositivos simultâneos |
| Fibra 300MB Residencial | `id_servico HubSoft` | R$ XX | Streaming HD e home office, roteador incluído |
| Fibra 500MB Residencial | `id_servico HubSoft` | R$ XX | Streaming 4K, vídeos simultâneos, jogos online |
| Fibra 1GB Residencial | `id_servico HubSoft` | R$ XX | Máxima velocidade, múltiplos usuários |

### Fibra Empresarial

| Nome do Produto | SKU (id_servico) | Preço | Descrição resumida |
|---|---|---|---|
| Fibra Empresarial 300MB | `id_servico HubSoft` | R$ XX | SLA garantido, suporte prioritário |
| Fibra Empresarial 500MB | `id_servico HubSoft` | R$ XX | SLA + IP fixo, ideal para câmeras e VPN |
| Fibra Empresarial 1GB | `id_servico HubSoft` | R$ XX | SLA + IP fixo + suporte dedicado 24h |

### Telefonia Móvel

| Nome do Produto | SKU (id_servico) | Preço | Descrição resumida |
|---|---|---|---|
| Plano Móvel 5GB | `id_servico HubSoft` | R$ XX | WhatsApp e redes sociais inclusos |
| Plano Móvel 15GB | `id_servico HubSoft` | R$ XX | Streaming e videochamadas no mês inteiro |
| Plano Móvel 30GB | `id_servico HubSoft` | R$ XX | Heavy user, dados de sobra o mês todo |

> Para descobrir os `id_servico` disponíveis no HubSoft: execute `GET /api/v1/integracao/configuracao/servico` e filtre por `servico_tecnologia`:
> - `id_servico_tecnologia: 4` → FIBRA ÓPTICA
> - `id_servico_tecnologia: 21` → TELEFONIA (móvel)
>
> Consulte também `docs/hubsoft-integration/test-results/README.md`.

---

## Como o Agente Usa os Produtos

1. Ao ser ativado, o agente recebe o catálogo vinculado injetado no contexto
2. Durante a conversa, apresenta os planos com base no perfil do cliente
3. Quando o cliente confirma interesse em um plano, chama `link_product_to_pipeline_item(product_id)` — registra automaticamente no pipeline de vendas
4. Gera resumo e chama `transferir_para_humano(resumo)` para o time comercial finalizar

**Dica de up-sell:** coloque na descrição de cada produto a comparação com o plano superior. O agente usa esse texto para argumentar o upgrade.

---

## Vinculando Produtos ao Agente

Após criar os produtos no catálogo:

1. Acesse **Agentes** → **⋯ Actions** → **Edit** no agente desejado
2. Acesse a aba **Produtos**
3. Selecione os produtos que o agente deve conhecer:
   - **Vendas Fibra**: selecione todos os planos de fibra (residencial + empresarial)
   - **Vendas Móvel**: selecione todos os planos de telefonia
4. Clique em **Save**

> Mudanças no catálogo (novo plano, ajuste de preço) refletem na próxima conversa **sem reconfigurar o prompt do agente**.

---

## Referências

- Doc oficial: [Visão Geral de Produtos](https://docs.evolutionfoundation.com.br/user-guides/products/overview)
- Endpoints HubSoft para descobrir `id_servico`: `docs/hubsoft-integration/test-results/README.md`
- Script de teste: `scripts/hubsoft-api-tests/test_vendas.py`
