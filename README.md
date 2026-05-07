 🛡️ Token Sentinel

**AI Gateway inteligente para otimização de custos e roteamento de LLMs.**

![Stack](https://img.shields.io/badge/stack-FastAPI%20%7C%20LiteLLM%20%7C%20SQLite%20%7C%20React-blue)
![Status](https://img.shields.io/badge/status-MVP-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)

---

## O que é?

O Token Sentinel é uma **camada intermediária entre aplicações/agentes e provedores de LLM**. Ele atua como um API Gateway inteligente que:

- 🔍 Analisa a complexidade de cada prompt
- 🚦 Roteia automaticamente para o modelo ideal (custo vs. qualidade)
- ✂️ Comprime e otimiza o contexto (reduz tokens)
- 📊 Monitora custos, tokens e latência em tempo real
- 🛡️ Previne desperdício computacional e custos imprevisíveis

## Por que usar?

Empresas que usam LLMs enfrentam prompts gigantes, uso de modelos caros para tarefas simples, falta de controle de tokens e custos imprevisíveis.

O Token Sentinel resolve isso automaticamente.

## Funcionalidades do MVP

- ✅ **POST /chat** — API compatível com OpenAI (aceita mensagens e retorna resposta otimizada)
- ✅ **Complexity Analyzer** — classifica prompts em `low`, `medium`, `high`
- ✅ **Router** — escolhe automaticamente o modelo (Llama 8B, 70B, etc.)
- ✅ **Context Optimizer** — remove mensagens antigas, corta redundância
- ✅ **Token Counter** — conta input/output tokens com tiktoken
- ✅ **Cost Calculator** — calcula custo estimado e economia gerada
- ✅ **GET /metrics** — retorna métricas agregadas
- ✅ **Dashboard** — interface web dark tech com gráficos e tabelas
- ✅ **Logging** — todas as requests salvas em SQLite para auditoria

## Stack

| Camada | Tecnologia |
|--------|-----------|
| Backend | FastAPI + Python 3.12 |
| LLM Router | LiteLLM (provider agnostic) |
| Modelos | Groq (Llama 3.1 8B, Llama 3.3 70B) |
| Token Counter | tiktoken |
| Observabilidade | Langfuse (tracing) |
| Banco | SQLite (MVP) / PostgreSQL (produção) |
| Dashboard | HTML + CSS + JavaScript vanilla |
| Infra | GitHub Codespaces |

## Como rodar

```bash
git clone https://github.com/rafael-souzza/tokensentinel.git
cd tokensentinel/backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # adicione sua GROQ_API_KEY
uvicorn api.main:app --host 0.0.0.0 --port 8000
Acesse http://localhost:8000 para o dashboard.

Arquitetura
text
Client/App → POST /chat
  ↓
Complexity Analyzer (regras heurísticas)
  ↓
Context Optimizer (truncamento + dedup)
  ↓
Router (escolhe modelo baseado em complexidade)
  ↓
LLM Provider (via LiteLLM)
  ↓
Cost Calculator + Logger (SQLite)
  ↓
Response + Métricas salvas
Endpoints
Método	Rota	Descrição
POST	/chat	Chat otimizado com roteamento automático
GET	/metrics	Métricas agregadas (tokens, custo, latência)
GET	/api/health	Health check
GET	/	Dashboard
Roadmap
V2 (em breve)
Semantic Cache (respostas similares reaproveitadas)

Budget Enforcement (custo máximo por request/dia)

Dynamic Context Compression (ajuste por modelo/custo)

Benchmark entre modelos

V3 (futuro)
Adaptive Routing com reinforcement learning

Self-optimizing prompts

Anomaly Detection

Autonomous Optimization

Autor
Rafael Souza
