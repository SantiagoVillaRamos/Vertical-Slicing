"""
Router de FastAPI para el módulo de Catálogo.
Define los endpoints HTTP para gestionar productos.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Annotated

from src.modules.catalogo.application.facade import CatalogoFacade
from src.modules.catalogo.application.features.create_product.command import CreateProductCommand
from src.modules.catalogo.application.features.create_product.response import CreateProductResponse
from src.modules.catalogo.api.dependencies import get_catalogo_facade
from src.core.exceptions import DomainError, BusinessRuleViolation, ValidationError


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
    Endpoint para crear un nuevo producto.
    Usa la Facade del módulo Catálogo.
    
    Args:
        command: Datos del producto a crear
        facade: Facade del módulo inyectada automáticamente
        
    Returns:
        Datos del producto creado
        
    Raises:
        HTTPException 400: Si hay errores de validación o reglas de negocio
        HTTPException 500: Si hay errores internos
    """
    try:
        # Ejecutar a través de la facade
        result = await facade.create_product(command)
        return result
        
    except ValidationError as e:
        # Errores de validación de dominio (ej: SKU inválido, precio negativo)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Validation Error", "message": e.message}
        )
        
    except BusinessRuleViolation as e:
        # Violaciones de reglas de negocio (ej: SKU duplicado)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Business Rule Violation", "message": e.message}
        )
        
    except DomainError as e:
        # Otros errores de dominio
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Domain Error", "message": e.message}
        )
        
    except Exception as e:
        # Errores inesperados
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Internal Server Error", "message": str(e)}
        )


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
    return await facade.list_products(skip, limit)


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
