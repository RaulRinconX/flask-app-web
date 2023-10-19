from flask import Blueprint, jsonify
from models.historias_model import historiaModel

main=Blueprint('historia_blueprint',__name__)

@main.route('/')
def get_historias():
    try:
        historias = historiaModel.get_historias()
        return jsonify(historias)
    except Exception as e:
        return jsonify({'message': str(e)}),500
    