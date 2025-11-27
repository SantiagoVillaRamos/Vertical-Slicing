"""
Command (DTO) para crear un producto.
Los Commands son objetos de transferencia de datos sin lógica de negocio.
"""
from pydantic import BaseModel, Field, field_validator


class CreateProductCommand(BaseModel):
    """
    DTO de entrada para crear un producto.
    Usa Pydantic para validación básica de tipos y formato.
    """
    sku: str = Field(..., min_length=5, description="Código único del producto")
    name: str = Field(..., min_length=3, description="Nombre del producto")
    description: str = Field(default="", description="Descripción del producto")
    price: float = Field(..., gt=0, description="Precio del producto")
    currency: str = Field(default="USD", description="Moneda del precio")
    initial_stock: int = Field(default=0, ge=0, description="Stock inicial")
    
    @field_validator('sku')
    @classmethod
    def validate_sku_format(cls, v: str) -> str:
        """Validación básica del formato SKU."""
        if not all(c.isalnum() or c == '-' for c in v):
            raise ValueError("SKU solo puede contener caracteres alfanuméricos y guiones")
        return v.upper()  # Normalizar a mayúsculas
    
    @field_validator('price')
    @classmethod
    def validate_price_decimals(cls, v: float) -> float:
        """Validar que el precio tenga máximo 2 decimales."""
        if round(v, 2) != v:
            raise ValueError("El precio no puede tener más de 2 decimales")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "sku": "PROD-12345",
                "name": "Laptop Dell XPS 15",
                "description": "Laptop de alto rendimiento",
                "price": 1299.99,
                "currency": "USD",
                "initial_stock": 10
            }
        }
