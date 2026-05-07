from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.chat import router as chat_router

app = FastAPI(title="Token Sentinel", version="0.1.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(chat_router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "Token Sentinel"}

@app.get("/")
def root():
    return {"message": "Token Sentinel - AI Gateway", "version": "0.1.0"}