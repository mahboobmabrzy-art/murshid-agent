import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("audit")

def record_audit(user_id: str, action: str, details: dict):
    logger.info(f"[AUDIT] User: {user_id} | Action: {action} | Details: {details}")
