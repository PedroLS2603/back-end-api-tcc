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

    for u in users:
        tipopessoa = TipoPessoaTable.query.get(users[cont].tp)
        tipopessoa = tipopessoa.descricao
        output.append({"ID": users[cont].id,"Nome":users[cont].nome, "CPF": users[cont].cpf, "RG": users[cont].rg, "Tipo": tipopessoa})
        cont = cont+1

    return jsonify(output)

@bp_users.route('/user/mostrar/<id>', methods=['GET'])
def show_by_id(id):
    user = PessoaTable.query.get(id)
    tipopessoa = TipoPessoaTable.query.get(user.tp)

    output = {"ID":user.id,"Nome": user.nome, "CPF": user.cpf, "RG": user.rg, "Tipo": tipopessoa.descricao}
    
    
    return jsonify(output)

@bp_users.route('/user/criar', methods=['POST'])
def create():
    nome = request.json['nome']
    cpf = request.json['cpf']
    rg = request.json['rg']
    foto = request.json['foto']
    tipopessoa = request.json['tipopessoa']

    tp = TipoPessoaTable.query.filter(TipoPessoaTable.descricao==tipopessoa).first()

    tipopessoa = tp.id

    new_user = PessoaTable(nome,cpf,rg,foto,tipopessoa)

    db.session.add(new_user)
    db.session.commit()

    return jsonify('deu certo')

@bp_users.route('/user/alterar/<id>', methods=['PUT'])
def update(id):

    user = PessoaTable.query.get(id)

    nome = request.json['nome']
    cpf = request.json['cpf']
    rg = request.json['rg']
    ft = request.json['foto']
    tp = request.json['tipopessoa']

    tipopessoa = TipoPessoaTable.query.all()
    if tp in tipopessoa:
        tp = tipopessoa['descricao']

        
    if nome != "":
        user.nome = nome
    if cpf != "":
        user.cpf = cpf
    if rg != "":
        user.rg = rg
    if ft != "":
        user.ft = ft
    if tp != "":
        user.tp = tp

    db.session.commit()

    return jsonify('Usuário alterado com sucesso!')
    
@bp_users.route('/user/deletar/<id>', methods=['DELETE'])
def delete(id):
    user = PessoaTable.query.get(id)

    db.session.delete(user)
    db.session.commit()

    return jsonify('Usuário deletado com sucesso!')
    
