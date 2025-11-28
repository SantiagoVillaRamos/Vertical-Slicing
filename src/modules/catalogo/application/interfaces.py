"""
Interfaces (Puertos) para los Casos de Uso del módulo Catálogo.
Estas interfaces permiten la inversión de dependencias (Dependency Inversion Principle).
"""
from abc import ABC, abstractmethod
from typing import List

from src.modules.catalogo.application.features.create_product.command import CreateProductCommand
from src.modules.catalogo.application.features.create_product.response import CreateProductResponse
from src.modules.catalogo.application.features.reserve_stock.command import ReserveStockCommand
from src.modules.catalogo.application.features.reserve_stock.response import ReserveStockResponse


class ICreateProductUseCase(ABC):
    """
    Interfaz para el caso de uso de crear producto.
    
    Esta interfaz define el contrato que debe cumplir cualquier
    implementación del caso de uso de creación de productos.
    """
    
    @abstractmethod
    async def execute(self, command: CreateProductCommand) -> CreateProductResponse:
        """
        Ejecuta la creación de un producto.
        
        Args:
            command: Datos del producto a crear
            
        Returns:
            Respuesta con los datos del producto creado
            
        Raises:
            BusinessRuleViolation: Si el SKU ya existe o hay violaciones de negocio
            ValidationError: Si los datos no son válidos
        """
        pass


class IListProductsUseCase(ABC):
    """
    Interfaz para el caso de uso de listar productos.
    
    Esta interfaz define el contrato que debe cumplir cualquier
    implementación del caso de uso de listado de productos.
    """
    
    @abstractmethod
    async def execute(self, skip: int = 0, limit: int = 100) -> List[CreateProductResponse]:
        """
        Ejecuta el listado de productos.
        
        Args:
            skip: Número de registros a saltar (paginación)
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de productos
        """
        pass


class IReserveStockUseCase(ABC):
    """
    Interfaz para el caso de uso de reservar stock.
    
    Esta interfaz define el contrato que debe cumplir cualquier
    implementación del caso de uso de reserva de stock.
    """
    
    @abstractmethod
    async def execute(self, command: ReserveStockCommand) -> ReserveStockResponse:
        """
        Ejecuta la reserva de stock.
        
        Args:
            command: Datos de los productos y cantidades a reservar
            
        Returns:
            Respuesta con el resultado de la reserva
            
        Raises:
            NotFoundError: Si algún producto no existe
            BusinessRuleViolation: Si no hay stock suficiente
        """
        pass
