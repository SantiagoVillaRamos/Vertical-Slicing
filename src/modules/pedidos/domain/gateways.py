"""
Puertos de Gateway para comunicación con otros módulos.
Este es el patrón clave para la comunicación entre contextos delimitados.
"""
from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from src.modules.pedidos.domain.entities import OrderItem
from src.core.exceptions import DomainError


class StockReservationError(DomainError):
    """Excepción cuando no se puede reservar stock."""
    pass


class InventoryGateway(ABC):
    """
    Puerto del Gateway de Inventario.
    
    Este puerto define CÓMO el módulo de Pedidos quiere comunicarse
    con el módulo de Catálogo, sin conocer los detalles de implementación.
    
    Responsabilidad: Verificar disponibilidad y reservar stock de productos.
    """
    
    @abstractmethod
    async def verify_and_reserve_stock(self, items: List[OrderItem]) -> bool:
        """
        Verifica disponibilidad y reserva stock para los items de una orden.
        
        Args:
            items: Lista de items a reservar
            
        Returns:
            True si se pudo reservar todo el stock
            
        Raises:
            StockReservationError: Si no hay stock suficiente o hay algún error
        """
        pass
    
    @abstractmethod
    async def release_stock(self, items: List[OrderItem]) -> bool:
        """
        Libera stock previamente reservado (en caso de cancelación).
        
        Args:
            items: Lista de items cuyo stock se debe liberar
            
        Returns:
            True si se liberó el stock correctamente
        """
        pass
    
    @abstractmethod
    async def verify_product_exists(self, product_id: UUID) -> bool:
        """
        Verifica si un producto existe en el catálogo.
        
        Args:
            product_id: ID del producto a verificar
            
        Returns:
            True si el producto existe
        """
        pass
