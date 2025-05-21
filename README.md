# MCP Adapter Service

A lightweight, containerized FastAPI service that receives **Model Context Protocol (MCP)** requests and asynchronously dispatches them to backend services such as:

- `maceopt`: Geometry optimization using MACE
- `zeopp`: Structural analysis using Zeo++
- `xtb`: GFN1-xTB-based optimization

---

## 🚀 Features

- ✅ Supports standardized MCP request format
- 🧠 Asynchronous task queue via Celery
- 🧪 Rich structured logging with trace ID
- 🔌 Easily extendable to more backend models
- 🐳 Fully containerized for server deployment
- 🧵 Route-based Zeo++ multi-function support

---

## 📦 Deployment (Docker Compose)

### 1. Clone the repository

```bash
git clone https://github.com/your-org/mcp-adapter-service.git
cd mcp-adapter-service
```text
```

### 2. Configure environment

Create a `.env` file:

```ini
# Redis
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Backend services
MACEOPT_BASE_URL=http://192.168.100.208:4748
ZEO_BASE_URL=http://192.168.100.208:9876
XTB_BASE_URL=http://192.168.100.208:4548
```

### 3. Build and start all services

```bash
docker-compose up --build -d
```

Access the API via: `http://<your-server-ip>:9000/docs`

---

## 🧠 API Endpoints

### `POST /mcp`

Submit a structured request to route to the appropriate backend.

Example body:

```json
{
  "input": "<.xyz or .cssr content>",
  "context": {
    "task_id": "mcp_001",
    "model": "zeopp",
    "parameters": {
      "route": "surface_area",
      "output_filename": "output.sa"
    }
  }
}
```

### `GET /result/{task_id}`

Query asynchronous task result by task ID.

### `GET /zeopp/list_routes`

List all supported Zeo++ analysis endpoints.

---

## 📂 Project Structure

```
app/
├── adapters/         # Dispatcher and router
├── middleware/       # Trace logging
├── models/           # Pydantic schema
├── services/         # Celery tasks and backend clients
├── utils/            # Rich logger and trace ID
├── main.py           # FastAPI app entry
celery_worker.py      # Celery worker entry
Dockerfile
docker-compose.yml
.env.template
```

---

## 👤 Author

Shibo Li · 2025  
MIT License
