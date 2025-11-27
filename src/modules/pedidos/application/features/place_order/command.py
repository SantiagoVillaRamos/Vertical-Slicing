"""
Command (DTO) para crear una orden.
"""
from pydantic import BaseModel, Field, field_validator
from typing import List
from uuid import UUID


class OrderItemCommand(BaseModel):
    """DTO para un item de la orden."""
    product_id: UUID = Field(..., description="ID del producto")
    quantity: int = Field(..., gt=0, description="Cantidad a ordenar")
    
    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "123e4567-e89b-12d3-a456-426614174000",
                "quantity": 2
            }
        }


class CustomerInfoCommand(BaseModel):
    """DTO para información del cliente."""
    customer_id: str = Field(..., min_length=1, description="ID del cliente")
    name: str = Field(..., min_length=3, description="Nombre completo")
    email: str = Field(..., description="Email del cliente")
    phone: str = Field(..., description="Teléfono del cliente")
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Email debe ser válido")
        return v.lower()
    
    class Config:
        json_schema_extra = {
            "example": {
                "customer_id": "CUST-001",
                "name": "Juan Pérez",
                "email": "juan@example.com",
                "phone": "+57 300 1234567"
            }
        }


class AddressCommand(BaseModel):
    """DTO para dirección de envío."""
    street: str = Field(..., min_length=5, description="Calle y número")
    city: str = Field(..., min_length=2, description="Ciudad")
    state: str = Field(..., description="Departamento/Estado")
    postal_code: str = Field(..., description="Código postal")
    country: str = Field(default="Colombia", description="País")
    
    class Config:
        json_schema_extra = {
            "example": {
                "street": "Calle 123 #45-67",
                "city": "Bogotá",
                "state": "Cundinamarca",
                "postal_code": "110111",
                "country": "Colombia"
            }
        }


class PlaceOrderCommand(BaseModel):
    """
    DTO de entrada para crear una orden.
    """
    customer_info: CustomerInfoCommand = Field(..., description="Información del cliente")
    items: List[OrderItemCommand] = Field(..., min_length=1, description="Items de la orden")
    shipping_address: AddressCommand = Field(..., description="Dirección de envío")
    
    @field_validator('items')
    @classmethod
    def validate_items(cls, v: List[OrderItemCommand]) -> List[OrderItemCommand]:
        if not v:
            raise ValueError("La orden debe tener al menos un item")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "customer_info": {
                    "customer_id": "CUST-001",
                    "name": "Juan Pérez",
                    "email": "juan@example.com",
                    "phone": "+57 300 1234567"
                },
                "items": [
                    {
                        "product_id": "123e4567-e89b-12d3-a456-426614174000",
                        "quantity": 2
                    }
                ],
                "shipping_address": {
                    "street": "Calle 123 #45-67",
                    "city": "Bogotá",
                    "state": "Cundinamarca",
                    "postal_code": "110111",
                    "country": "Colombia"
                }
            }
        }
