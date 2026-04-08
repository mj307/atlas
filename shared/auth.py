from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

SECRET_KEY = "secret" # temp

def verify_mcp_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    if token != SECRET_KEY:
        raise HTTPException(status_code=401, detail="Invalid token")

    return token