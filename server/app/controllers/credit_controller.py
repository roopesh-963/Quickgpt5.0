from fastapi import APIRouter, Depends, Request, HTTPException
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.transaction import Transaction
from app.services.stripe_service import create_checkout_session
import os
import stripe
from pydantic import BaseModel


router = APIRouter()

# Example plans (same as Node.js)
plans = [
    {
        "_id": "basic",
        "name": "Basic",
        "price": 10,
        "credits": 100,
        "features": ['100 text generations', '50 image generations', 'Standard support', 'Access to basic models']
    },
    {
        "_id": "pro",
        "name": "Pro",
        "price": 20,
        "credits": 500,
        "features": ['500 text generations', '200 image generations', 'Priority support', 'Access to pro models', 'Faster response time']
    },
    {
        "_id": "premium",
        "name": "Premium",
        "price": 30,
        "credits": 1000,
        "features": ['1000 text generations', '500 image generations', '24/7 VIP support', 'Access to premium models', 'Dedicated account manager']
    }
]

# GET PLANS (public)
@router.get("/plan")
async def get_plans():
    return {"success": True, "plans": plans}

# PURCHASE PLAN
class PurchaseRequest(BaseModel):
    plan_id: str

@router.post("/purchase")
async def purchase_plan(req: PurchaseRequest, current_user: User = Depends(get_current_user)):
    plan = next((p for p in plans if p["_id"] == req.plan_id), None)
    if not plan:
        raise HTTPException(status_code=400, detail="Invalid plan")

    # Create a transaction in DB
    transaction = Transaction(
        user_id=str(current_user.id),
        plan_id=plan["_id"],
        amount=plan["price"],
        credits=plan["credits"]
    )
    await transaction.insert()

    origin = os.getenv("FRONTEND_URL", "http://localhost:5173")
    session = await create_checkout_session(
        plan_name=plan["name"],
        plan_price=plan["price"],
        transaction_id=str(transaction.id),
        success_url=f"{origin}/loading",
        cancel_url=origin
    )

    return {"success": True, "url": session.url}

# STRIPE WEBHOOK
@router.post("/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.getenv("STRIPE_WEBHOOK_SECRET")
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook Error: {str(e)}")

    # Handle payment_intent.succeeded
    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        session_list = stripe.checkout.sessions.list(payment_intent=payment_intent["id"])
        session = session_list.data[0] if session_list.data else None
        if session:
            transaction_id = session.metadata.get("transactionId")
            app_id = session.metadata.get("appId")
            if app_id == "quickgpt":
                transaction = await Transaction.get(transaction_id)
                if transaction and transaction.status != "completed":
                    user = await User.get(transaction.user_id)
                    if user:
                        user.credits += transaction.credits
                        await user.save()
                    transaction.status = "completed"
                    await transaction.save()
    return {"received": True}
