from flask import flask, request, jsonify, current_app
from flask_blueprint import Blueprint
from flask_sqlalchemy import SQLAlchemy
from models import PessoaTable, TipoPessoaTable
from serializer import PessoaSchema

bp_users = Blueprint('pessoa', __name__)

@bp_user.route('/user/mostrar', methods['GET'])
def show():
    ps = PessoaSchema(many=True)
    users = pessoa.query.all()
    result = ps.dump(users)

    return jsonify(result)

@bp_user.route('/user/mostrar/<id>', methods['GET'])
def show_by_id(id):
    ps = PessoaSchema
    user = pessoa.query.get(id)
    result = ps.dump(user)

    return jsonify(result)

@bp_user.route('/user/criar', methods['GET', 'POST'])
def create():
    nome = request.json['nome']
    cpf = request.json['cpf']
    rg = request.json['rg']
    ft = request.json['foto']
    tp = request.json['tipopessoa']

    tipopessoa = TipoPessoaTable.query.all()
    if tp in tipopessoa:
        tp = tipopessoa['descricao']


    new_user = PessoaTable(nome, cpf, rg, ft, tp)

    current_app.db.session.add(new_user)
    current_app.db.session.commit()

@bp_users.route('/user/alterar/<id>', methods['PUT'])
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

    current_app.db.session.commit()

    return jsonify('Usuário deletado com sucesso!')
    
@bp_users.route('/user/deletar/<id>', methods=['DELETE'])
def delete(id):
    user = PessoaTable.query.get(id)

    current_app.db.session.delete(user)

    return jsonify('Usuário deletado com sucesso!')
    
