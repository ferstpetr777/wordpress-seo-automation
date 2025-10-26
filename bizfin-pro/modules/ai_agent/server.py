from typing import Any, Dict, Optional
from fastapi import FastAPI, Header, HTTPException
from starlette.responses import PlainTextResponse
from pydantic import BaseModel
import os
import uvicorn
import re


class StructuredRequest(BaseModel):
    prompt: str
    schema: Dict[str, Any]
    temperature: Optional[float] = 0.2
    max_tokens: Optional[int] = 3000


app = FastAPI(title="BizFin AI Assistant", version="1.0.0")


@app.get("/health")
def health() -> PlainTextResponse:
    return PlainTextResponse("ok")


def _auth_or_401(auth_header: Optional[str]) -> None:
    expected = os.getenv("AI_ASSISTANT_API_KEY", "demo_key")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")
    token = auth_header.split(" ", 1)[1].strip()
    if token != expected:
        raise HTTPException(status_code=403, detail="Invalid API key")


@app.post("/v1/structured")
def structured(req: StructuredRequest, Authorization: Optional[str] = Header(default=None)) -> Dict[str, Any]:
    _auth_or_401(Authorization)

    # Наивная эвристическая генерация структурированного ответа под заданную схему.
    # В реальном режиме здесь можно подключить LLM-провайдера.
    prompt_lower = req.prompt.lower()

    def extract_list(pattern: str) -> list[str]:
        found = re.findall(pattern, prompt_lower)
        return [s.strip() for s in found if s.strip()]

    response: Dict[str, Any] = {}
    props = req.schema.get("properties", {}) if isinstance(req.schema, dict) else {}

    for key in props.keys():
        if key in ("primary", "secondary", "semantic_keywords", "trending_terms"):
            # Выделяем слова из темы
            words = re.findall(r"[а-яёa-z0-9\-]{4,}", prompt_lower)
            unique = []
            for w in words:
                if w not in unique:
                    unique.append(w)
                if len(unique) >= 8:
                    break
            response[key] = unique[:8]
        elif key == "long_tail":
            # Берем фразы вокруг ключа в кавычках
            tails = extract_list(r"\"([^\"]{15,80})\"")
            if not tails:
                tails = [
                    "как получить обеспечение банковской гарантии",
                    "стоимость и сроки обеспечения банковской гарантии",
                    "документы для обеспечения банковской гарантии"
                ]
            response[key] = tails[:8]
        elif key == "search_intent":
            if any(x in prompt_lower for x in ["как", "сколько", "стоимость", "оформить", "заявка"]):
                response[key] = "commercial"
            else:
                response[key] = "informational"
        elif key == "difficulty":
            response[key] = 6
        elif key == "content_gaps":
            response[key] = [
                "Недостаточно практических кейсов",
                "Слабые CTA",
                "Нет интерактивных инструментов"
            ]
        elif key == "analysis_insights":
            response[key] = "Структурированный анализ сформирован из предоставленного контента."
        elif key == "content_angles":
            response[key] = [
                "Пошаговый гид: обеспечение банковской гарантии в 2024",
                "Снижение рисков при обеспечении банковской гарантии",
                "Сравнение условий обеспечения в банках-партнерах",
                "Документы и типичные ошибки при обеспечении",
                "Сроки и стоимость: как оптимизировать расходы",
                "Кейс: ускоренное обеспечение для тендеров",
                "Чек-лист для бухгалтера и юриста"
            ]
        else:
            # Значение по умолчанию согласно типу
            t = props[key].get("type") if isinstance(props.get(key), dict) else None
            if t == "array":
                response[key] = []
            elif t == "integer":
                response[key] = 0
            else:
                response[key] = ""

    return response


if __name__ == "__main__":
    uvicorn.run("modules.ai_agent.server:app", host="127.0.0.1", port=8000, reload=False)


