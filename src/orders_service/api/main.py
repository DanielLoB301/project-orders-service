from fastapi import FastAPI

from orders_service.api.routers import orders

app = FastAPI(title="Orders Service")

app.include_router(orders.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Orders Service running"}