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

# set secret key
app.secret_key = 'C14v3S3cr3t4'

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
                flash(endpoint + '/' + data[0])
                return redirect(url_for('inicio')), 302
            
            cursor.execute("INSERT INTO LINKS (URL, SHORT_LINK) VALUES (%s, %s)", (url, short_link))
            
            mysql.connection.commit()
            cursor.close()
            
            new_url = endpoint + '/' + short_link
            flash(new_url)
            return redirect(url_for('inicio')), 302
    except: 
        return render_template('404.html'), 404

# route to redirect to database
@app.route('/<id>')
def getUrl (id):
    try:
        cursor = mysql.connection.cursor()
        
        # search in database url direction
        cursor.execute("SELECT URL FROM LINKS WHERE SHORT_LINK = BINARY %s", (id,))

        # save in a variable and close connection
        data = cursor.fetchone()
        cursor.close()

        return render_template('ads.html', url=data[0]), 200

    except:
        return render_template('404.html'), 404

# run app
if __name__ == '__main__':
    app.run(port = 80, debug = True)
