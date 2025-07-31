from  flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysql_connector import MySQL
import shortuuid

# init app
app = Flask(__name__)

# endpoint
endpoint = 'http://opti.url'

# connect mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'P@u102018.180905'
app.config['MYSQL_DATABASE'] = 'db_opti_url'

# init mysql
mysql = MySQL(app)

# init route
@app.route('/', methods = ['GET'])
def inicio():
    try:
        return jsonify(response = 'inicio')
    except: 
        return jsonify(response = 'error'), 500

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
                cursor.execute("SELECT * FROM links WHERE short_link = BINARY %s", (short_link))
                
                if not cursor.fetchone():
                    break
            
            cursor.execute("INSERT INTO links (url, short_link) VALUES (%s, %s)", (url, short_link))
            
            mysql.connection.commit()
            cursor.close()
            
            new_url = endpoint + '/' + short_link
            return jsonify(response = new_url)
    except: 
        return jsonify(response = 'error'), 500

# run app
if __name__ == '__main__':
    app.run(port = 80, debug = True)
