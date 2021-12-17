from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template

app = Flask(__name__)
stores = {
    'first_store': {'item1': 10, 'item2': 20},
}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/store')
def get_stores():
    return jsonify(stores)


@app.route('/store/<string:name>')
def get_store(name):
    if name in stores:
        return jsonify({name: stores[name]})
    return jsonify({'message': 'store not found'})


@app.route('/store/<string:name>', methods=['POST'])
def create_store():
    request_data = request.get_json()
    stores[request_data] = {}
    return jsonify({request_data: {}})


@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    stores[name].extend(request_data)
    return jsonify({name: request_data})


@app.route('/store/<string:name>/item')
def get_items_from_store(name):
    if name in stores:
        return jsonify(stores[name])
    return jsonify({'message': 'store not found'})


app.run()
