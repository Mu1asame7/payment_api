from fastapi import FastAPI
from app.api.v1 import auth, users, accounts, payments, webhook

app = FastAPI(title="Payment API")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(accounts.router)
app.include_router(payments.router)
app.include_router(webhook.router)
