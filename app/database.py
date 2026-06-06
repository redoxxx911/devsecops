import os
from motor.motor_asyncio import AsyncIOMotorClient

# App service for standard read/write on collections
APP_MONGO_URI = os.getenv("APP_MONGO_URI")
app_client = AsyncIOMotorClient(APP_MONGO_URI)
app_db = app_client.appdb

# Audit service strictly for insert-only on audit_logs
AUDIT_MONGO_URI = os.getenv("AUDIT_MONGO_URI")
audit_client = AsyncIOMotorClient(AUDIT_MONGO_URI)
audit_db = audit_client.appdb

async def log_audit_event(event_type: str, user: str, details: dict):
    """Writes to the restricted audit_logs collection using the audit role."""
    document = {"event_type": event_type, "user": user, "details": details}
    await audit_db.audit_logs.insert_one(document)
