import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysql_connector import MySQL
import shortuuid

# init app
app = Flask(__name__)

# endpoint - usar variable de entorno en producción
endpoint = os.getenv('APP_URL', 'http://localhost')

# connect mysql - usar variables de entorno
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'P@u102018.180905')
app.config['MYSQL_DATABASE'] = os.getenv('MYSQL_DATABASE', 'db_opti_url')

# init mysql
mysql = MySQL(app)

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
            cursor = mysql.connection.cursor()
            
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
                return jsonify({'short_link': f"{endpoint}/{data[0]}"})
            
            # insert new link
            cursor.execute("INSERT INTO LINKS (URL, SHORT_LINK) VALUES (%s, %s)", (url, short_link))
            mysql.connection.commit()
            cursor.close()
            
            return jsonify({'short_link': f"{endpoint}/{short_link}"})
    except:
        return jsonify({'error': 'Error creating short link'}), 500

# route for redirect to original url
@app.route('/<short_link>')
def redirect_url(short_link):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT URL FROM LINKS WHERE SHORT_LINK = BINARY %s", (short_link,))
        data = cursor.fetchone()
        cursor.close()
        
        if data:
            return redirect(data[0])
        else:
            return render_template('404.html'), 404
    except:
        return render_template('404.html'), 404

# run app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)