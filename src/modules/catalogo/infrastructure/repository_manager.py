"""
Gestor Singleton para Repositorios del módulo Catálogo.
Garantiza una única instancia de repositorio por sesión de BD.
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.catalogo.infrastructure.repositories import SQLAlchemyProductRepository
from src.modules.catalogo.domain.repositories import ProductRepository


class RepositoryManager:
    """
    Singleton para gestionar instancias de repositorios.
    
    Este patrón asegura que:
    1. Solo existe una instancia del repositorio por sesión
    2. Se reutiliza la misma instancia en múltiples casos de uso
    3. Se optimiza el uso de recursos
    
    Beneficios:
    - Eficiencia: Reutiliza instancias del repositorio
    - Consistencia: Misma instancia en toda la request
    - Gestión centralizada: Un solo punto para obtener repositorios
    """
    
    _instance: Optional['RepositoryManager'] = None
    _product_repository: Optional[ProductRepository] = None
    _current_session: Optional[AsyncSession] = None
    
    def __new__(cls):
        """
        Implementación del patrón Singleton.
        
        Garantiza que solo exista una instancia de RepositoryManager
        en toda la aplicación.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_product_repository(self, session: AsyncSession) -> ProductRepository:
        """
        Obtiene la instancia del repositorio de productos.
        
        Si la sesión cambia, crea una nueva instancia.
        Si la sesión es la misma, reutiliza la instancia existente.
        
        Args:
            session: Sesión de base de datos
            
        Returns:
            Instancia del repositorio de productos
        """
        # Si la sesión cambió o no hay repositorio, crear uno nuevo
        if self._current_session is not session or self._product_repository is None:
            self._current_session = session
            self._product_repository = SQLAlchemyProductRepository(session)
        
        return self._product_repository
    
    def reset(self):
        """
        Resetea el singleton (útil para testing).
        
        Limpia las referencias a repositorios y sesiones,
        permitiendo crear nuevas instancias.
        """
        self._product_repository = None
        self._current_session = None
