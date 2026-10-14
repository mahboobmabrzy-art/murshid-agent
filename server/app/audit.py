import logging
logger = logging.getLogger("murshid.audit")
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

def record_audit(user_id: str, action: str, details: dict):
    logger.info(f"audit user={user_id} action={action} details={details}")
