from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from serializer import TipoPessoaSchema
from __init__ import db
from models import TipoPessoaTable

bp_role = Blueprint('role', __name__)

@bp_role.route('/tipopessoa/mostrar', methods=['GET'])
def show():
    tps = TipoPessoaSchema(many=True)
    tp = TipoPessoaTable.query.all()
    result = tps.dump(tp)

    return jsonify(result)

@bp_role.route('/tipopessoa/mostrar/<id>', methods=['GET'])
def show_by_id():
    tps = TipoPessoaSchema()
    tp = TipoPessoaTable.query.get(id)
    result = tps.dump(tp)

    return jsonify(result)

@bp_role.route('/tipopessoa/criar', methods=['POST'])
def create():
    descricao = request.json['descricao']

    new_role = TipoPessoaTable(descricao)

    db.session.add(new_role)
    db.session.commit()

    return jsonify('Certin certin, meu bom')

@bp_role.route('/tipopessoa/<id>', methods=['PUT'])
def update(id):
    tp = TipoPessoaTable.query.get(id)

    descricao = request.json['descricao']

    tp.descricao = descricao

    db.session.add(tp)
    db.session.commit()

@bp_role.route('/tipopessoa/delete/<id>', methods=['DELETE'])
def delete(id):
    role = TipoPessoaTable.query.get(id)

    db.session.delete(role)

    return jsonify('certin certin')