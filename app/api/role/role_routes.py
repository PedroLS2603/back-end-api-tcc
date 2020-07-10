from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from serializer import TipoPessoaSchema
from __init__ import db
from models import TipoPessoaTable

bp_role = Blueprint('role', __name__)

@bp_role.route('/tipopessoa/mostrar', methods=['GET'])
def show():

    tp = TipoPessoaTable.query.all()
    output =[]
    cont= 0 

    try:
        for t in tp:
            output.append({"id": tp.id, "descricao":tp.descricao})
            cont= cont +1

        return jsonify(output)

    except:
        return jsonify('Sem registros.')

@bp_role.route('/tipopessoa/mostrar/<id>', methods=['GET'])
def show_by_id(id):
    try:
        tp = TipoPessoaTable.query.get(id)
        output = {"id": tp.id, "descricao":tp.descricao}

        return jsonify(output)

    except:
        return jsonify('Sem registro.')

@bp_role.route('/tipopessoa/criar', methods=['POST'])
def create():
    descricao = request.json['descricao']

    try:
        new_role = TipoPessoaTable(descricao)

        db.session.add(new_role)
        db.session.commit()

        return jsonify('Tipo criado com sucesso!')

    except:
        return jsonify('Erro ao criar tipo. Verifique as informações inseridas')

@bp_role.route('/tipopessoa/alterar/<id>', methods=['PUT'])
def update(id):
    tp = TipoPessoaTable.query.get(id)

    descricao = request.json['descricao']

    try:
        if descricao !='':
            tp.descricao = descricao

        db.session.add(tp)
        db.session.commit()
        
        return jsonify("Informações do tipo alteradas com sucesso!")

    except:
        return jsonify('Não foi possível alterar as informações do tipo. Verifique as informações inseridas.')

@bp_role.route('/tipopessoa/delete/<id>', methods=['DELETE'])
def delete(id):
    role = TipoPessoaTable.query.get(id)

    try:
        db.session.delete(role)
        db.session.commit()

        return jsonify('Tipo deletado com sucesso!')
    
    except:
        return jsonify('Erro ao deletar tipo.')
