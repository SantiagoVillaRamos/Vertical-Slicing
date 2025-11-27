"""
Response (DTO) para la creación de una orden.
"""
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List


class OrderItemResponse(BaseModel):
    """DTO de salida para un item de orden."""
    product_id: UUID
    product_name: str
    quantity: int
    unit_price: float
    subtotal: float


class PlaceOrderResponse(BaseModel):
    """
    DTO de salida para la creación de una orden.
    """
    order_id: UUID
    customer_id: str
    customer_name: str
    items: List[OrderItemResponse]
    total_amount: float
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "order_id": "123e4567-e89b-12d3-a456-426614174000",
                "customer_id": "CUST-001",
                "customer_name": "Juan Pérez",
                "items": [
                    {
                        "product_id": "123e4567-e89b-12d3-a456-426614174001",
                        "product_name": "Laptop Dell XPS 15",
                        "quantity": 2,
                        "unit_price": 1299.99,
                        "subtotal": 2599.98
                    }
                ],
                "total_amount": 2599.98,
                "status": "confirmed",
                "created_at": "2024-01-01T12:00:00"
            }
        }
