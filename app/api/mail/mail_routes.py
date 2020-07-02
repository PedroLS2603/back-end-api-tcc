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

    morador = MoradorTable.query.filter_by(morador_idapt=apartamento, morador_idprd=predio).first()
    morador = morador.morador_idpes

    datahora = datetime.datetime.now()

    destinatario = EncomendaTable(morador, datahora)

    db.session.add(destinatario)
    db.session.commit()

    return jsonify("Tudo certo")

@bp_encomenda.route('/mail/mostrar', methods=['GET'])
def show_all():
    encomendas = EncomendaTable.query.all()


    output = []
    cont = 0 
    for e in encomendas:
        pessoa = PessoaTable.query.get(encomendas[cont].encomenda_idpes)
        pessoa= pessoa.nome 

        datahora = encomendas[cont].datahora
        datahora = datahora.strftime('%d/%m/%Y %H:%M')

        output.append({"ID":encomendas[cont].id, "Destinatário":pessoa, "Entrega em": datahora })
        cont = cont+1

    return jsonify({"Encomendas":output})

@bp_encomenda.route('/mail/mostrar/<id>', methods=['GET'])
def show_by_id(id):
    encomenda = EncomendaTable.query.get(id)
    
    datahora = encomenda.datahora
    datahora = datahora.strftime('%d/%m/%Y %H:%M')
    
    pessoa = PessoaTable.query.get(encomenda.encomenda_idpes)
    pessoa = pessoa.nome

    output = {"ID":encomenda.id, "Destinatário": pessoa, "Entrega em":datahora }


    return jsonify(output)

@bp_encomenda.route('/mail/alterar/<id>', methods=['PUT'])
def modify(id):
    apartamento = request.json['apartamento']
    predio = request.json['predio']

    encomenda = EncomendaTable.query.get(id)

    if apartamento and predio != "":
        pessoa = MoradorTable.query.filter_by(morador_idapt=apartamento, morador_idprd=predio).first()
    
        encomenda.encomenda_idpes = pessoa.morador_idpes
        encomenda.datahora = datetime.datetime.now()

    db.session.commit()

    return jsonify('Tudo certo')

@bp_encomenda.route('/mail/deletar/<id>', methods=['DELETE'])
def delete(id):
    encomenda = EncomendaTable.query.get(id)

    db.session.delete(encomenda)
    db.session.commit()

    return jsonify('Tudo certo') 