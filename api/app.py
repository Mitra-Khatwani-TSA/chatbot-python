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

        return jsonify({'msg': botres}), 201
    else:
        return jsonify({"msg": "Hello World!"})
    
if __name__ == '__main__':
    #app.run(debug=True, port=61154)
    app.run(debug=True, host='0.0.0.0')