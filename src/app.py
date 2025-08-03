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
    'autocommit': True
}

# create connection pool
def get_db_connection():
    return mysql.connector.connect(**mysql_config)

# set secret key - usar variable de entorno
app.secret_key = os.getenv('SECRET_KEY', 'C14v3S3cr3t4')

# init route
@app.route('/', methods = ['GET'])
def inicio():
    try:
        return render_template('index.html'), 200
    except: 
        return render_template('404.html'), 404

# route for create link and save in database
@app.route('/create', methods = ['POST'])
def create():
    try:
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