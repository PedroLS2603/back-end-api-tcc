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

    try:
        new_prob = ProblemaTable(dscr, prd.id, ap.id )

        db.session.add(new_prob)
        db.session.commit()

        return jsonify('Problema registrado com sucesso!')

    except:
        return jsonify('Erro ao registrar problema. Verifique as informações inseridas')

@bp_problema.route('/problema/mostrar', methods=['GET'])
def show_all():
    problemas = ProblemaTable.query.all()

    output = []

    cont = 0

    try:
        for problema in problemas:
            output.append({'id':problemas[cont].id, 'predio':problemas[cont].problema_idprd, 'apartamento': problemas[cont].problema_idapt, 'descricao': problemas[cont].descricao})
            cont = cont+1
            
        return jsonify(output)

    except:
        return jsonify('Sem registros.')

@bp_problema.route('/problema/mostrar/<id>', methods=['GET'])
def show_by_id(id):
    problema = ProblemaTable.query.get(id)

    try:
        output = {'id':problema.id, 'predio':problema.problema_idprd, 'apartamento': problema.problema_idapt, 'descricao': problema.descricao}

        return jsonify(output)

    except:
        return jsonify('Sem registro.')

@bp_problema.route('/problema/alterar/<id>', methods=['PUT'])
def modify(id):
    problema = ProblemaTable.query.get(id)

    dscr = request.json['descricao']
    ap = request.json['apartamento']
    prd = request.json['predio']

    try:
        if dscr !='':
            problema.descricao = dscr
        if ap !='':
            problema.problema_idapt = ap
        if prd !='':
            problema.problema_idprd = prd

        db.session.commit()

        return jsonify('Informações sobre o problema alteradas com sucesso!')

    except:
        return jsonify('Erro ao alterar informações sobre o problema. Verifique as informações inseridas.')

@bp_problema.route('/problema/deletar/<id>', methods=['DELETE'])
def delete(id):
    try:
        problema = ProblemaTable.query.get(id)

        db.session.delete(problema)
        db.session.commit()

        return jsonify('Problema deletado com sucesso!')
    
    except:
        return jsonify('Erro ao deletar problema.')
