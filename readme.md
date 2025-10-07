
# 🐳 Projeto - Frontend + Backend com Docker Compose

Este projeto demonstra uma aplicação simples com dois containers:

- **Frontend:** página HTML servida por Nginx  
- **Backend:** API em Flask que retorna uma mensagem JSON

---

## 📁 Estrutura
```
simple-nginx-flask-app/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html
│   ├── nginx.conf
│   └── Dockerfile
└── compose.yaml
```

---

## ▶️ Como rodar o projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/thduran/simple-nginx-flask-app
   cd simple-nginx-flask-app
   ```

2. Construa e suba os containers:
   ```bash
   docker compose up --build
   ```

3. Acesse no navegador:
   ```
   http://localhost:8080
   ```

---

## 🧪 Testes manuais

- **Verifique a API diretamente:**  
  ```bash
  curl http://localhost:5000/api
  ```

- **Verifique se o frontend responde:**  
  Acesse `http://localhost:8080`  
  → A mensagem `"Olá do backend!"` deve aparecer na tela.

---

## 🧰 Comandos Docker usados

```bash
docker compose up --build       # Constrói e sobe os serviços
docker compose down             # Encerra e remove os containers
docker compose ps               # Lista containers ativos
docker logs frontend            # Exibe logs do container frontend
docker exec -it backend sh      # Acessa o container backend
```

---

## 🔗 Comunicação entre serviços

- O `frontend` usa **proxy reverso no Nginx** para redirecionar `/api` para o `backend`.
- Os serviços se comunicam via **rede interna** do Docker Compose.

---

## ✅ Status

✔️ Semana de estudos finalizada — conceitos de Docker, Dockerfile, imagens, volumes e Docker Compose aplicados.
