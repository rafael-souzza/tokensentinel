import re

def analyze_complexity(messages: list) -> dict:
    if not messages:
        return {"level": "low", "score": 0}

    full_text = " ".join([m.get("content", "") for m in messages])
    length = len(full_text)

    has_json = bool(re.search(r'\{.*\}|\[.*\]', full_text))
    has_code = bool(re.search(r'```|def |function |import |class ', full_text))
    has_ocr = bool(re.search(r'ocr|imagem|pdf|documento', full_text.lower()))
    has_reasoning = bool(re.search(r'analis|expliq|justifi|compare|avalie', full_text.lower()))
    has_multi_step = len(re.findall(r'\d+\.\s', full_text)) >= 3
    has_tools = bool(re.search(r'ferramenta|tool|plugin|api|agente', full_text.lower()))

    score = length / 500 + (10 if has_json else 0) + (10 if has_code else 0) + (15 if has_ocr else 0) + (15 if has_reasoning else 0) + (10 if has_multi_step else 0) + (15 if has_tools else 0)

    if score < 10:
        level = "low"
    elif score < 30:
        level = "medium"
    else:
        level = "high"

    return {"level": level, "score": round(score, 1), "factors": {"length": min(length, 5000), "has_json": has_json, "has_code": has_code, "has_ocr": has_ocr, "has_reasoning": has_reasoning, "has_multi_step": has_multi_step, "has_tools": has_tools}}