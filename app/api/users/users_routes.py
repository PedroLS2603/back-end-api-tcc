from flask import Flask, Blueprint, request, jsonify 
from flask_sqlalchemy import SQLAlchemy
from models import PessoaTable, TipoPessoaTable
from __init__ import db
from serializer import PessoaSchema

bp_users = Blueprint('pessoa', __name__)

@bp_users.route('/user/mostrar', methods=['GET'])
def show():

    users = PessoaTable.query.all()
    output=[]
    cont=0

    try:
        for u in users:
            tipopessoa = TipoPessoaTable.query.get(users[cont].tp)
            tipopessoa = tipopessoa.descricao
            output.append({"id": users[cont].id,"nome":users[cont].nome, "cpf": users[cont].cpf, "rg": users[cont].rg, "tipo": tipopessoa})
            cont = cont+1

        return jsonify(output)

    except:
        return jsonify({"message":'Sem registros.'})

@bp_users.route('/user/mostrar/<id>', methods=['GET'])
def show_by_id(id):
    user = PessoaTable.query.get(id)

    try:
        tipopessoa = TipoPessoaTable.query.get(user.tp)

        output = {"id":user.id,"nome": user.nome, "cpf": user.cpf, "rg": user.rg, "tipo": tipopessoa.descricao}
        
        
        return jsonify(output)
    except:
        return jsonify({"message":'Sem registros.'})

@bp_users.route('/user/criar', methods=['POST'])
def create():
    nome = request.json['nome']
    cpf = request.json['cpf']
    rg = request.json['rg']
    foto = request.json['foto']
    tipopessoa = request.json['tipopessoa']

    try:
        tp = TipoPessoaTable.query.filter_by(descricao=tipopessoa).first()

        tipopessoa = tp.id

        new_user = PessoaTable(nome,cpf,rg,foto,tipopessoa)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message":'Pessoa criada com sucesso!'})

    except:
        return jsonify({"message":'Erro ao criar pessoa. Verifique as informações inseridas'})

@bp_users.route('/user/alterar/<id>', methods=['PUT'])
def update(id):

    user = PessoaTable.query.get(id)

    nome = request.json['nome']
    cpf = request.json['cpf']
    rg = request.json['rg']
    ft = request.json['foto']
    tp = request.json['tipopessoa']
        
    try:
        if nome != "":
            user.nome = nome
        if cpf != "":
            user.cpf = cpf
        if rg != "":
            user.rg = rg
        if ft != "":
            user.ft = ft
        if tp != "":
            tipopessoa = TipoPessoaTable.query.all()
            if tp in tipopessoa:
                tp = tipopessoa.id

            user.tp = tp

        db.session.commit()

        return jsonify({"message":'Usuário alterado com sucesso!'})
    
    except:
        return jsonify({"message":'Erro ao alterar usuário. Verifique as informações inseridas.'})

@bp_users.route('/user/deletar/<id>', methods=['DELETE'])
def delete(id):
    try:
        user = PessoaTable.query.get(id)

        db.session.delete(user)
        db.session.commit()

        return jsonify({"message":'Usuário deletado com sucesso!'})
        
    except:
        return jsonify({"message":'Erro ao deletar usuário.'})    
