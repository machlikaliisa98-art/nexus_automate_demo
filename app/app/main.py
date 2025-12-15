import os
from fastapi import FastAPI, Form, Depends
from twilio.rest import Client
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.models import Order
from app.ai_parser import parse_order

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Twilio setup
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
client = Client(TWILIO_SID, TWILIO_TOKEN)

app = FastAPI(title="Nexus Automate API", version="1.0")

# Root route / health check
@app.get("/")
def read_root():
    return {"message": "Nexus Automate API is running!"}

# WhatsApp webhook endpoint
@app.post("/whatsapp")
async def whatsapp_webhook(
    From: str = Form(...),
    Body: str = Form(...),
    db: Session = Depends(get_db)
):
    # Parse the message with AI
    order_data = parse_order(Body)

    # Save order to database
    order = Order(
        customer_name=From,
        product_name=order_data.get("product_name"),
        quantity=float(order_data.get("quantity", 0)),
        unit=order_data.get("unit", "kg"),
        destination=order_data.get("destination"),
        delivery_time=order_data.get("delivery_time")
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    # Send reply via WhatsApp
    reply = (
        f"✅ Order received!\n"
        f"Product: {order.product_name}\n"
        f"Quantity: {order.quantity} {order.unit}\n"
        f"Destination: {order.destination}\n"
        f"Delivery: {order.delivery_time}\n"
        f"Nexus Automate will confirm pricing shortly."
    )

    client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        to=From,
        body=reply
    )

    return {"status": "success", "order_id": order.id}

# Retrieve all orders
@app.get("/orders/")
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return orders

