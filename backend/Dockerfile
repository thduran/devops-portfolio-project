# ---- Build stage ----
# based on Wolfi (OS focused on security)
FROM cgr.dev/chainguard/python:latest-dev AS builder

WORKDIR /app

# Avoid .pyc files and buffered logs
ENV PYTHONDONTWRITEBYTECODE=1
# For logs to appear on docker console, facilitating debug
ENV PYTHONUNBUFFERED=1

USER root

# Creates app user. Wolfi uses /etc/apk/keys as standard dir
RUN addgroup --system app && adduser --system --ingroup app app

# Install build dependencies for psycopg (binary wheel deve evitar compilação, mas fallback)
RUN apk update && apk add postgresql-dev build-base

# To use cache, copy is made before code copy - if only the code changes, Docker doesn't reinstall everything
COPY requirements.txt .

# Updates pip and tools of Python installation (setuptools and wheel)
RUN python3 -m pip install --upgrade pip setuptools wheel

# --no-cache-dir helps to maintain a smaller image
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# ---- Final stage ----
FROM cgr.dev/chainguard/python:latest

WORKDIR /app

# Copies user definition of builder
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group

# Copies python packages installed in builder
COPY --from=builder /usr/lib/python*/site-packages /usr/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copies app.py of builder
# Only what's necessary is brought: app and packages.
COPY --from=builder --chown=app:app /app/app.py .

# Diz ao Python para procurar pacotes neste diretório
ENV PYTHONPATH="/usr/lib/python3.12/site-packages"

# Garantindo que o PATH inclui Python e pip (PATH base já tem /usr/bin)
ENV PATH="/usr/local/bin:${PATH}"

USER app

EXPOSE 5000

# CMD omitindo python3 (ENTRYPOINT da imagem adiciona)
CMD ["-m", "flask", "--app", "app.py", "run", "--host=0.0.0.0"]