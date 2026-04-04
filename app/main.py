from fastapi import FastAPI, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import jwt
import time
from typing import Optional

app = FastAPI(title="Zero-Trust Vault API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "SuperSecureDevSecOpsVaultKey"

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/token")
async def login(credentials: LoginRequest):
    if credentials.email == "admin@arch" and credentials.password == "secure123":
        payload = {"sub": credentials.email, "exp": time.time() + 3600}
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/secrets")
async def get_secrets(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization Header")
    
    try:
        # Extract "Bearer <token>"
        token = authorization.split(" ")[1]
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        
        # Return mock secure data
        return {
            "secrets": [
                "SSH_KEY: 8b2e...3f1a",
                "DB_PASSWORD: admin_complex_pass_2026",
                "PRODUCTION_API_URL: https://api.internal.vault",
                "MOCK_BITCOIN_WALLET: bc1qxy2kgdy..."
            ]
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or Expired Token")
