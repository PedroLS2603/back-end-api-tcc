from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from __init__ import db
from models import EncomendaTable, MoradorTable, PessoaTable
from serializer import EncomendaSchema
import datetime

bp_encomenda = Blueprint("encomenda", __name__)

@bp_encomenda.route('/mail/criar', methods=['POST'])
def create():
    apartamento = request.json['apartamento']
    predio = request.json['predio']

    try:
        morador = MoradorTable.query.filter_by(morador_idapt=apartamento, morador_idprd=predio).first()
        morador = morador.morador_idpes

        datahora = datetime.datetime.now()

        destinatario = EncomendaTable(morador, datahora)

        db.session.add(destinatario)
        db.session.commit()

        return jsonify("Registro de encomenda criado com sucesso!")
    
    except:
        return jsonify("Erro ao criar registro de encomenda")

@bp_encomenda.route('/mail/mostrar', methods=['GET'])
def show_all():
    encomendas = EncomendaTable.query.all()

    output = []
    cont = 0

    try:
        for e in encomendas:
            pessoa = PessoaTable.query.get(encomendas[cont].encomenda_idpes)

            datahora = encomendas[cont].datahora
            datahora = datahora.strftime('%d/%m/%Y %H:%M')

            output.append({"id":encomendas[cont].id, "destinatario":pessoa.nome, "datahora": datahora })
            cont = cont+1

        return jsonify(output)

    except:
        return jsonify({"message":'Sem registros.'})

@bp_encomenda.route('/mail/mostrar/<id>', methods=['GET'])
def show_by_id(id):
    encomenda = EncomendaTable.query.get(id)
    
    try:
        datahora = encomenda.datahora
        datahora = datahora.strftime('%d/%m/%Y %H:%M')
        
        pessoa = PessoaTable.query.get(encomenda.encomenda_idpes)
        pessoa = pessoa.nome

        output = {"id":encomenda.id, "destinatario": pessoa, "datahora":datahora }


        return jsonify(output)

    except:
        return jsonify({"message":'Sem registro.'})

@bp_encomenda.route('/mail/alterar/<id>', methods=['PUT'])
def modify(id):
    apartamento = request.json['apartamento']
    predio = request.json['predio']

    encomenda = EncomendaTable.query.get(id)

    try:
        if apartamento and predio != "":
            pessoa = MoradorTable.query.filter_by(morador_idapt=apartamento, morador_idprd=predio).first()
        
            encomenda.encomenda_idpes = pessoa.morador_idpes
            encomenda.datahora = datetime.datetime.now()

        db.session.commit()

        return jsonify({"message":'Registro de encomenda alterado com sucesso!'})
    
    except:
        return jsonify({"message":'Erro ao alterar registro de encomenda, verifique as informações inseridas.'})

@bp_encomenda.route('/mail/deletar/<id>', methods=['DELETE'])
def delete(id):
    try:
        encomenda = EncomendaTable.query.get(id)

        db.session.delete(encomenda)
        db.session.commit()

        return jsonify({"message":'Registro de encomenda deletado com sucesso!'})
    
    except:
        return jsonify({"message":'Erro ao deletar registro de encomenda.'})
