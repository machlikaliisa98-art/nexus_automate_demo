from pydantic import BaseModel

class OrderCreate(BaseModel):
    product_name: str
    quantity: int
    location: str

