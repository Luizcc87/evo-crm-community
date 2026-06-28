# Custom Tools — Agentes HubSoft: Índice

Mapa completo de todas as Custom Tools configuradas nos agentes de IA do Evo CRM para a integração HubSoft.

> **Nota:** As tools `transferir_para_financeiro`, `transferir_para_suporte`, `transferir_para_vendas_fibra`, `transferir_para_vendas_movel` e `transferir_para_retencao` são **Native Tools de sub-agent routing** — configuradas na aba **Sub Agents** do Evo CRM, não na aba Custom Tools. Não constam neste índice. Apenas `transferir_para_humano` é Custom Tool HTTP real.

## Tools Compartilhadas (`shared/`)

| Tool | Tipo | Agente(s) | Doc |
|------|------|-----------|-----|
| `transferir_para_humano` | Custom HTTP | Orquestrador, Suporte, Financeiro, Vendas Fibra, Vendas Móvel, Retenção | [transferir-para-humano.md](shared/transferir-para-humano.md) |
| `get_faturas_pendentes` | Custom HTTP | Suporte, Financeiro | [get-faturas-pendentes.md](shared/get-faturas-pendentes.md) |
| `get_tipo_atendimento_by_nome` | Custom HTTP | Suporte, Retenção | [get-tipo-atendimento-by-nome.md](shared/get-tipo-atendimento-by-nome.md) |
| `link_product_to_pipeline_item` | **Native Tool** | Vendas Fibra, Vendas Móvel | [link-product-to-pipeline-item.md](shared/link-product-to-pipeline-item.md) |

## Agente Suporte (`suporte/`)

| Tool | Tipo | Doc |
|------|------|-----|
| `get_cliente_by_cpf` | Custom HTTP | [get-cliente-by-cpf.md](suporte/get-cliente-by-cpf.md) |
| `get_ultima_conexao` | Custom HTTP | [get-ultima-conexao.md](suporte/get-ultima-conexao.md) |
| `get_extrato_conexao` | Custom HTTP | [get-extrato-conexao.md](suporte/get-extrato-conexao.md) |
| `get_cpe_info` | Custom HTTP | [get-cpe-info.md](suporte/get-cpe-info.md) |
| `abrir_os_suporte` | Custom HTTP | [abrir-os-suporte.md](suporte/abrir-os-suporte.md) |

## Agente Financeiro (`financeiro/`)

| Tool | Tipo | Doc |
|------|------|-----|
| `get_cliente_by_dados` | Custom HTTP | [get-cliente-by-dados.md](financeiro/get-cliente-by-dados.md) |
| `request_desbloqueio_confianca` | Custom HTTP | [request-desbloqueio-confianca.md](financeiro/request-desbloqueio-confianca.md) |

## Agente Retenção (`retencao/`)

| Tool | Tipo | Doc |
|------|------|-----|
| `get_cliente_by_id_servico` | Custom HTTP | [get-cliente-by-id-servico.md](retencao/get-cliente-by-id-servico.md) |
| `registrar_renegociacao` | Custom HTTP | [registrar-renegociacao.md](retencao/registrar-renegociacao.md) |
| `abrir_os_cancelamento` | Custom HTTP | [abrir-os-cancelamento.md](retencao/abrir-os-cancelamento.md) |

## Padrões Globais

- Retornos sempre têm `status: "success" | "error"` + `msg`
- `id_cliente_servico` é o identificador universal entre tools — obtido em `get_cliente_by_cpf` ou no handoff
- CPF/CNPJ enviado **apenas dígitos**, sem máscara (`"12345678909"`, não `"123.456.789-09"`)
- `apenas_pendente` é string `"sim"`, não boolean
- `abrir_os` é boolean que controla geração de OS vs só protocolo
