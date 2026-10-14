from fastapi import Depends, HTTPException, status, Header

async def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing auth")
    
    token = authorization.replace("Bearer ", "")
    if token == "dev-token":
        return {"id": "user-dev", "email": "dev@example.com", "roles": ["admin"]}
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
