from flask import Blueprint, jsonify, request
from __init__ import db
from flask_sqlalchemy import SQLAlchemy
from serializer import PredioSchema
from models import PredioTable

bp_predio = Blueprint('predio', __name__)

@bp_predio.route('/predio/criar', methods=['POST'])
def create():

    evento = request.json['evento']

    try:
        new_predio = PredioTable(evento)


        db.session.add(new_predio)
        db.session.commit()

        return jsonify('Prédio criado com sucesso!')

    except:
        return jsonify('Erro ao criar prédio. Verifique as informações inseridas.')

@bp_predio.route('/predio/alterar/<id>', methods=['PUT'])
def modify(id):

    predio = PredioTable.query.get(id)
    evt = request.json ['evento']

    try:
        if evt !='':
            predio.evento = evt

        db.session.commit()

        return jsonify('Informações do prédio alterada com sucesso!')

    except:
        return jsonify('Erro ao alterar informações do prédio. Verifique as informações inseridas.')

@bp_predio.route('/predio/mostrar', methods=['GET'])
def show_all():
    prds = PredioTable.query.all()
    output = []

    cont = 0 

    try:
        for i in prds:
            output.append({"predio":prds[cont].id, "evento": prds[cont].evento})
            cont = cont+1


        return jsonify(output)
    except:
        return jsonify('Sem registros.')

@bp_predio.route('/predio/mostrar/<id>', methods=['GET'])
def show_by_id(id):
    predio = PredioTable.query.get(id)

    try:
        output = {
            "predio":predio.id,
            "evento":predio.evento
            }


        return jsonify(output)

    except:
        return jsonify('Sem registro.')

@bp_predio.route('/predio/deletar/<id>', methods=['DELETE'])
def delete_by_id(id):

    try:
        predio = PredioTable.query.get(id)

        db.session.delete(predio)
        db.session.commit()

        return jsonify('Prédio deletado com sucesso!')

    except:
        return jsonify('Erro ao deletar prédio.')
