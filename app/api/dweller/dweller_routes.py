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

    tp = TipoPessoaTable.query.filter_by(descricao='morador').first()

    pessoa = PessoaTable.query.filter_by(cpf=cpf, tp=tp.id).first()

    new_morador = MoradorTable(ap, prd, pessoa.id)

    db.session.add(new_morador)
    db.session.commit()

    return jsonify({"message":'Morador registrado com sucesso!'})
    


@bp_morador.route('/morador/mostrar', methods=['GET'])
def show_all():

    tipopessoa = TipoPessoaTable.query.filter_by(descricao='morador').first()

    moradores = PessoaTable.query.filter_by(tp=tipopessoa.id).all()

    mrds = MoradorTable.query.all()

    try:    
        cont = 0 
        output = []
        
        for i in mrds:
            pessoa = PessoaTable.query.filter_by(id=mrds[cont].morador_idpes).first()
            output.append({"id": mrds[cont].id,"nome": pessoa.nome, "cpf":pessoa.cpf, "rg":pessoa.rg, "foto":pessoa.foto, "apartamento":mrds[cont].morador_idapt, "predio": mrds[cont].morador_idprd}) 
            cont = cont+1

        return jsonify(output)
    
    except:
        return jsonify({"message":'Sem registros'})

@bp_morador.route('/morador/mostrar/<id>', methods=['GET'])
def show_by_id(id):
    
    morador = MoradorTable.query.get(id)

    try:
        mrd = PessoaTable.query.get(morador.morador_idpes)


        result = {"id":morador.id, "nome": mrd.nome, "cpf": mrd.cpf, "rg": mrd.rg, "foto": mrd.foto, "predio": morador.morador_idprd, "apartamento": morador.morador_idapt }

        return jsonify(result)

    except:
        return jsonify({"message":'Sem registros. Verifique as informações inseridas.'})

@bp_morador.route('/morador/alterar/<id>', methods=['PUT'])
def modify(id):

    prd = request.json['predio']
    apt = request.json['apartamento']

    morador = MoradorTable.query.get(id)

    try:
        if apt != '':
            morador.morador_idapt = apt
        if prd != '':
            morador.morador_idprd = prd

        db.session.commit()

        return jsonify({"message":'Informações do morador alteradas com sucesso!', "status":200})

    except:
        return jsonify({"message":'Erro ao alterar as informações do morador. Verifique as informações inseridas.', "status":400, "apartamento":apt, "predio":prd})

@bp_morador.route('/morador/deletar/<id>', methods=['DELETE'])
def delete(id):
    
    morador = MoradorTable.query.get(id)

    try:
        db.session.delete(morador)
        db.session.commit()

        return jsonify({"message":'Morador deletado com sucesso!',"status": 200, "ID": morador.id})
    except:
        return jsonify({"message":'Erro ao deletar morador.', "status": 400, "ID": morador.id})