MODEL_ROUTING = {
    "low": {
        "model": "groq/llama-3.1-8b-instant",
        "cost_per_1k_input": 0.00005,
        "cost_per_1k_output": 0.00008,
    },
    "medium": {
        "model": "groq/llama-3.3-70b-versatile",
        "cost_per_1k_input": 0.00059,
        "cost_per_1k_output": 0.00079,
    },
    "high": {
        "model": "groq/llama-3.3-70b-versatile",
        "cost_per_1k_input": 0.00059,
        "cost_per_1k_output": 0.00079,
    },
    "fallback": {
        "model": "groq/llama-3.1-8b-instant",
        "cost_per_1k_input": 0.00005,
        "cost_per_1k_output": 0.00008,
    }
}

def route_model(complexity_level: str) -> dict:
    return MODEL_ROUTING.get(complexity_level, MODEL_ROUTING["fallback"])