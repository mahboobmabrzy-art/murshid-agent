from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field, ValidationError
from typing import Optional, Dict, Any
from server.app.llm_client import LLMClient, LLMError
from server.app.auth import get_current_user
from server.app.audit import record_audit

router = APIRouter()
llm = LLMClient()

class AskRequest(BaseModel):
    project_id: Optional[str] = Field(None)
    prompt: str = Field(..., min_length=3)
    context: Optional[Dict[str, Any]] = {}

class AskResponse(BaseModel):
    action: str
    params: Dict[str, Any]
    confidence: float
    checks: list
    explanation: Optional[str] = None

@router.post("/", response_model=AskResponse)
async def ask(req: AskRequest, user=Depends(get_current_user)):
    record_audit(user.get("id", "anonymous"), "ask_request", {"project_id": req.project_id, "prompt_len": len(req.prompt)})
    prompt_template = (
        "You are Murshid agent. Output EXACTLY one JSON object matching schema: "
        '{"action": "...", "params": {...}, "confidence": 0.0, "checks": [...], "explanation": "..."}\n'
        f"Project:{req.project_id}\nContext:{req.context}\nUser:{req.prompt}\n"
        "If missing info, return action 'ask_for_info' with params.missing list."
    )
    try:
        resp = await llm.send_prompt(prompt_template)
    except LLMError as e:
        raise HTTPException(status_code=502, detail=str(e))

    try:
        validated = AskResponse(**resp)
    except ValidationError as e:
        record_audit(user.get("id", "anonymous"), "ask_response_invalid", {"error": str(e), "raw": resp})
        return AskResponse(
            action="ask_for_info",
            params={"missing": ["structured_response"]},
            confidence=0.0,
            checks=[],
            explanation="الوكيل يحتاج مزيد من المعلومات"
        )

    if validated.action in ("create_campaign", "post_message", "delete_resource"):
        required_checks = {"api_key_exists", "permissions_ok"}
        missing_checks = list(required_checks - set(validated.checks))
        if missing_checks:
            return AskResponse(
                action="require_integration",
                params={"missing_checks": missing_checks},
                confidence=validated.confidence,
                checks=validated.checks,
                explanation="مطلوب إعدادات تكامل قبل التنفيذ"
            )

    record_audit(user.get("id", "anonymous"), "ask_response_ok", {"action": validated.action})
    return validated
