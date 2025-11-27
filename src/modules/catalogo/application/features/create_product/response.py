"""
Response (DTO) para la creación de un producto.
"""
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class CreateProductResponse(BaseModel):
    """
    DTO de salida para la creación de un producto.
    """
    product_id: UUID
    sku: str
    name: str
    description: str
    price: float
    currency: str
    stock: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True  # Permite crear desde objetos ORM
        json_schema_extra = {
            "example": {
                "product_id": "123e4567-e89b-12d3-a456-426614174000",
                "sku": "PROD-12345",
                "name": "Laptop Dell XPS 15",
                "description": "Laptop de alto rendimiento",
                "price": 1299.99,
                "currency": "USD",
                "stock": 10,
                "is_active": True,
                "created_at": "2024-01-01T12:00:00"
            }
        }
