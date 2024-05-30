from flask import Flask, request, jsonify
from flask_cors import CORS
from click_tool import fgo
app = Flask(__name__)
CORS(app)
a = fgo()
@app.route('/click_tool/getdata', methods=['GET'])

def get_data():
    return jsonify(a.d)

@app.route('/click_tool/update', methods=['POST'])

def update_data():
    updated_data = request.json
    a.update_d(updated_data)
    print(a.d)
    return jsonify({"message": "數據更新成功"})

if __name__ == '__main__':
    app.run(debug=False)