import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import mysql.connector
from mysql.connector import pooling
import shortuuid

# init app
app = Flask(__name__)

# endpoint - usar variable de entorno en producción
endpoint = os.getenv('APP_URL', 'https://opti-url.up.railway.app')

# mysql connection config
mysql_config = {
    'host': os.getenv('MYSQLHOST', 'localhost'),
    'user': os.getenv('MYSQLUSER', 'root'),
    'password': os.getenv('MYSQLPASSWORD', 'P@u102018.180905'),
    'database': os.getenv('MYSQLDATABASE', 'railway'),
    'port': int(os.getenv('MYSQLPORT', '3306')),
    'charset': 'utf8mb4',
    'autocommit': True,
    'connection_timeout': 20,
    'use_pure': True,
    'sql_mode': '',
    'raise_on_warnings': False
}

# Alternative external config (fallback)
mysql_external_config = {
    'host': os.getenv('MYSQL_PUBLIC_HOST', mysql_config['host']),
    'user': mysql_config['user'],
    'password': mysql_config['password'],
    'database': mysql_config['database'],
    'port': int(os.getenv('MYSQL_PUBLIC_PORT', mysql_config['port'])),
    'charset': 'utf8mb4',
    'autocommit': True,
    'connection_timeout': 20,
    'use_pure': True,
    'sql_mode': '',
    'raise_on_warnings': False
}

# create connection pool
def get_db_connection():
    try:
        # Try external connection first (more reliable for Railway)
        print("Trying external connection...")
        return mysql.connector.connect(**mysql_external_config)
    except Exception as external_error:
        print(f"Error with external connection: {external_error}")
        try:
            # Try internal connection as fallback
            print("Trying internal connection...")
            return mysql.connector.connect(**mysql_config)
        except Exception as internal_error:
            print(f"Error with internal connection: {internal_error}")
            raise external_error  # Raise the external error since it's preferred

