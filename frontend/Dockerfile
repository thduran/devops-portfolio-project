# ---- Estágio 1: Builder ----
# Alpine aqui (e não nginx) é aqui é suficiente
FROM alpine:latest as builder

WORKDIR /app

# Copia arquivos da app pro build stage
COPY index.html .
COPY nginx.conf .

# ---- Estágio 2: Final ----
# Fixa build pra garantir idempotência
FROM nginx:1.27.0-alpine

# Remove configuração padrão do nginx pra só a nossa ser usada
RUN rm /etc/nginx/conf.d/default.conf

# Copia arquivos do build para os locais devidos
COPY --from=builder /app/index.html /usr/share/nginx/html/index.html
COPY --from=builder /app/nginx.conf /etc/nginx/conf.d/default.conf

# installing curl used in line 26
RUN apk add --no-cache curl

# (Optional) Adds healthcheck to check if nginx is responding
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/ || exit 1

# Para documentação
EXPOSE 80