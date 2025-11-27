"""
Adaptador del Repositorio de Productos usando SQLAlchemy.
Implementa el puerto ProductRepository definido en el dominio.
"""
from typing import Optional, List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.catalogo.domain.entities import Product
from src.modules.catalogo.domain.value_objects import SKU, Price, Stock
from src.modules.catalogo.domain.repositories import ProductRepository
from src.modules.catalogo.infrastructure.models import ProductModel


class SQLAlchemyProductRepository(ProductRepository):
    """
    Implementación del ProductRepository usando SQLAlchemy.
    
    Responsabilidades:
    1. Mapear entre entidades de dominio (Product) y modelos de BD (ProductModel)
    2. Ejecutar operaciones CRUD en la base de datos
    """
    
    def __init__(self, session: AsyncSession):
        """
        Constructor con inyección de la sesión de base de datos.
        
        Args:
            session: Sesión async de SQLAlchemy
        """
        self.session = session
    
    # Métodos de mapeo (Domain <-> ORM)
    
    def _to_domain(self, model: ProductModel) -> Product:
        """Convierte un ProductModel (ORM) a Product (Dominio)."""
        return Product(
            product_id=model.product_id,
            sku=SKU(value=model.sku),
            name=model.name,
            description=model.description,
            price=Price(amount=model.price_amount, currency=model.price_currency),
            stock=Stock(quantity=model.stock_quantity),
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _to_model(self, product: Product) -> ProductModel:
        """Convierte un Product (Dominio) a ProductModel (ORM)."""
        return ProductModel(
            product_id=product.product_id,
            sku=str(product.sku),
            name=product.name,
            description=product.description,
            price_amount=product.price.amount,
            price_currency=product.price.currency,
            stock_quantity=product.stock.quantity,
            is_active=product.is_active,
            created_at=product.created_at,
            updated_at=product.updated_at
        )
    
    # Implementación de los métodos del puerto
    
    async def save(self, product: Product) -> Product:
        """Guarda un nuevo producto en la base de datos."""
        model = self._to_model(product)
        self.session.add(model)
        await self.session.flush()  # Para obtener el ID generado
        await self.session.refresh(model)
        return self._to_domain(model)
    
    async def update(self, product: Product) -> Product:
        """Actualiza un producto existente."""
        # Buscar el modelo existente
        stmt = select(ProductModel).where(ProductModel.product_id == product.product_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if not model:
            raise ValueError(f"Producto con ID {product.product_id} no encontrado")
        
        # Actualizar campos
        model.sku = str(product.sku)
        model.name = product.name
        model.description = product.description
        model.price_amount = product.price.amount
        model.price_currency = product.price.currency
        model.stock_quantity = product.stock.quantity
        model.is_active = product.is_active
        model.updated_at = product.updated_at
        
        await self.session.flush()
        await self.session.refresh(model)
        return self._to_domain(model)
    
    async def get_by_id(self, product_id: UUID) -> Optional[Product]:
        """Busca un producto por su ID."""
        stmt = select(ProductModel).where(ProductModel.product_id == product_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        return self._to_domain(model) if model else None
    
    async def get_by_sku(self, sku: SKU) -> Optional[Product]:
        """Busca un producto por su SKU."""
        stmt = select(ProductModel).where(ProductModel.sku == str(sku))
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        return self._to_domain(model) if model else None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """Obtiene todos los productos con paginación."""
        stmt = select(ProductModel).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        
        return [self._to_domain(model) for model in models]
    
    async def delete(self, product_id: UUID) -> bool:
        """Elimina un producto por su ID."""
        stmt = select(ProductModel).where(ProductModel.product_id == product_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if not model:
            return False
        
        await self.session.delete(model)
        await self.session.flush()
        return True
    
    async def exists_by_sku(self, sku: SKU) -> bool:
        """Verifica si existe un producto con el SKU dado."""
        stmt = select(ProductModel.product_id).where(ProductModel.sku == str(sku))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None
