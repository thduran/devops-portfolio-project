# ---- Estágio 1: Builder ----
# Here, alpine (and not nginx) is enough
FROM alpine:latest as builder

WORKDIR /app

COPY index.html .
COPY nginx.conf .

# ---- Estágio 2: Final ----
# Fixes build to guarantee idempotence
FROM nginx:1.27.0-alpine

# Removes nginx standard config so that only ours be used
RUN rm /etc/nginx/conf.d/default.conf

# Copies files from build to due dirs
COPY --from=builder /app/index.html /usr/share/nginx/html/index.html
COPY --from=builder /app/nginx.conf /etc/nginx/conf.d/default.conf

# Installing curl used in line 26
RUN apk add --no-cache curl

# (Optional) Adds healthcheck to check if nginx is responding
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/ || exit 1
  
EXPOSE 80