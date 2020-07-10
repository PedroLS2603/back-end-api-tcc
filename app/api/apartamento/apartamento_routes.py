from flask import Blueprint, jsonify, request
from __init__ import db
from flask_sqlalchemy import SQLAlchemy
from models import ApartamentoTable, PredioTable


bp_apartamento = Blueprint('apartamento', __name__)

@bp_apartamento.route('/apartamento/criar', methods=['POST'])
def create():
    
    idpredio = request.json['predio']

    try:    
        predio = PredioTable.query.get(idpredio)


        new_apt = ApartamentoTable(predio)

        db.session.add(new_apt)
        db.session.commit()

        return jsonify({"message":'Apartamento registrado com sucesso!'})
    
    except:
        return jsonify({"message":'Ocorreu um erro ao registrar o apartamento, verifique as informações inseridas.'})

@bp_apartamento.route('/apartamento/alterar/<id>', methods=['PUT'])
def modify(id):

    idpredio = request.json['predio']

    try:
        apt = ApartamentoTable.query.get(id)
        predio = PredioTable.query.get(idpredio)

        if idpredio !='':
            apt.apartamento_idprd = predio.id

        db.session.commit()

        return jsonify({"message":'Informações do apartamento alterada com sucesso!'})

    except:
        return jsonify({"message":'Não foi possível alterar as informações do apartamento, verifique as informações inseridas.'})

@bp_apartamento.route('/apartamento/mostrar', methods=['GET'])
def show_all():

    apts = ApartamentoTable.query.all()
    apartamentos = []

    cont = 0 

    try:
        for i in apts:
            apartamentos.append({"predio": apts[cont].apartamento_idprd, "apartamento": apts[cont].id})
            cont = cont+1

        return jsonify(apartamentos)

    except:
        return jsonify({"message":'Sem registros. Favor verificar as informações inseridas'})

@bp_apartamento.route('/apartamento/mostrar/<id>', methods=['GET'])
def show_by_id(id):
    
    apartamento = ApartamentoTable.query.get(id)

    try:
        apt = {
            "apartamento":apartamento.id,
            "predio":apartamento.apartamento_idprd
            }


        return jsonify(apt)

    except:
        return jsonify({"message":'Sem registros. Favor verificar as informações inseridas'})

@bp_apartamento.route('/apartamento/deletar/<id>', methods=['DELETE'])
def delete_by_id(id):
    
    apartamento = ApartamentoTable.query.get(id)

    try:
        db.session.delete(apartamento)
        db.session.commit()

        return jsonify({"message":'Apartamento deletado com sucesso!'})
    except:
        return jsonify({"message":'Não foi possível deletar o apartamento.'})
