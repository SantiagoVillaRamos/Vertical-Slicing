"""
Mappers de la capa API para el módulo de Catálogo.
Responsable de convertir entre DTOs (Commands/Responses) y entidades de dominio.

IMPORTANTE: Estos mappers pertenecen a la capa de API, NO a la capa de aplicación.
Los casos de uso trabajan directamente con entidades de dominio.
"""
from src.modules.catalogo.application.features.create_product.command import CreateProductCommand
from src.modules.catalogo.application.features.create_product.response import CreateProductResponse
from src.modules.catalogo.domain.entities import Product


class ProductDTOMapper:
    """
    Mapper estático para convertir entre DTOs y entidades de dominio.
    
    Responsabilidades:
    - Convertir Commands a entidades de dominio
    - Convertir entidades de dominio a Response DTOs
    - Centralizar la lógica de transformación de datos entre la API y el dominio
    
    NOTA: Esta clase pertenece a la capa de API, no a la capa de aplicación.
    Los casos de uso NO deben depender de esta clase.
    """
    
    @staticmethod
    def domain_to_response(product: Product) -> CreateProductResponse:
        """
        Convierte una entidad Product a CreateProductResponse.
        
        Args:
            product: Entidad de dominio
            
        Returns:
            DTO de salida con los datos del producto
        """
        return CreateProductResponse(
            product_id=product.product_id,
            sku=str(product.sku),
            name=product.name,
            description=product.description,
            price=product.price.amount,
            currency=product.price.currency,
            stock=product.stock.quantity,
            is_active=product.is_active,
            created_at=product.created_at
        )
