"""
Response para la reserva de stock.
"""
from pydantic import BaseModel
from typing import List, Dict
from uuid import UUID


class ProductStockInfo(BaseModel):
    """Información de stock de un producto."""
    product_id: UUID
    product_name: str
    sku: str
    requested_quantity: int
    reserved_quantity: int
    remaining_stock: int
    unit_price: float


class ReserveStockResponse(BaseModel):
    """
    DTO de salida para la reserva de stock.
    """
    success: bool
    products: List[ProductStockInfo]
    message: str = ""
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "products": [
                    {
                        "product_id": "123e4567-e89b-12d3-a456-426614174000",
                        "product_name": "Laptop Dell XPS 15",
                        "sku": "LAPTOP-001",
                        "requested_quantity": 2,
                        "reserved_quantity": 2,
                        "remaining_stock": 8,
                        "unit_price": 1299.99
                    }
                ],
                "message": "Stock reservado exitosamente"
            }
        }
