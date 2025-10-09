[Para PT-BR, clique aqui](#projeto-docker-devops)

# Project Docker DevOps

This project documents a web application using best practices for containerization with Docker. The goal went beyond just "making it work", focusing on creating a resilient environment, secure and agile development workflow, simulating a production-like scenario.

---

## Architecture

A classic three-tier model. Each component runs in its own container:

-  **Frontend (nginx)**: serves the interface (`index.html`) and acts as a reverse proxy → requests to `/api` are redirected to the backend.
-  **Backend (Python/Flask)**: RESTful API that communicates with DB, handling logic such as adding and listing visitors.
-  **Database (PostgreSQL)**: Data persistence using Docker volume.

---

## Technologies

-  **Containerization and orchestration**: Docker and Docker Compose
-  **Backend**: Python , Flask, Flask-SQLAlchemy, Psycopg 3
-  **Frontend**: Nginx
-  **Database**: PostgreSQL
-  **Security**: Trivy (Vulnerability scanner)
-  **Base images**: Chainguard (security and “Zero-CVE”)

## How to run

### Prerequisites
- Docker
- Docker Compose

### Execution steps

1.  **Clone the repo**

```bash
git clone https://github.com/thduran/devops-portfolio-project
cd devops-portfolio-project
```

2. **Start the containers**
Run the following in the root to build the images and start the services in background.
```bash
docker compose up -d  --build
```
  
3. **Access the app**

Go to: `http://localhost:8080`.

---

## Learning and challenges

1. **Setting up an agile development environment**

To optimize workflow, a `compose.override.yaml` file was created.

- Live reloading: using bind mount, local `./backend` folder was mapped to `/app` inside the container.
- Debug mode: the service command was modified to use the Flask development server with the `--debug` flag, enabling automatic reload on code changes.

This eliminated the need to rebuild the image after every change, speeding up development.

2. **Adding resilience with healthchecks**

`Healthchecks` were implemented to ensure stability and fault recovery.

- **Backend**: `/health` route in Flask API executes `SELECT 1` to verify connection with DB.
- **Docker Compose**: all services were configured with `restart: unless-stopped`. Additionally, using `condition: service_healthy`, the `frontend` waits for status `healthy` from `backend` before starting.
- **Result**: prevents cascading errors by ensuring the frontend doesn’t start before backend and database are ready.

3. **Secure image (zero-CVE)**

a. **Baseline**: the first backend image, based on `python:3.12-slim`, was scanned with Trivy and revealed 200+ vulnerabilities.
b. **First optimization (distroless)**: refactored to use `gcr.io/distroless/python3-debian12`, reducing the attack surface -> new scan showed 49 vulnerabilities.
c. **Final optimization (Chainguard)**: migrated to `cgr.dev/chainguard/python`, ultra-minimal and security-focused. New Trivy scan revealed zero OS-level vulnerabilities.

4. **Challenges with minimalist images**
Using a highly restricted environment introduced several build challenges:

- **Error `permission denied`**: Chainguard images run as a non-root user by default. A temporary `USER root` was added in the build stage to create the `app` user.
- **Error `pg_config not found`**: when installing psycopg2, pip couldn’t find a precompiled version and attempted to build from scratch, requiring PostgreSQL dev tools.
-- **Solution**: installed postgresql-dev and build-base via apk in the build stage. Later, the project was upgraded to psycopgv3, more robust.
- **Error `No module named flask`**: after building, the app wouldn’t start. The issue was that Python didn’t know where to look for the copied packages in the final image.
-- **Solution**: added env variable `ENV PYTHONPATH="/usr/lib/python3.12/site-packages"`, which tells Python exactly where to find installed libraries.

## Best practices and dockerfile decisions

- **Multi-stage builds**: Using a `builder` stage (with all build tools) and a `final` stage (only runtime dependencies) ensures a lightweight and secure final image.
- **Cache optimization**: `COPY requirements.txt .` is done before `COPY app.py .` so Docker doesn’t reinstall all dependencies after every source code change.
- **Understanding the base image (ENTRYPOINT):**:
-- The base image already includes a standard `ENTRYPOINT ["python3"]`, so the `CMD` only passes arguments, avoiding duplication.
- **Explicit path configuration:**:
--`ENV PATH="/usr/local/bin:${PATH}"`: ensures executables installed via `pip` (like `flask`) can be found and run.
--`ENV PYTHONPATH`: critical in minimalist images to tell Python where manually copied modules are located.

Author: Thiago Duran (thduran)

---

PT-BR:

# Projeto Docker DevOps

Este projeto documenta uma aplicação web, utilizando as melhores práticas de containerização com Docker. O objetivo foi além de "fazer funcionar", focando em criar um ambiente resiliente, seguro e com um fluxo de desenvolvimento ágil, simulando cenário de produção.

---

## Arquitetura

Modelo clássico de três camadas. Cada componente é executado em seu próprio container:

-  **Frontend (nginx)**: Serve a interface (`index.html`) e atua como proxy reverso -> requisições para `/api` são redirecionadas pro backend.
-  **Backend (Python/Flask)**: API RESTful que se comunica com o BD, responsável pela lógica, como adicionar e listar visitantes.
-  **Banco de Dados (PostgreSQL)**: Persistência dos dados em volume Docker.

---

## Tecnologias

-  **Containerização e orquestração**: Docker e Docker Compose
-  **Backend**: Python, Flask, Flask-SQLAlchemy, Psycopg 3
-  **Frontend**: Nginx
-  **Banco de dados**: PostgreSQL
-  **Segurança**: Trivy (Scanner de vulnerabilidades)
-  **Imagens base**: Chainguard (segurança e "zero-CVE")

---

## Como executar

### Pré-requisitos
- Docker
- Docker Compose

### Passos para execução

1.  **Clone o repositório**

```bash
git clone https://github.com/thduran/devops-portfolio-project
cd devops-portfolio-project
```

2. **Suba os containers**
Execute o comando na raiz do projeto para construir as imagens e iniciar os serviços em segundo plano.
```bash
docker compose up -d  --build
```
  
3. **Acesse a app**

Acesse: `http://localhost:8080`.


## Aprendizado e desafios

1. **Configurando ambiente de desenvolvimento ágil**

Para otimizar o fluxo de trabalho, foi criado um arquivo `compose.override.yaml`.

- Live reloading: Usando bind mount, a pasta local `./backend` foi mapeada para a pasta `/app` do container.
- Modo debug: O comando do serviço foi alterado pra usar o servidor de desenvolvimento do Flask com a flag `--debug`, que reinicia automaticamente a cada alteração no código.

Isso eliminou a necessidade de reconstruir a imagem a cada mudança, acelerando desenvolvimento.

2. **Adicionando resiliência com healthchecks**

Foram implementados `healthchecks` para garantir estabilidade e recuperação de falhas.

- **Backend**: rota `/health` na API Flask que executa `SELECT 1` pra verificar conexão com BD.
- **Docker Compose**: todos os serviços foram configurados com `restart: unless-stopped`. Além disso, com `condition: service_healthy`, o serviço `frontend` espera status `healthy` do `backend` antes de iniciar.
- **Resultado**: evita erros em cascata, pois previne que o frontend inicie antes que o backend e o BD.

3. **Imagem segura (zero-CVE)**

a. **Linha de base**: a primeira imagem do backend, baseada em `python:3.12-slim`, foi escaneada com o Trivy e revelou 200+ vulnerabilidades.
b. **Primeira otimização (distroless)**: imagem refatorada pra usar `gcr.io/distroless/python3-debian12`, reduzindo a superfície de ataque -> novo scan mostrou 49 vulnerabilidades.
c. **Nova otimização (chainguard)**: a imagem foi migrada para `cgr.dev/chainguard/python`, por ser ultra enxuta e focada em segurança. Novo scan com o Trivy revelou zero vulnerabilidades de SO.

4. **Desafios da imagem minimalista**
Por ser um ambiente extremamente restrito, a troca da imagem trouxe desafios no processo de build:

- **Erro `permission denied`**: a imagem da Chainguard, por segurança, roda com um usuário não-root por padrão. `USER root` temporário foi adicionado no estágio de build para permitir a criação do usuário `app`.
- **Erro `pg_config not found`**: ao tentar instalar o psycopg2, o pip não encontrou uma versão pré-compilada e tentou compilá-la do zero. Para isso, precisava das ferramentas de desenvolvimento do PostgreSQL.
-- **Solução**: instalação de postgresql-dev e build-base via apk no estágio de build pra permitir a compilação. Depois, o projeto foi modernizado pra usar psycopgv3, que é mais robusta.
- **Erro `No module named flask`**: após build, a aplicação não iniciava. A causa era que o Python na imagem final não sabia onde procurar os pacotes que haviam sido copiados.
-- **Solução**: sdicionada variável de ambiente `ENV PYTHONPATH="/usr/lib/python3.12/site-packages"`, que diz ao Python onde exatamente encontrar as bibliotecas instaladas.

  
## Boas práticas e decisões no dockerfile

- **Multi-stage builds**: o uso de estágio `builder` (com todas as ferramentas de compilação) e um estágio `final` (só com o necessário pra executar) garante uma imagem final leve e segura.
- **Uso de cache**: `COPY requirements.txt .` é feito antes de `COPY app.py .` pra que o Docker não precise reinstalar todas as dependências a cada mudança no código-fonte.
- **Entendimento da imagem base (ENTRYPOINT)**:
-- A imagem já possui um `ENTRYPOINT ("python3")` padrão. Por isso, o `CMD` omite isso e passa só os argumentos, evitando duplicação.
- **Configuração explícita de paths**:
--`ENV PATH="/usr/local/bin:${PATH}"`: garante que os executáveis instalados pelo `pip` (como `flask`) possam ser encontrados e executados.
--`ENV PYTHONPATH`: essencial em imagens minimalistas pra dizer ao Python onde encontrar os módulos copiados manualmente.

Autor: Thiago Duran (thduran)