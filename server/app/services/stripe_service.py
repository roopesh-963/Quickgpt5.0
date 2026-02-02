import stripe, os

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

async def create_checkout_session(plan_name, plan_price, transaction_id, success_url, cancel_url):
    session = stripe.checkout.sessions.create(
        mode="payment",
        line_items=[{
            "price_data": {
                "currency": "usd",
                "unit_amount": int(plan_price * 100),
                "product_data": {"name": plan_name}
            },
            "quantity": 1
        }],
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={"transactionId": transaction_id, "appId": "quickgpt"}
    )


    return session
