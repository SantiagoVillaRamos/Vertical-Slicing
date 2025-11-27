"""
Script para inicializar la base de datos.
Crea todas las tablas definidas en los modelos SQLAlchemy.
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from src.core.config import settings
from src.core.database import Base

# Importar todos los modelos para que SQLAlchemy los registre
from src.modules.catalogo.infrastructure.models import ProductModel
from src.modules.pedidos.infrastructure.models import OrderModel, OrderItemModel


async def init_db():
    """Crea todas las tablas en la base de datos."""
    
    # Convertir URL a async
    async_database_url = settings.database_url.replace(
        "postgresql://", "postgresql+asyncpg://"
    )
    
    # Crear engine
    engine = create_async_engine(async_database_url, echo=True)
    
    print("🔧 Creando tablas en la base de datos...")
    
    async with engine.begin() as conn:
        # Crear todas las tablas
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ Tablas creadas exitosamente!")
    
    await engine.dispose()


async def drop_db():
    """Elimina todas las tablas de la base de datos."""
    
    # Convertir URL a async
    async_database_url = settings.database_url.replace(
        "postgresql://", "postgresql+asyncpg://"
    )
    
    # Crear engine
    engine = create_async_engine(async_database_url, echo=True)
    
    print("⚠️  Eliminando todas las tablas...")
    
    async with engine.begin() as conn:
        # Eliminar todas las tablas
        await conn.run_sync(Base.metadata.drop_all)
    
    print("✅ Tablas eliminadas!")
    
    await engine.dispose()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "drop":
        # python -m src.scripts.init_db drop
        asyncio.run(drop_db())
    else:
        # python -m src.scripts.init_db
        asyncio.run(init_db())
