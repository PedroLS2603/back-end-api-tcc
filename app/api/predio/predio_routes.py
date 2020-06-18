from flask import Blueprint, jsonify, request
from __init__ import db
from flask_sqlalchemy import SQLAlchemy
from serializer import PredioSchema
from models import PredioTable

bp_predio = Blueprint('predio', __name__)

@bp_predio.route('/predio/criar', methods=['POST'])
def create():

    evento = request.json['evento']

    new_predio = PredioTable(evento)


    db.session.add(new_predio)
    db.session.commit()

    return jsonify('Tudo certo')

@bp_predio.route('/predio/alterar/<id>', methods=['PUT'])
def modify(id):

    predio = PredioTable.query.get(id)

    evt = request.json ['evento']

    predio.evento = evt

    db.session.commit()

    return jsonify('Tudo certo')

@bp_predio.route('/predio/mostrar', methods=['GET'])
def show_all():
    ps = PredioSchema(many=True)

    prds = PredioTable.query.all()
    predios = []

    cont = 0 

    for i in prds:
        predios.append({"predio":prds[cont].id, "evento": prds[cont].evento})
        cont = cont+1


    return jsonify(predios)

@bp_predio.route('/predio/mostrar/<id>', methods=['GET'])
def show_by_id(id):
    ps = PredioSchema()
    
    predio = PredioTable.query.get(id)

    prd = {
        "predio":predio.id,
        "evento":predio.evento
        }


    return jsonify(prd)

@bp_predio.route('/predio/deletar/<id>', methods=['DELETE'])
def delete_by_id(id):

    predio = PredioTable.query.get(id)

    db.session.delete(predio)
    db.session.commit()

    return jsonify('Tudo certo ')



