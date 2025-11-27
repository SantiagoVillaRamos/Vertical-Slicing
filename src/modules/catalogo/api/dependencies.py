"""
Funciones de Inyección de Dependencias para el módulo de Catálogo.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.core.database import get_db_session
from src.modules.catalogo.infrastructure.repositories import SQLAlchemyProductRepository
from src.modules.catalogo.application.features.create_product.use_case import CreateProductUseCase


# Dependency: Product Repository
async def get_product_repository(
    session: AsyncSession = Depends(get_db_session)
) -> SQLAlchemyProductRepository:
    """
    Inyecta el repositorio de productos.
    
    Args:
        session: Sesión de base de datos (inyectada automáticamente)
        
    Returns:
        Instancia del repositorio de productos
    """
    return SQLAlchemyProductRepository(session)


# Dependency: CreateProduct Use Case
async def get_create_product_use_case(
    repository: SQLAlchemyProductRepository = Depends(get_product_repository)
) -> CreateProductUseCase:
    """
    Inyecta el caso de uso CreateProduct.
    
    Args:
        repository: Repositorio de productos (inyectado automáticamente)
        
    Returns:
        Instancia del caso de uso
    """
    return CreateProductUseCase(repository)


# Dependency: ListProducts Use Case
async def get_list_products_use_case(
    repository: SQLAlchemyProductRepository = Depends(get_product_repository)
) -> "ListProductsUseCase":
    """Inyecta el caso de uso ListProducts."""
    from src.modules.catalogo.application.features.list_products.use_case import ListProductsUseCase
    return ListProductsUseCase(repository)
