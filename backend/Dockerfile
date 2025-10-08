# ---- Build stage ----
# A tag específica (.1) garante que o build seja sempre o mesmo.
FROM python:3.12.1-slim as builder

# Define o diretório de trabalho
WORKDIR /app

# impede que Python gere arquivos .pyc, que são desnecessários e ocupam espaço.
ENV PYTHONDONTWRITEBYTECODE 1
# Pra que logs apareçam no console do Docker, facilitando o debug
ENV PYTHONUNBUFFERED 1

# Feito antes de copiar código pra aproveitar cache - Se só o código mudar, Docker não reinstala tudo.
COPY requirements.txt .

# --no-cache-dir ajuda a manter a imagem menor
# install --user instala pacotes em um diretório do usuário 
RUN pip install --no-cache-dir --user -r requirements.txt

# Copia o código da aplicação
COPY app.py .

# ---- Final stage ----
FROM python:3.12.1-slim

# Para não rodar como root, por segurança
RUN addgroup --system app && adduser --system --group app

# Define o diretório de trabalho
WORKDIR /home/app

# Força python a procurar pacotes no diretório correto
ENV PYTHONPATH=/home/app/.local/lib/python3.12/site-packages

# Copia da imagem builder tudo que foi instalado via pip (/root/.local)
# --chown garante que o usuário app seja o dono
COPY --from=builder --chown=app:app /root/.local /home/app/.local

# Copia o arquivo do app da imagem builder pro workdir da imagem final
# Só o necessário é trazido: app e dependências.
COPY --from=builder --chown=app:app /app/app.py .

# Adiciona o caminho onde as dependências Python foram instaladas (/home/app/.local/bin) ao PATH.
# Comandos instalados via pip podem ser executados sem precisar de caminho completo.
ENV PATH="/home/app/.local/bin:${PATH}"

# Muda para o usuário não-root
USER app

# Comando para executar a aplicação
CMD ["python", "app.py"]