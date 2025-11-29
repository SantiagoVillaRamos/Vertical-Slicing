"""
Mappers de Infraestructura para el módulo de Catálogo.
Responsable de convertir entre entidades de dominio y modelos ORM.
"""
from src.modules.catalogo.domain.entities import Product
from src.modules.catalogo.domain.value_objects import SKU, Price, Stock
from src.modules.catalogo.infrastructure.models import ProductModel


class ProductMapper:
    """
    Mapper estático para convertir entre Product (dominio) y ProductModel (ORM).
    
    Responsabilidades:
    - Convertir de modelo ORM a entidad de dominio
    - Convertir de entidad de dominio a modelo ORM
    - Actualizar modelos ORM existentes con datos de entidades de dominio
    """
    
    @staticmethod
    def to_domain(model: ProductModel) -> Product:
        """
        Convierte un ProductModel (ORM) a Product (entidad de dominio).
        
        Args:
            model: Modelo ORM de SQLAlchemy
            
        Returns:
            Entidad de dominio Product
        """
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
    
    @staticmethod
    def to_model(product: Product) -> ProductModel:
        """
        Convierte un Product (entidad de dominio) a ProductModel (ORM).
        
        Args:
            product: Entidad de dominio
            
        Returns:
            Modelo ORM de SQLAlchemy
        """
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
    
    @staticmethod
    def update_model(model: ProductModel, product: Product) -> ProductModel:
        """
        Actualiza un ProductModel existente con datos de una entidad Product.
        
        Útil para operaciones de actualización donde ya tenemos un modelo
        cargado de la base de datos.
        
        Args:
            model: Modelo ORM existente a actualizar
            product: Entidad de dominio con los nuevos datos
            
        Returns:
            El mismo modelo actualizado (para encadenamiento)
        """
        model.sku = str(product.sku)
        model.name = product.name
        model.description = product.description
        model.price_amount = product.price.amount
        model.price_currency = product.price.currency
        model.stock_quantity = product.stock.quantity
        model.is_active = product.is_active
        model.updated_at = product.updated_at
        
        return model
