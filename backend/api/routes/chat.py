from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from services.complexity import analyze_complexity
from services.router import route_model
import litellm
import os
import time
import tiktoken
import uuid
import asyncio
from services.logger import log_request
from langfuse import Langfuse

router = APIRouter()

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY", ""),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY", ""),
    host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    model: Optional[str] = None
    max_tokens: Optional[int] = 500

@router.post("/chat")
async def chat(request: ChatRequest):
    start_time = time.time()

    messages_dict = [m.model_dump() for m in request.messages]
    complexity = analyze_complexity(messages_dict)

    if request.model:
        routing = {"model": request.model, "cost_per_1k_input": 0, "cost_per_1k_output": 0}
    else:
        routing = route_model(complexity["level"])

    optimized_messages = optimize_context(messages_dict, complexity["level"])

    enc = tiktoken.get_encoding("cl100k_base")
    full_text = " ".join([m["content"] for m in optimized_messages])
    input_tokens = len(enc.encode(full_text))
    full_original = " ".join([m["content"] for m in messages_dict])
    original_tokens = len(enc.encode(full_original))
    saved_tokens = original_tokens - input_tokens

    trace = langfuse.trace(name="chat", metadata={"complexity": complexity["level"]})
    generation = trace.generation(
        name="llm_call",
        model=routing["model"],
        input=messages_dict,
    )

    try:
        response = litellm.completion(
            model=routing["model"],
            messages=optimized_messages,
            max_tokens=request.max_tokens or 500,
            api_key=os.getenv("GROQ_API_KEY", ""),
        )
        output_text = response.choices[0].message.content
        generation.end(output=output_text)
    except Exception as e:
        generation.end(level="ERROR", status_message=str(e))
        raise HTTPException(status_code=500, detail=f"LLM Error: {str(e)}")

    output_tokens = len(enc.encode(output_text))
    cost_input = (input_tokens / 1000) * routing["cost_per_1k_input"]
    cost_output = (output_tokens / 1000) * routing["cost_per_1k_output"]
    cost_total = cost_input + cost_output
    cost_without = (original_tokens / 1000) * routing["cost_per_1k_input"] + (output_tokens / 1000) * routing["cost_per_1k_output"]
    savings = max(0, cost_without - cost_total)

    latency = (time.time() - start_time) * 1000

    request_id = str(uuid.uuid4())[:8]
    asyncio.create_task(log_request({
        "request_id": request_id,
        "model_used": routing["model"],
        "complexity_level": complexity["level"],
        "complexity_score": complexity["score"],
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "saved_tokens": saved_tokens,
        "cost_total": cost_total,
        "cost_saved": savings,
        "latency_ms": latency,
        "status": "success",
    }))

    return {
        "response": output_text,
        "model_used": routing["model"],
        "complexity": complexity,
        "tokens": {"input": input_tokens, "output": output_tokens, "total": input_tokens + output_tokens, "saved": saved_tokens},
        "cost": {"total": round(cost_total, 6), "saved": round(savings, 6), "savings_percent": round((savings / cost_without * 100), 1) if cost_without > 0 else 0},
        "latency_ms": round(latency, 2),
    }

def optimize_context(messages: list, level: str) -> list:
    if len(messages) <= 4:
        return messages
    optimized = messages[-10:]
    if level == "low" and len(messages) > 6:
        system_msg = next((m for m in optimized if m["role"] == "system"), None)
        recent = [m for m in optimized if m["role"] != "system"]
        if len(recent) > 4:
            recent = recent[:1] + recent[-3:]
        optimized = [system_msg] + recent if system_msg else recent
    return [m for m in optimized if m is not None]