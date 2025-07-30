from  flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysql_connector import MySQL
import shortuuid

# init app
app = Flask(__name__)

# endpoint
endpoint = 'http://opti.url'

# run app
if __name__ == '__main__':
    app.run(port = 80, debug = True)
