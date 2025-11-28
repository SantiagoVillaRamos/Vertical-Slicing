"""
Factories del dominio de Catálogo.
Los factories encapsulan la lógica compleja de creación de entidades.
"""
from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from src.modules.catalogo.domain.entities import Product
from src.modules.catalogo.domain.value_objects import SKU, Price, Stock


@dataclass
class ProductCreationData:
    """
    DTO interno del dominio para datos de creación de producto.
    Encapsula los datos primitivos necesarios para crear un Product.
    """
    sku: str
    name: str
    description: str
    price: float
    currency: str
    initial_stock: int
    product_id: Optional[UUID] = None



class ProductFactory:
    """
    Factory Method para crear productos.
    
    Responsabilidades:
    1. Crear y validar Value Objects (SKU, Price, Stock)
    2. Aplicar reglas de negocio de construcción
    3. Construir la entidad Product con todos sus invariantes
    
    Nota: Este factory NO valida unicidad de SKU, esa es una 
    regla de aplicación que requiere acceso al repositorio.
    """
    
    @staticmethod
    def create(data: ProductCreationData) -> Product:
        """
        Crea un nuevo producto a partir de datos primitivos.
        
        Args:
            data: Datos de creación del producto
            
        Returns:
            Product: Entidad Product completamente construida y validada
            
        Raises:
            ValidationError: Si los Value Objects no son válidos
            BusinessRuleViolation: Si las reglas de la entidad no se cumplen
        """
        # 1. Crear Value Objects (aquí se validan automáticamente)
        sku = SKU(value=data.sku)
        price = Price(amount=data.price, currency=data.currency)
        stock = Stock(quantity=data.initial_stock)
        
        # 2. Crear la entidad Product
        # (las validaciones de la entidad se ejecutan en __post_init__)
        product = Product(
            sku=sku,
            name=data.name,
            description=data.description,
            price=price,
            stock=stock
        )
        
        # 3. Si se proporciona un ID específico, usarlo
        if data.product_id:
            object.__setattr__(product, 'product_id', data.product_id)
        
        return product
    
    @staticmethod
    def create_from_primitives(
        sku: str,
        name: str,
        description: str,
        price: float,
        currency: str,
        initial_stock: int,
        product_id: Optional[UUID] = None
    ) -> Product:
        """
        Método de conveniencia para crear un producto desde primitivos.
        
        Este método es útil cuando no quieres crear explícitamente
        un ProductCreationData.
        """
        data = ProductCreationData(
            sku=sku,
            name=name,
            description=description,
            price=price,
            currency=currency,
            initial_stock=initial_stock,
            product_id=product_id
        )
        return ProductFactory.create(data)
        