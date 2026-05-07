from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api.routes.chat import router as chat_router
from api.routes.metrics import router as metrics_router
import os

app = FastAPI(title="Token Sentinel", version="0.1.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(chat_router)
app.include_router(metrics_router)

# Dashboard estático
frontend_path = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "Token Sentinel"}