"""
Caso de uso para listar productos.
"""
from typing import List

from src.modules.catalogo.application.interfaces import IListProductsUseCase
from src.modules.catalogo.domain.repositories import ProductRepository
from src.modules.catalogo.application.features.create_product.response import CreateProductResponse


class ListProductsUseCase(IListProductsUseCase):
    """
    Caso de uso: Listar Productos.
    Obtiene una lista paginada de productos del repositorio.
    """
    
    def __init__(self, repository: ProductRepository):
        self.repository = repository
    
    async def execute(self, skip: int = 0, limit: int = 100) -> List[CreateProductResponse]:
        """
        Ejecuta la lógica de negocio.
        
        Args:
            skip: Cantidad de registros a saltar
            limit: Cantidad máxima de registros a retornar
            
        Returns:
            Lista de DTOs de productos
        """
        # Obtener entidades del dominio
        products = await self.repository.get_all(skip, limit)
        
        # Convertir a DTOs de respuesta
        return [
            CreateProductResponse(
                product_id=p.product_id,
                sku=str(p.sku),
                name=p.name,
                description=p.description,
                price=p.price.amount,
                currency=p.price.currency,
                stock=p.stock.quantity,
                is_active=p.is_active,
                created_at=p.created_at
            )
            for p in products
        ]
