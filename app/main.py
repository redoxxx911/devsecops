import os
import time
import logging
from datetime import datetime, timedelta
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from jose import JWTError, jwt
from pythonjsonlogger import jsonlogger
from database import app_db, log_audit_event

# Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "default_secret")
ALGORITHM = "HS256"

# JSON Logging Setup (Output to stdout for Filebeat/Fluentd to capture later)
logger = logging.getLogger("api_logger")
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

# Rate Limiter
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Middlewares ---
@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    log_dict = {
        "client_ip": request.client.host,
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "response_time_ms": round(process_time * 1000, 2)
    }
    logger.info("API Request", extra=log_dict)
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catches 500s and logs them to the MongoDB audit_logs collection."""
    error_details = {"path": request.url.path, "error": str(exc), "ip": request.client.host}
    await log_audit_event("CRITICAL_ERROR", "system", error_details)
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

# --- Models (Input Validation & Sanitization) ---
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# --- Endpoints ---
@app.post("/token")
@limiter.limit("5/minute")
async def login(request: Request, user: UserLogin):
    # Dummy auth check
    if user.email != "admin@example.com" or user.password != "password123":
        await log_audit_event("AUTH_FAILED", user.email, {"ip": request.client.host})
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    expires = datetime.utcnow() + timedelta(hours=1)
    token = jwt.encode({"sub": user.email, "exp": expires}, JWT_SECRET, algorithm=ALGORITHM)
    await log_audit_event("AUTH_SUCCESS", user.email, {"ip": request.client.host})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/secure-data")
async def read_secure_data(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return {"data": "This is protected data", "user": payload.get("sub")}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
