import os
from flask import Flask, jsonify

# init app
app = Flask(__name__)

# Simple health check
@app.route('/', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': 'Simple Flask app is running'})

@app.route('/test', methods=['GET'])
def test():
    return jsonify({
        'mysqlhost': os.getenv('MYSQLHOST', 'not set'),
        'mysqluser': os.getenv('MYSQLUSER', 'not set'),
        'mysqldatabase': os.getenv('MYSQLDATABASE', 'not set'),
        'mysqlport': os.getenv('MYSQLPORT', 'not set')
    })

# run app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
