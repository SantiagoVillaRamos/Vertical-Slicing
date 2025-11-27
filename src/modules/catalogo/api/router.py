"""
Router de FastAPI para el módulo de Catálogo.
Define los endpoints HTTP para gestionar productos.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from src.modules.catalogo.application.features.create_product.command import CreateProductCommand
from src.modules.catalogo.application.features.create_product.response import CreateProductResponse
from src.modules.catalogo.application.features.create_product.use_case import CreateProductUseCase
from src.modules.catalogo.application.features.list_products.use_case import ListProductsUseCase
from src.modules.catalogo.api.dependencies import get_create_product_use_case, get_list_products_use_case
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
    use_case: CreateProductUseCase = Depends(get_create_product_use_case)
) -> CreateProductResponse:
    """
    Endpoint para crear un nuevo producto.
    
    Args:
        command: Datos del producto a crear
        use_case: Caso de uso inyectado automáticamente
        
    Returns:
        Datos del producto creado
        
    Raises:
        HTTPException 400: Si hay errores de validación o reglas de negocio
        HTTPException 500: Si hay errores internos
    """
    try:
        # Ejecutar el caso de uso
        result = await use_case.execute(command)
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
    skip: int = 0,
    limit: int = 100,
    use_case: ListProductsUseCase = Depends(get_list_products_use_case)
) -> List[CreateProductResponse]:
    """
    Endpoint para listar productos.
    """
    return await use_case.execute(skip, limit)


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
