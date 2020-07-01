from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from models import ProblemaTable, ApartamentoTable, PredioTable
from serializer import ProblemaSchema
from __init__ import db

bp_problema = Blueprint('problema', __name__)

@bp_problema.route('/problema/criar', methods=['POST'])
def create():

    ap = request.json['apartamento']
    prd = request.json['predio']
    dscr = request.json['descricao']

    ap = ApartamentoTable.query.get(ap)
    prd = PredioTable.query.get(prd)

    ap = ap.id
    prd = prd.id

    new_prob = ProblemaTable(dscr, prd, ap )

    db.session.add(new_prob)
    db.session.commit()

    return jsonify('Tudo certo')

@bp_problema.route('/problema/mostrar', methods=['GET'])
def show_all():
    problemas = ProblemaTable.query.all()

    output = []

    cont = 0

    for problema in problemas:
        output.append({'id':problemas[cont].id, 'predio':problemas[cont].problema_idprd, 'apartamento': problemas[cont].problema_idapt, 'descricao': problemas[cont].descricao})
        cont = cont+1
    return jsonify(output)

@bp_problema.route('/problema/mostrar/<id>', methods=['GET'])
def show_by_id(id):
    problema = ProblemaTable.query.get(id)

    output = {'id':problema.id, 'predio':problema.problema_idprd, 'apartamento': problema.problema_idapt, 'descricao': problema.descricao}

    return jsonify(output)

@bp_problema.route('/problema/alterar/<id>', methods=['PUT'])
def modify(id):
    problema = ProblemaTable.query.get(id)

    problema.descricao = request.json['descricao']
    problema.problema_idapt = request.json['apartamento']
    problema.problema_idprd = request.json['predio']

    db.session.commit()

    return jsonify('Tudo certo')

@bp_problema.route('/problema/deletar/<id>', methods=['DELETE'])
def delete(id):
    problema = ProblemaTable.query.get(id)

    db.session.delete(problema)
    db.session.commit()

    return jsonify('Tudo certo')
