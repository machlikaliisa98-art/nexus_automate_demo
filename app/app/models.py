from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, index=True)
    product_name = Column(String)
    quantity = Column(Float)
    unit = Column(String)
    destination = Column(String)
    delivery_time = Column(String)
    status = Column(String, default="AI Parsed")
    price = Column(Float, default=0.0)

