from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from .schemas import OrderCreate
from .models import Order
from .bot import send_whatsapp_message

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Nexus Automate API is running!"}

@app.post("/orders/")
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(
        product_name=order.product_name,
        quantity=order.quantity,
        location=order.location
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Send WhatsApp confirmation
    send_whatsapp_message(
        to="whatsapp:+250xxxxxxxxx",  # replace with your test number
        message=f"Order received: {order.quantity}kg of {order.product_name} to {order.location}"
    )

    return {"status": "success", "order_id": db_order.id}

