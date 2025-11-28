"""
Caso de Uso: Crear Producto.
Orquesta la lógica de aplicación para crear un producto.
"""
from src.modules.catalogo.application.features.create_product.command import CreateProductCommand
from src.modules.catalogo.application.features.create_product.response import CreateProductResponse
from src.modules.catalogo.application.interfaces import ICreateProductUseCase
from src.modules.catalogo.domain.entities import Product
from src.modules.catalogo.domain.value_objects import SKU, Price, Stock
from src.modules.catalogo.domain.factories import ProductFactory
from src.modules.catalogo.domain.repositories import ProductRepository
from src.core.exceptions import BusinessRuleViolation


class CreateProductUseCase(ICreateProductUseCase):
    """
    Caso de Uso: Crear un nuevo producto en el catálogo.
    
    Responsabilidades:
    1. Validar que el SKU no exista
    2. Crear la entidad Product con los Value Objects
    3. Persistir usando el repositorio
    """
    
    def __init__(self, product_repository: ProductRepository):
        """
        Constructor con Inyección de Dependencias.
        
        Args:
            product_repository: Implementación del puerto ProductRepository
        """
        self.product_repository = product_repository
    
    async def execute(self, command: CreateProductCommand) -> CreateProductResponse:
        """
        Ejecuta el caso de uso.
        
        Args:
            command: Datos de entrada para crear el producto
            
        Returns:
            CreateProductResponse con los datos del producto creado
            
        Raises:
            BusinessRuleViolation: Si el SKU ya existe o hay violaciones de negocio
        """
        # 1. Crear la entidad Product usando el Factory
        # (el factory crea los VOs y valida las reglas de construcción)
        product = ProductFactory.create_from_primitives(
            sku=command.sku,
            name=command.name,
            description=command.description,
            price=command.price,
            currency=command.currency,
            initial_stock=command.initial_stock
        )
        # 2. Verificar que el SKU no exista (regla de aplicación)
        if await self.product_repository.exists_by_sku(product.sku):
            raise BusinessRuleViolation(
                f"Ya existe un producto con el SKU: {product.sku}"
            )
        
        # 3. Persistir usando el repositorio
        saved_product = await self.product_repository.save(product)
        
        # 5. Mapear a Response DTO
        return CreateProductResponse(
            product_id=saved_product.product_id,
            sku=str(saved_product.sku),
            name=saved_product.name,
            description=saved_product.description,
            price=saved_product.price.amount,
            currency=saved_product.price.currency,
            stock=saved_product.stock.quantity,
            is_active=saved_product.is_active,
            created_at=saved_product.created_at
        )
