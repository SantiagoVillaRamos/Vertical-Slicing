"""
Script temporal para inicializar la base de datos con credenciales correctas.
"""
import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine

# Configurar la URL correcta con el PUERTO 5433
os.environ['DATABASE_URL'] = 'postgresql://postgres:postgres@localhost:5433/ecommerce'

from src.core.database import Base
from src.modules.catalogo.infrastructure.models import ProductModel
from src.modules.pedidos.infrastructure.models import OrderModel, OrderItemModel


async def init_db():
    """Crea todas las tablas en la base de datos."""
    
    # URL correcta para asyncpg en puerto 5433
    async_database_url = "postgresql+asyncpg://postgres:postgres@localhost:5433/ecommerce"
    
    # Crear engine
    engine = create_async_engine(async_database_url, echo=True)
    
    print("🔧 Creando tablas en la base de datos (Puerto 5433)...")
    
    async with engine.begin() as conn:
        # Crear todas las tablas
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ Tablas creadas exitosamente!")
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_db())
