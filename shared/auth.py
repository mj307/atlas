from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from shared.config import settings
# actually checks each time a request comes in, so it cedices who is allowed to access the system

security = HTTPBearer()

SECRET_KEY = settings.mcp_secret_key

def verify_mcp_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    if token != SECRET_KEY:
        raise HTTPException(status_code=401, detail="Invalid token")

    return token