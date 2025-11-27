"""
Script para verificar conexión a PostgreSQL.
"""
import psycopg2

try:
    # Intentar conectar
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="ecommerce",
        user="postgres",
        password="postgres"
    )
    
    print("✅ Conexión exitosa a PostgreSQL!")
    
    # Crear un cursor y ejecutar una consulta simple
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print(f"📊 Versión de PostgreSQL: {version[0]}")
    
    # Cerrar
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error de conexión: {e}")
