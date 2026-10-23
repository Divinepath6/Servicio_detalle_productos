from flask import Flask, jsonify, request
from productos import obtener_producto_db


app = Flask(__name__)

@app.route('/api/producto/<int:id>', methods=['GET'])
def obtener_producto(id):
    if id == 0:
        return jsonify({
            "error": "Sin id"
        }), 400
    else:
        return obtener_producto_db(id)


if __name__ == '__main__':
    # Inicia el servidor de desarrollo en modo debug
    app.run(debug=True)