# HubSoft API Testing Party Mode Prompt

Este prompt foi desenhado para invocar múltiplos agentes trabalhando juntos (Party Mode) para evoluir a pesquisa em testes práticos.

**Como usar:**
Copie o bloco de texto abaixo e cole no chat para iniciar a execução.

```text
/evo-party-mode Invoque os agentes evo-architect, evo-dev, evo-qa e evo-tech-writer para uma sessão conjunta.

**Objetivo:**
Analisar a documentação existente sobre a API do HubSoft (em `docs/hubsoft-integration`), criar scripts locais de comunicação real com a API, executar ou preparar esses testes, e documentar os resultados e padrões descobertos.

**Passo a passo esperado da equipe:**
1. **evo-architect**: Defina a estrutura de diretórios em `scripts/hubsoft-api-tests` (ou semelhante) e `docs/hubsoft-integration/test-results` para organizar os scripts de teste e as saídas.
2. **evo-dev**: Desenvolva scripts reais (ex: Node.js, Python ou cURL/Shell) capazes de autenticar e consultar endpoints vitais descritos no `technical-research-api-hubsoft.md` (como obter token, listar clientes, etc). O código deve estar preparado para receber as credenciais de forma segura (via `.env`).
3. **evo-qa**: Revise os scripts para garantir que existam asserções adequadas (status codes, formato da resposta JSON, tratamento de erros de autenticação).
4. **evo-tech-writer**: Após a criação e (se possível) execução dos testes com dados simulados ou sandbox, gere os arquivos de documentação com os resultados e *payloads* em `docs/hubsoft-integration/test-results`.

Por favor, debatam brevemente a melhor linguagem/ferramenta para os scripts de teste, entrem em um consenso e procedam com a criação dos arquivos de forma colaborativa!
```
