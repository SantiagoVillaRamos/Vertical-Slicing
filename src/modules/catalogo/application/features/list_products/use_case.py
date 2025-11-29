"""
Caso de uso para listar productos.
"""
from typing import List

from src.modules.catalogo.application.interfaces import IListProductsUseCase
from src.modules.catalogo.domain.repositories import ProductRepository
from src.modules.catalogo.domain.entities import Product


class ListProductsUseCase(IListProductsUseCase):
    """
    Caso de uso: Listar Productos.
    Obtiene una lista paginada de productos del repositorio.
    """
    
    def __init__(self, repository: ProductRepository):
        self.repository = repository
    
    async def execute(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """
        Ejecuta la lógica de negocio.
        
        Args:
            skip: Cantidad de registros a saltar
            limit: Cantidad máxima de registros a retornar
            
        Returns:
            Lista de entidades de dominio Product
        """
        # Obtener y retornar entidades del dominio directamente
        return await self.repository.get_all(skip, limit)
