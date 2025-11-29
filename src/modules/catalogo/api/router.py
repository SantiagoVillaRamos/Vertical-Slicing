"""
Router de FastAPI para el módulo de Catálogo.
Define los endpoints HTTP para gestionar productos.
"""
from fastapi import APIRouter, Depends, status
from typing import List, Annotated

from src.modules.catalogo.application.facade import CatalogoFacade
from src.modules.catalogo.application.features.create_product.command import CreateProductCommand
from src.modules.catalogo.application.features.create_product.response import CreateProductResponse
from src.modules.catalogo.api.dependencies import get_catalogo_facade


from src.modules.catalogo.api.mappers import ProductDTOMapper

# Router del módulo
router = APIRouter()


@router.post(
    "/products",
    response_model=CreateProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo producto",
    description="Crea un nuevo producto en el catálogo con validación de SKU único"
)
async def create_product(
    command: CreateProductCommand,
    facade: Annotated[CatalogoFacade, Depends(get_catalogo_facade)]
) -> CreateProductResponse:
    """
    Crea un nuevo producto en el catálogo.
    
    Las excepciones son manejadas automáticamente por los exception handlers globales.
    
    Args:
        command: Datos del producto a crear
        facade: Facade del módulo inyectada automáticamente
        
    Returns:
        Datos del producto creado
    """
    
    # 1. Pasar la entidad a la facade
    saved_product = await facade.create_product(command)
    
    # 2. Mapear a DTO de respuesta
    return ProductDTOMapper.domain_to_response(saved_product)


@router.get(
    "/products",
    response_model=List[CreateProductResponse],
    summary="Listar productos",
    description="Obtiene una lista paginada de productos"
)
async def list_products(
    facade: Annotated[CatalogoFacade, Depends(get_catalogo_facade)],
    skip: int = 0,
    limit: int = 100
) -> List[CreateProductResponse]:
    """
    Endpoint para listar productos.
    Usa la Facade del módulo Catálogo.
    
    Args:
        skip: Número de registros a saltar (paginación)
        limit: Número máximo de registros a retornar
        facade: Facade del módulo inyectada automáticamente
        
    Returns:
        Lista de productos
    """
    # La facade retorna una lista de entidades de dominio
    products = await facade.list_products(skip, limit)
    
    # Mapeamos a lista de DTOs de respuesta
    return [ProductDTOMapper.domain_to_response(p) for p in products]


@router.get(
    "/health",
    summary="Health check del módulo Catálogo"
)
async def health_check():
    """Endpoint de salud del módulo."""
    return {
        "module": "catalogo",
        "status": "healthy"
    }
