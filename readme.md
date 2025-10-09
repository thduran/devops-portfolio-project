
# Projeto Docker DevOps

Este projeto documenta a criação, orquestração e otimização de uma aplicação web full-stack, utilizando as melhores práticas de containerização com Docker. O objetivo principal foi além de simplesmente "fazer funcionar", focando em criar um ambiente resiliente, seguro e com um fluxo de desenvolvimento ágil, simulando um cenário de produção moderno.

---

## Arquitetura da Aplicação

A aplicação é arquitetada em um modelo clássico de três camadas, onde cada componente é executado em seu próprio contêiner:

-  **Frontend (Nginx)**: Serviço responsável por servir a interface do usuário (`index.html`) e atuar como Reverse Proxy. Todas as requisições para `/api` são redirecionadas para o backend.
-  **Backend (Python/Flask)**: API RESTful que se comunica com o banco de dados, responsável por toda a lógica de negócio, como adicionar e listar visitantes.
-  **Banco de Dados (PostgreSQL)**: Garantia de persistência dos dados em um volume Docker, evitando perda de dados caso o contêiner seja recriado.

---

## Tecnologias Utilizadas

-  **Containerização e Orquestração**: Docker & Docker Compose
-  **Backend**: Python, Flask, Flask-SQLAlchemy, Psycopg 3
-  **Frontend**: Nginx
-  **Banco de Dados**: PostgreSQL
-  **Segurança**: Trivy (Scanner de Vulnerabilidades)
-  **Imagens Base**: Chainguard (Segurança e "Zero-CVE")

---

## Como Executar o Projeto

### Pré-requisitos
- Docker
- Docker Compose

### Passos para Execução

1.  **Clone o Repositório**

```bash
git  clone <url-do-seu-repositorio>
cd <nome-do-repositorio>
```

2. **Configure as Variáveis de Ambiente**
Crie  um  arquivo  `.env`  na  raiz  do  projeto  copiando  o  conteúdo  do  arquivo  `Código.txt`.
Ele  contém  as  credenciais  do  banco  de  dados  e  é  lido  automaticamente  pelo  Docker  Compose.

3. **Suba os Contêineres**
Execute o comando abaixo na raiz do projeto. Ele irá construir as imagens e iniciar todos os serviços em segundo plano.
```bash
docker compose up -d  --build
```
  
4. **Acesse a Aplicação**

Abra seu navegador e acesse: `http://localhost:8080`.


## Jornada de Aprendizado e Desafios Superados
Esta seção detalha a evolução do projeto, os desafios encontrados e as soluções aplicadas, que representam o principal aprendizado desta jornada.

1. **Configurando um Ambiente de Desenvolvimento Ágil**

Para otimizar o fluxo de trabalho, foi criado um arquivo ```bashcompose.override.yaml```.

- Live Reloading: Usando um bind mount, a pasta local `./backend` foi mapeada para a pasta `/app` dentro do contêiner.
- Modo Debug: O comando do serviço foi alterado para usar o servidor de desenvolvimento do Flask com a flag `--debug`, que reinicia automaticamente a cada alteração no código.

Isso eliminou a necessidade de reconstruir a imagem a cada mudança, acelerando drasticamente o ciclo de desenvolvimento.

2. **Adicionando Resiliência com Healthchecks**

Para garantir que a aplicação subisse de forma estável e se recuperasse de falhas, foram implementados `healthchecks`:

 - **Backend**: Foi criada uma rota `/health` na API Flask que executa uma consulta simples (`SELECT 1`) para verificar a conexão com o banco de dados.
- **Docker Compose**: Todos os serviços foram configurados com `restart: unless-stopped`. Além disso, o serviço `frontend` foi instruído a esperar que o `backend` estivesse `healthy` antes de iniciar (`condition: service_healthy`).
- **Resultado**: Isso previne que o frontend inicie antes que o backend e o banco de dados estejam totalmente prontos, evitando erros em cascata.

3. **O Caminho para uma Imagem Segura (Zero-CVE)**

Este foi o maior desafio e o maior aprendizado do projeto.

a. **Linha de Base**: A primeira versão da imagem do backend, baseada em `python:3.12-slim`, foi escaneada com o Trivy e revelou mais de 220 vulnerabilidades.
b. **Primeira Otimização (Distroless)**: A imagem foi refatorada para usar a base `gcr.io/distroless/python3-debian12`. Isso reduziu drasticamente a superfície de ataque, e um novo scan mostrou "apenas" 49 vulnerabilidades.
c. **Atingindo a Excelência (Chainguard)**: Para buscar um resultado ainda melhor, a imagem foi migrada para a base da Chainguard (`cgr.dev/chainguard/python`), conhecida por ser ultra-enxuta e focada em segurança. Após superar alguns desafios, um novo scan com o Trivy revelou ZERO vulnerabilidades de sistema operacional.

4. **Resolvendo Desafios com Imagens Minimalistas**
A migração para a Chainguard, por ser um ambiente extremamente restrito, trouxe desafios únicos que exigiram um entendimento mais profundo do processo de build:

- **Erro `permission denied`**: A imagem da Chainguard, por segurança, roda com um usuário não-root por padrão. Foi preciso adicionar `USER root` temporariamente no estágio de build para permitir a criação do usuário `app`.
- **Erro `pg_config not found`**: Ao tentar instalar o psycopg2, o pip não encontrou uma versão pré-compilada e tentou compilá-la do zero. Para isso, precisava das ferramentas de desenvolvimento do PostgreSQL.
-- **Solução**: Foi necessário instalar postgresql-dev e build-base via apk no estágio de build para permitir a compilação. Posteriormente, o projeto foi modernizado para usar a biblioteca psycopg (v3), que é mais robusta.
- **Erro `No module named flask`**: Após o build, a aplicação não iniciava. A causa era que o Python na imagem final, por ser um ambiente não-padrão, não sabia onde procurar os pacotes que haviam sido copiados.
-- **Solução**: Foi adicionada a variável de ambiente `ENV PYTHONPATH="/usr/lib/python3.12/site-packages"`, que "mostra" ao Python o caminho exato para encontrar as bibliotecas instaladas.

  
## Boas Práticas e Decisões de Design no Dockerfile

O `Dockerfile` final do backend é resultado de várias iterações e reflete boas práticas importantes:
- **Multi-stage Builds**: O uso de um estágio `builder` (com todas as ferramentas de compilação) e um estágio `final` (apenas com o necessário para executar) garante uma imagem final leve e segura.
- **Otimização de Cache**: A instrução `COPY requirements.txt` . é feita antes de `COPY app.py .` para que o Docker não precise reinstalar todas as dependências a cada mudança no código-fonte.
- **Entendimento da Imagem Base (ENTRYPOINT)**:
-- A imagem da Chainguard já possui um `ENTRYPOINT` definido como python3. Por isso, o `CMD` omite o `python3` e fornece apenas os argumentos, evitando duplicação.
- **Configuração Explícita de Paths**:
--`ENV PATH="/usr/local/bin:${PATH}"`: Garante que os executáveis instalados pelo `pip` (como `flask`) possam ser encontrados e executados pelo sistema.
--`ENV PYTHONPATH`: Essencial em imagens minimalistas para dizer ao Python onde encontrar os módulos copiados manualmente.

Autor: Thiago Duran (thduran)