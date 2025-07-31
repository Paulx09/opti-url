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

# run app
if __name__ == '__main__':
    app.run(port = 80, debug = True)
