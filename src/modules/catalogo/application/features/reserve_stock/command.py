"""
Command para reservar stock de productos.
"""
from pydantic import BaseModel, Field
from typing import List
from uuid import UUID


class ReserveStockItemCommand(BaseModel):
    """DTO para un item a reservar."""
    product_id: UUID = Field(..., description="ID del producto")
    quantity: int = Field(..., gt=0, description="Cantidad a reservar")


class ReserveStockCommand(BaseModel):
    """
    DTO de entrada para reservar stock de múltiples productos.
    """
    items: List[ReserveStockItemCommand] = Field(..., min_length=1, description="Items a reservar")
    
    class Config:
        json_schema_extra = {
            "example": {
                "items": [
                    {
                        "product_id": "123e4567-e89b-12d3-a456-426614174000",
                        "quantity": 2
                    }
                ]
            }
        }
