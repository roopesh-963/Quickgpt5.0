from beanie import Document
from datetime import datetime

class Transaction(Document):
    user_id: str
    plan_id: str
    amount: float
    credits: int
    status: str = "pending"  # pending / completed
    created_at: datetime = datetime.utcnow()

    class Settings:
        name = "transactions"
