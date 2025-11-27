"""
Excepciones base del dominio.
Estas excepciones son compartidas por todos los módulos.
"""


class DomainError(Exception):
    """Excepción base para errores de dominio."""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class NotFoundError(DomainError):
    """Excepción cuando una entidad no se encuentra."""
    
    def __init__(self, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id
        message = f"{entity_name} con ID '{entity_id}' no encontrado"
        super().__init__(message)


class ValidationError(DomainError):
    """Excepción para errores de validación de dominio."""
    pass


class BusinessRuleViolation(DomainError):
    """Excepción cuando se viola una regla de negocio."""
    pass
