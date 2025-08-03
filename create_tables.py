#!/usr/bin/env python3
"""
Script para crear la tabla LINKS en Railway MySQL
"""
import os
import mysql.connector
from mysql.connector import Error

def create_table():
    connection = None
    try:
        # Variables de entorno que obtenemos de Railway
        mysql_public_url = os.getenv('MYSQL_PUBLIC_URL', '')
        mysql_host = os.getenv('RAILWAY_TCP_PROXY_DOMAIN', 'trolley.proxy.rlwy.net')
        mysql_port = int(os.getenv('RAILWAY_TCP_PROXY_PORT', '14109'))
        mysql_user = os.getenv('MYSQLUSER', 'root')
        mysql_password = os.getenv('MYSQLPASSWORD', '')
        mysql_database = os.getenv('MYSQLDATABASE', 'railway')
        
        print(f"Conectando a: {mysql_host}:{mysql_port}")
        print(f"Usuario: {mysql_user}")
        print(f"Base de datos: {mysql_database}")
        
        # Configuración de conexión usando la URL pública de Railway
        connection = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_database,
            port=mysql_port
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Crear la base de datos si no existe
            cursor.execute("CREATE DATABASE IF NOT EXISTS railway")
            cursor.execute("USE railway")
            
            # Crear la tabla LINKS
            create_table_query = """
            CREATE TABLE IF NOT EXISTS LINKS (
                id INT AUTO_INCREMENT PRIMARY KEY,
                URL TEXT NOT NULL,
                SHORT_LINK VARCHAR(10) NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            cursor.execute(create_table_query)
            print("Tabla LINKS creada correctamente")
            
            # Verificar que la tabla existe
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print("Tablas en la base de datos:")
            for table in tables:
                print(f"   - {table[0]}")
            
            # Insertar datos de ejemplo (opcional)
            cursor.execute("SELECT COUNT(*) FROM LINKS")
            count = cursor.fetchone()[0]
            
            if count == 0:
                cursor.execute(
                    "INSERT INTO LINKS (URL, SHORT_LINK) VALUES (%s, %s)",
                    ('https://example.com', 'example')
                )
                connection.commit()
                print("Datos de ejemplo insertados")
            
            cursor.close()
            
    except Error as e:
        print(f"Error al conectar con MySQL: {e}")
    
    finally:
        if connection.is_connected():
            connection.close()
            print("Conexión cerrada")

if __name__ == "__main__":
    print("Iniciando creación de tabla en Railway MySQL")
    create_table()
    print("Proceso completado")