# Función para inicializar la base de datos
def init_database():
    try:
        print("Intentando inicializar base de datos...")
        print(f"Conectando a: {mysql_config['host']}:{mysql_config['port']}")
        print(f"Usuario: {mysql_config['user']}")
        print(f"Base de datos: {mysql_config['database']}")
        
        connection = get_db_connection()
        print("Conexión establecida exitosamente")
        
        cursor = connection.cursor()
        print("Cursor creado")
        
        # Crear la tabla LINKS si no existe
        create_table_query = """
        CREATE TABLE IF NOT EXISTS links (
            id INT AUTO_INCREMENT PRIMARY KEY,
            url TEXT NOT NULL,
            short_link TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        print("Ejecutando query de creación de tabla...")
        cursor.execute(create_table_query)
        connection.commit()
        print("Tabla creada y commit realizado")
        
        # Verificar que la tabla existe
        cursor.execute("SHOW TABLES LIKE 'links'")
        result = cursor.fetchone()
        print(f"Verificación de tabla: {result}")
        
        cursor.close()
        connection.close()
        print("Tabla links inicializada correctamente")
        return True
        
    except Exception as e:
        print(f"Error inicializando base de datos: {e}")
        print(f"Tipo de error: {type(e).__name__}")
        print(f"Detalles del error: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

# La inicialización se hace bajo demanda en la primera consulta

# set secret key - usar variable de entorno
app.secret_key = os.getenv('SECRET_KEY', 'C14v3S3cr3t4')

# init route
@app.route('/', methods = ['GET'])
def inicio():
    try:
        return render_template('index.html'), 200
    except: 
        return render_template('404.html'), 404

# Health check endpoint
@app.route('/health', methods = ['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'App is running'}), 200

# Database configuration diagnostic endpoint
@app.route('/db-config', methods = ['GET'])
def db_config():
    return jsonify({
        'internal_config': {
            'mysql_host': os.getenv('MYSQLHOST', 'NOT_SET'),
            'mysql_user': os.getenv('MYSQLUSER', 'NOT_SET'),
            'mysql_database': os.getenv('MYSQLDATABASE', 'NOT_SET'),
            'mysql_port': os.getenv('MYSQLPORT', 'NOT_SET'),
        },
        'external_config': {
            'mysql_public_host': os.getenv('MYSQL_PUBLIC_HOST', 'NOT_SET'),
            'mysql_public_port': os.getenv('MYSQL_PUBLIC_PORT', 'NOT_SET'),
        },
        'has_password': 'YES' if os.getenv('MYSQLPASSWORD') else 'NO'
    })

# Manual database initialization endpoint
@app.route('/init-db', methods = ['GET'])
def manual_init_db():
    try:
        print("=== Iniciando diagnóstico de base de datos ===")
        result = init_database()
        if result:
            return jsonify({'status': 'success', 'message': 'Database initialized successfully'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Database initialization failed - check logs for details'}), 500
    except Exception as e:
        print(f"Error en manual_init_db: {e}")
        return jsonify({'status': 'error', 'message': f'Error: {str(e)}'}), 500

# Test database connection endpoint
@app.route('/test-db', methods = ['GET'])
def test_db_connection():
    try:
        print("=== Probando conexión básica ===")
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1 as test")
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return jsonify({'status': 'success', 'message': f'Database connection successful. Test result: {result}'}), 200
    except Exception as e:
        print(f"Error en test de conexión: {e}")
        import traceback
        error_details = traceback.format_exc()
        return jsonify({
            'status': 'error', 
            'message': f'Database connection failed: {str(e)}',
            'error_type': type(e).__name__,
            'traceback': error_details
        }), 500

# Database connection test with retry
@app.route('/test-db-retry', methods = ['GET'])
def test_db_connection_retry():
    import time
    attempts = 3
    for attempt in range(attempts):
        try:
            print(f"Intento {attempt + 1} de {attempts}")
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            return jsonify({
                'status': 'success', 
                'message': f'Database connection successful on attempt {attempt + 1}',
                'result': result[0] if result else None
            })
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < attempts - 1:
                print(f"Waiting 2 seconds before retry...")
                time.sleep(2)
            else:
                return jsonify({
                    'status': 'error',
                    'message': f'Database connection failed after {attempts} attempts',
                    'error_type': type(e).__name__,
                    'last_error': str(e)
                }), 500

# route for create link and save in database
@app.route('/create', methods = ['POST'])
def create():
    try:
        # REMOVED: auto initialization - use /init-db endpoint first
        
        if request.method == 'POST':
            # get url
            url = request.form['url']
            
            # get database connection
            connection = get_db_connection()
            cursor = connection.cursor()
            
            # cicle for duplicated url
            while True:
                short_link = shortuuid.ShortUUID().random(length = 5)  # Reducido a 5 caracteres
                cursor.execute("SELECT * FROM links WHERE short_link = BINARY %s", (short_link,))
                
                if not cursor.fetchone():
                    break
            
            # check if url already exists
            cursor.execute("SELECT short_link FROM links WHERE url = BINARY %s", (url,))
            data = cursor.fetchone()
            if data:
                cursor.close()
                connection.close()
                return jsonify({'short_link': f"{endpoint}/{data[0]}"})
            
            # insert new link
            cursor.execute("INSERT INTO links (url, short_link) VALUES (%s, %s)", (url, short_link))
            connection.commit()
            cursor.close()
            connection.close()
            
            return jsonify({'short_link': f"{endpoint}/{short_link}"})
    except Exception as e:
        return jsonify({'error': f'Error creating short link: {str(e)}'}), 500

# route for redirect to original url
@app.route('/<short_link>')
def redirect_url(short_link):
    try:
        # get database connection
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT url FROM links WHERE short_link = BINARY %s", (short_link,))
        data = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if data:
            return redirect(data[0])
        else:
            return render_template('404.html'), 404
    except Exception as e:
        return render_template('404.html'), 404

# run app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)