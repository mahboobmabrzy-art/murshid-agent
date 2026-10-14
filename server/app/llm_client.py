import os
import asyncio
import httpx
import json
from typing import Any, Dict

LLM_API_KEY = os.getenv("LLM_API_KEY", "")
GEMINI_URL = os.getenv("GEMINI_URL", "https://api.gemini.example/v1/generate")

class LLMError(Exception):
    pass

class LLMClient:
    def __init__(self, api_key: str = LLM_API_KEY, base_url: str = GEMINI_URL):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    async def _post(self, payload: Dict[str, Any], timeout: int = 30) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=timeout) as client:
            r = await client.post(self.base_url, json=payload, headers=self.headers)
            r.raise_for_status()
            return r.json()

    async def send_prompt(self, prompt: str, max_retries: int = 3) -> Dict[str, Any]:
        payload = {"prompt": prompt, "max_tokens": 800, "temperature": 0.2}
        backoff = 1
        for attempt in range(1, max_retries + 1):
            try:
                data = await self._post(payload)
                structured = self._extract_structured(data)
                return structured
            except (httpx.HTTPError, json.JSONDecodeError, KeyError) as e:
                if attempt == max_retries:
                    raise LLMError(f"LLM failed after {max_retries} attempts: {e}")
                await asyncio.sleep(backoff)
                backoff *= 2
        raise LLMError("LLM unreachable")

    def _extract_structured(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if "structured_response" in data and isinstance(data["structured_response"], dict):
            return data["structured_response"]
        text = data.get("text") or data.get("output") or ""
        try:
            return json.loads(text)
        except Exception:
            return {
                "action": "ask_for_info",
                "params": {"missing": ["structured_response"]},
                "confidence": 0.0,
                "checks": [],
                "explanation": "الوكيل يحتاج مزيد من المعلومات"
            }
