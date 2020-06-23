from flask import Blueprint, jsonify, request
from __init__ import db
from flask_sqlalchemy import SQLAlchemy
from models import ApartamentoTable, PredioTable


bp_apartamento = Blueprint('apartamento', __name__)

@bp_apartamento.route('/apartamento/criar', methods=['POST'])
def create():
    
    idpredio = request.json['predio']

    predio = PredioTable.query.get(idpredio)


    new_apt = ApartamentoTable(predio)

    db.session.add(new_apt)
    db.session.commit()

    return jsonify('Tudo certo')

@bp_apartamento.route('/apartamento/alterar/<id>', methods=['PUT'])
def modify(id):

    apt = ApartamentoTable.query.get(id)

    idpredio = request.json['predio']

    predio = PredioTable.query.get(idpredio)

    apt.apartamento_idprd = predio.id

    db.session.commit()

    return jsonify('Tudo certo')

@bp_apartamento.route('/apartamento/mostrar', methods=['GET'])
def show_all():

    apts = ApartamentoTable.query.all()
    apartamentos = []

    cont = 0 

    for i in apts:
        apartamentos.append({"predio": apts[cont].apartamento_idprd, "apartamento": apts[cont].id})
    

    return jsonify(apartamentos)

@bp_apartamento.route('/apartamento/mostrar/<id>', methods=['GET'])
def show_by_id(id):
    
    apartamento = ApartamentoTable.query.get(id)

    apt = {
        "apartamento":apartamento.id,
        "predio":apartamento.apartamento_idprd
        }


    return jsonify(apt)

@bp_apartamento.route('/apartamento/deletar/<id>', methods=['DELETE'])
def delete_by_id(id):
    
    apartamento = ApartamentoTable.query.get(id)

    db.session.delete(apartamento)
    db.session.commit()

    return jsonify('Tudo certo')
