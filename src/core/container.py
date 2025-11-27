"""
Contenedor de Inyección de Dependencias (DI).
Patrón Composition Root para gestionar dependencias.
"""
from typing import Callable, Dict, Any


class DIContainer:
    """
    Contenedor simple de DI para gestionar dependencias.
    Cada módulo registrará sus propias dependencias.
    """
    
    def __init__(self):
        self._services: Dict[str, Callable] = {}
    
    def register(self, name: str, factory: Callable):
        """Registra una factory para crear instancias de servicios."""
        self._services[name] = factory
    
    def resolve(self, name: str) -> Any:
        """Resuelve y retorna una instancia del servicio."""
        if name not in self._services:
            raise ValueError(f"Servicio '{name}' no registrado en el contenedor DI")
        
        factory = self._services[name]
        return factory()
    
    def clear(self):
        """Limpia todas las dependencias registradas."""
        self._services.clear()


# Singleton del contenedor
container = DIContainer()
