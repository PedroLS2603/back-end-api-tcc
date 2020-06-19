from flask import Flask, Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import EntradaTable, PessoaTable
from serializer import EntradaSchema
from __init__ import db
import datetime



bp_entrada = Blueprint('entrada', __name__)

@bp_entrada.route('/entrada/criar', methods=['POST'])
def create():

    ap = request.json['apartamento']
    prd = request.json['predio']
    cpf = request.json ['cpf']

    pessoa = PessoaTable.query.filter_by(cpf=cpf).first()

    pessoa = pessoa.id

    datahora = datetime.datetime.now()


    new_entrada = EntradaTable(ap, prd, pessoa, datahora)

    db.session.add(new_entrada)
    db.session.commit()

    return jsonify('Tudo certo')

@bp_entrada.route('/entrada/mostrar', methods=['GET'])
def show_all():

    es = EntradaSchema(many=True)

    entrds = EntradaTable.query.all()

    entradas = []
    cont = 0
    for i in entrds:
        entradas.append({"idacesso":entrds[cont].id, "apartamento":entrds[cont].entrada_idapt, "predio": entrds[cont].entrada_idprd, "pessoa": entrds[cont].entrada_idpes, "datahora": entrds[cont].datahora})
        
        datahora = entradas[cont]["datahora"]
        datahora = datahora.strftime('%d/%m/%Y %H:%M')
        entradas[cont]["datahora"] = datahora
        
        pessoa = PessoaTable.query.get(entradas[cont]['pessoa'])
        entradas[cont]["pessoa"] = pessoa.nome
        
        
        
        cont = cont+1


    return jsonify(entradas) 

@bp_entrada.route('/entrada/mostrar/<id>', methods=['GET'])
def show_by_id(id):

    entrd = EntradaTable.query.get(id)

    entrada = {"idacesso": entrd.id,
               "apartamento": entrd.entrada_idapt,
               "predio": entrd.entrada_idprd,
               "pessoa": entrd.entrada_idpes,
               "datahora": entrd.datahora
     }
    
    pessoa = PessoaTable.query.get(entrada['pessoa'])
    entrada['pessoa'] = pessoa.nome

    entrada['datahora'] = entrada['datahora'].strftime('%d/%m/%Y %H:%M')


    return jsonify(entrada)

@bp_entrada.route('/entrada/deletar/<id>', methods=['DELETE'])
def delete(id):

    entrada = EntradaTable.query.get(id)

    db.session.delete(entrada)
    db.session.commit()

    return jsonify('Tudo certo')