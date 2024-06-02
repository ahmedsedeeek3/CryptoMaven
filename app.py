from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def hello_world():
    return jsonify({"Hello": "World"})

@app.route("/items/<int:item_id>", methods=['GET'])
def read_item(item_id):
    q = request.args.get('q', None)
    return jsonify({"item_id": item_id, "q": q})

@app.route("/items/<int:item_id>", methods=['PUT'])
def update_item(item_id):
    item_data = request.json
    name = item_data.get('name')
    price = item_data.get('price')
    is_offer = item_data.get('is_offer', None)
    return jsonify({"item_name": name, "item_id": item_id, "item_price": price, "is_offer": is_offer})

@app.route("/items", methods=['POST'])
def create_item():
    item_data = request.json
    name = item_data.get('name')
    price = item_data.get('price')
    is_offer = item_data.get('is_offer', None)
    return jsonify({"item_name": name, "item_price": price, "is_offer": is_offer})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
