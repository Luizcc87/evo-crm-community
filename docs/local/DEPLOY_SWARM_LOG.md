# Histórico de Resolução de Problemas: Deploy Swarm Local

Durante o setup e estabilização do ambiente Windows/Docker Desktop do Evo-CRM Community rodando em Docker Swarm (`deploy/local`), enfrentamos diversos gargalos comuns de infraestrutura. Este arquivo registra a causa e a respectiva solução de cada evento para poupar tempo em futuras manutenções.

## 1. Conflito de Nomes no DNS do Swarm
* **Sintoma**: Ao iniciar o stack `evo-crm-db`, o DNS interno falhava ao resolver o nome do host (ex: o core não achava o banco).
* **Causa**: O Docker Swarm possui uma limitação de roteamento se o nome do serviço for exato ao nome do repositório/stack inteiro em casos específicos de overload de overlay network.
* **Solução**: Desmembramos a infraestrutura para arquivos independentes (`stack.db.yml` e `stack.redis.yml`) e renomeamos os serviços de `evo-crm-db` para simplesmente `postgres` e `cache`. A comunicação agora é feita explicitamente via rede externa.

## 2. Erro de Inicialização do Processor (DuplicateTableError vs MissingGreenlet)
* **Sintoma**: O serviço `evo_processor` falhava repetitivamente em looping gerando crashes na subida do container.
* **Causa Histórica**: 
  1. Primeiro, observamos a falha `DuplicateTableError` vindo do comando `alembic upgrade head`, o que revelava que múltiplas réplicas/tentativas rodavam as migrações concorrentes. Resolvemos isolando isso com verificações lógicas no comando do Docker.
  2. Depois, para evitar alertas, mudamos a connection string para `postgresql+asyncpg://`. O boot falhou em seguida com um erro `MissingGreenlet: greenlet_spawn has not been called`. Isso acontece porque a API (FastAPI) em seu arquivo `main.py` roda de forma síncrona a inicialização das tabelas (`Base.metadata.create_all()`). O driver `asyncpg` bloqueia transações síncronas se o ambiente verde (greenlet) não estiver ativado.
* **Solução**: Voltamos ao uso do driver assíncrono transparente padrão (`postgresql://`), o qual por baixo dos panos na imagem já suporta o parse das tabelas pelo `psycopg2` e evita a falha `MissingGreenlet`.

## 3. Rejeição de Imagens (Swarm: "No such image")
* **Sintoma**: Os logs relatavam continuamente `State message: rejected` devido a `Error message: No such image: [xyz]`.
* **Causa**: Estávamos lidando com o fork local (onde usamos a conta Docker Hub `lc1868`) versus a base do oficial (`evoapicloud`). A imagem principal da infra `evo-ai-crm-community` nunca foi construída para a conta `lc1868`, causando rejeição generalizada pelo orchestrador quando se tentava deploy pela pipeline automática.
* **Solução**: Mapeamos a Fonte da Verdade local (`IMAGE_REGISTRY_MAP.md`). As imagens intocadas do core assumiram a proveniência original (`evoapicloud`) e as imagens modificadas pela equipe voltaram exclusivamente para `lc1868` em `latest` / `1.0.0`.

## 4. Chaves Criptográficas Inválidas (Fernet base64)
* **Sintoma**: O Core falhava dizendo que a `ENCRYPTION_KEY` era inválida.
* **Causa**: O algoritmo Fernet pede obrigatoriamente um base64 the 32-bytes decodificado. Estávamos passando textos limpos como secret.
* **Solução**: Configurada uma chave fernet compatível com a biblioteca padrão (gerada de forma canônica) nas variáveis dos arquivos locaux (`stack_evo-crm.local.yaml`).

## 5. Saúde e Resiliência (Healthcheck Falsos e Paridade de ENV)
* **Sintoma**: O Node Sidekiq (Auth e CRM) morria dizendo "Unhealthy" apesar do log estar limpo e rodando e o boot do Auth falhava enviando e-mail.
* **Causa**: Sidekiq workers não têm endpoints abertos web para curl, e as variáveis SMTP estavam faltando entre arquivos do Swarm versus arquivos da Local.
* **Solução**: Mapeamento espelhado obrigatório de todas as variáveis vitais (`JWT`, `Doorkeeper`, `MFA`, `SMTP`, etc) entre apps web e seus respectivos Sidekiqs. E a declaração de `disable: true` no healthcheck de containers unicamente processadores de fila.
