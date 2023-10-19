from flask import Blueprint, jsonify
from models.citas_model import citasModel

main=Blueprint('citas_blueprint',__name__)

@main.route('/')
def get_citas():
    try:
        citas = citasModel.get_citas()
        return jsonify(citas)
    except Exception as e:
        return jsonify({'message': str(e)}),500