import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import mysql.connector
from mysql.connector import pooling
import shortuuid

# init app
app = Flask(__name__)

# endpoint - usar variable de entorno en producción
endpoint = os.getenv('APP_URL', 'http://localhost')

# mysql connection config
mysql_config = {
    'host': os.getenv('MYSQLHOST', 'localhost'),
    'user': os.getenv('MYSQLUSER', 'root'),
    'password': os.getenv('MYSQLPASSWORD', 'P@u102018.180905'),
    'database': os.getenv('MYSQLDATABASE', 'railway'),
    'port': int(os.getenv('MYSQLPORT', '3306')),
    'charset': 'utf8mb4',
    'autocommit': True,
    'connection_timeout': 10,
    'use_pure': True
}

# create connection pool
def get_db_connection():
    try:
        return mysql.connector.connect(**mysql_config)
    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
        raise

# Función para inicializar la base de datos
def init_database():
    try:
        print("Intentando inicializar base de datos...")
        print(f"Conectando a: {mysql_config['host']}:{mysql_config['port']}")
        print(f"Usuario: {mysql_config['user']}")
        print(f"Base de datos: {mysql_config['database']}")
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Crear la tabla LINKS si no existe
        create_table_query = """
        CREATE TABLE IF NOT EXISTS LINKS (
            id INT AUTO_INCREMENT PRIMARY KEY,
            URL TEXT NOT NULL,
            SHORT_LINK VARCHAR(10) NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
        connection.close()
        print("Tabla LINKS inicializada correctamente")
        return True
        
    except Exception as e:
        print(f"Error inicializando base de datos: {e}")
        print(f"Tipo de error: {type(e).__name__}")
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
        'mysql_host': os.getenv('MYSQLHOST', 'NOT_SET'),
        'mysql_user': os.getenv('MYSQLUSER', 'NOT_SET'),
        'mysql_database': os.getenv('MYSQLDATABASE', 'NOT_SET'),
        'mysql_port': os.getenv('MYSQLPORT', 'NOT_SET'),
        'has_password': 'YES' if os.getenv('MYSQLPASSWORD') else 'NO'
    })

# Manual database initialization endpoint
@app.route('/init-db', methods = ['GET'])
def manual_init_db():
    try:
        if init_database():
            return jsonify({'status': 'success', 'message': 'Database initialized successfully'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Database initialization failed'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error: {str(e)}'}), 500

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
                short_link = shortuuid.ShortUUID().random(length = 7)
                cursor.execute("SELECT * FROM LINKS WHERE SHORT_LINK = BINARY %s", (short_link,))
                
                if not cursor.fetchone():
                    break
            
            # check if url already exists
            cursor.execute("SELECT SHORT_LINK FROM LINKS WHERE URL = BINARY %s", (url,))
            data = cursor.fetchone()
            if data:
                cursor.close()
                connection.close()
                return jsonify({'short_link': f"{endpoint}/{data[0]}"})
            
            # insert new link
            cursor.execute("INSERT INTO LINKS (URL, SHORT_LINK) VALUES (%s, %s)", (url, short_link))
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
        cursor.execute("SELECT URL FROM LINKS WHERE SHORT_LINK = BINARY %s", (short_link,))
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