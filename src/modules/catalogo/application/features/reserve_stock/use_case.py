"""
Caso de Uso: Reservar Stock de Productos.
Este use case es llamado por el módulo de Pedidos via el Gateway.
"""
from typing import List
from src.modules.catalogo.application.features.reserve_stock.command import ReserveStockCommand
from src.modules.catalogo.application.features.reserve_stock.response import (
    ReserveStockResponse, ProductStockInfo
)
from src.modules.catalogo.domain.repositories import ProductRepository
from src.core.exceptions import BusinessRuleViolation, NotFoundError


class ReserveStockUseCase:
    """
    Caso de Uso: Reservar stock de múltiples productos.
    
    Este use case es CRUCIAL para la comunicación entre módulos.
    Es llamado por el módulo de Pedidos cuando se crea una orden.
    
    Responsabilidades:
    1. Verificar que todos los productos existan
    2. Verificar que haya stock suficiente para todos los items
    3. Reservar el stock (reducir la cantidad disponible)
    4. Operación transaccional: todo o nada
    """
    
    def __init__(self, product_repository: ProductRepository):
        """
        Constructor con Inyección de Dependencias.
        
        Args:
            product_repository: Implementación del puerto ProductRepository
        """
        self.product_repository = product_repository
    
    async def execute(self, command: ReserveStockCommand) -> ReserveStockResponse:
        """
        Ejecuta el caso de uso.
        
        Args:
            command: Datos de entrada con los items a reservar
            
        Returns:
            ReserveStockResponse con el resultado de la reserva
            
        Raises:
            NotFoundError: Si algún producto no existe
            BusinessRuleViolation: Si no hay stock suficiente
        """
        products_info: List[ProductStockInfo] = []
        
        # Fase 1: Verificar que todos los productos existan y tengan stock
        for item in command.items:
            product = await self.product_repository.get_by_id(item.product_id)
            
            if not product:
                raise NotFoundError("Product", str(item.product_id))
            
            # Verificar stock disponible
            if not product.stock.is_available(item.quantity):
                raise BusinessRuleViolation(
                    f"Stock insuficiente para el producto '{product.name}'. "
                    f"Disponible: {product.stock.quantity}, Solicitado: {item.quantity}"
                )
        
        # Fase 2: Reservar stock (si llegamos aquí, todo está OK)
        for item in command.items:
            product = await self.product_repository.get_by_id(item.product_id)
            
            # Reservar stock (esto reduce la cantidad)
            product.reserve_stock(item.quantity)
            
            # Actualizar en la base de datos
            updated_product = await self.product_repository.update(product)
            
            # Agregar información del producto
            products_info.append(
                ProductStockInfo(
                    product_id=updated_product.product_id,
                    product_name=updated_product.name,
                    sku=str(updated_product.sku),
                    requested_quantity=item.quantity,
                    reserved_quantity=item.quantity,
                    remaining_stock=updated_product.stock.quantity,
                    unit_price=updated_product.price.amount
                )
            )
        
        return ReserveStockResponse(
            success=True,
            products=products_info,
            message=f"Stock reservado exitosamente para {len(products_info)} producto(s)"
        )
