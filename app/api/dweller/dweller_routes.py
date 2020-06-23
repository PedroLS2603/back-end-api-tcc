from flask import Blueprint, jsonify, request 
from flask_sqlalchemy import SQLAlchemy
from __init__ import db
from models import PessoaTable, MoradorTable, TipoPessoaTable
from serializer import PessoaSchema, MoradorSchema

bp_morador = Blueprint('morador', __name__)

@bp_morador.route('/morador/criar', methods=['POST'])
def create():
    ap = request.json['apartamento']
    prd = request.json['predio']
    cpf = request.json['cpf']

    pessoa = PessoaTable.query.filter_by(cpf=cpf).first()

    pessoa = pessoa.id

    new_morador = MoradorTable(ap, prd, pessoa)

    db.session.add(new_morador)
    db.session.commit()

    return jsonify('Tudo certo')
    
@bp_morador.route('/morador/mostrar', methods=['GET'])
def show_all():
    tipopessoa = TipoPessoaTable.query.filter_by(descricao='morador').first()
    tipopessoa = tipopessoa.id

    moradores = PessoaTable.query.filter_by(tp=tipopessoa).all()

    mrds = MoradorTable.query.all()

    cont = 0 
    result = []

    for i in moradores:
        result.append({"nome":moradores[cont].nome, "cpf":moradores[cont].cpf, "rg":moradores[cont].rg, "foto":moradores[cont].foto, "apartamento":mrds[cont].morador_idapt, "predio": mrds[cont].morador_idprd}) 
        cont = cont+1

    return jsonify(result)

@bp_morador.route('/morador/mostrar/<id>', methods=['GET'])
def show_by_id(id):
    
    morador = MoradorTable.query.get(id)
    idpes = morador.morador_idpes
    mrd = PessoaTable.query.get(idpes)


    result = {"nome": mrd.nome, "cpf": mrd.cpf, "rg": mrd.rg, "foto": mrd.foto, "predio": morador.morador_idprd, "apartamento": morador.morador_idapt }

    return jsonify(result)

@bp_morador.route('/morador/alterar/<id>', methods=['PUT'])
def modify(id):

    prd = request.json['predio']
    apt = request.json['apartamento']

    morador = MoradorTable.query.get(id)

    morador.morador_idapt = apt
    morador.morador_idprd = prd

    db.session.commit()

    return jsonify('Tudo certo')

@bp_morador.route('/morador/deletar/<id>', methods=['DELETE'])
def delete(id):
    
    morador = MoradorTable.query.get(id)

    db.session.delete(morador)
    db.session.commit()

    return jsonify('Tudo certo')