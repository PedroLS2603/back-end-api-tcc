from flask import Flask, Blueprint, request, jsonify 
from flask_sqlalchemy import SQLAlchemy
from models import PessoaTable, TipoPessoaTable
from __init__ import db
from serializer import PessoaSchema

bp_users = Blueprint('pessoa', __name__)

@bp_users.route('/user/mostrar', methods=['GET'])
def show():
    ps = PessoaSchema(many=True)
    users = PessoaTable.query.all()
    result = ps.dump(users)


    return jsonify(result)

@bp_users.route('/user/mostrar/<id>', methods=['GET'])
def show_by_id(id):
    ps = PessoaSchema()
    user = PessoaTable.query.get(id)
    
    return ps.jsonify(user)

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



    user.nome = nome
    user.cpf = cpf
    user.rg = rg
    user.ft = ft
    user.tp = tp

    db.session.commit()

    return jsonify('Usuário alterado com sucesso!')
    
@bp_users.route('/user/deletar/<id>', methods=['DELETE'])
def delete(id):
    user = PessoaTable.query.get(id)

    db.session.delete(user)
    db.session.commit()

    return jsonify('Usuário deletado com sucesso!')
    
