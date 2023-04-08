from flask import Flask, jsonify, request
from flask_cors import CORS

from main import chat

app = Flask(__name__)

CORS(app)

@app.route("/api", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        some_json = request.get_json()

        botres = chat(some_json["msg"])
        response = jsonify({'msg': botres})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 201
    else:
        response = jsonify({'msg': 'hello world'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    
if __name__ == '__main__':
    #app.run(debug=True, port=61154)
    app.run(debug=True, host='0.0.0.0')