from flask import Blueprint, request, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
from serializer import TipoPessoaSchema
from models import TipoPessoaTable

bp_role = Blueprint('role', __name__)

@bp_role.route('/tipopessoa/mostrar')
def show():
    tps = TipoPessoaSchema(many=True)
    tp = tipopessoa.query.all()
    result = tps.dump(tp)

    return jsonify(result)

@bp_role.route('/tipopessoa/mostrar/<id>')
def show_by_id():
    tps = TipoPessoaSchema()
    tp = tipopessoa.query.get(id)
    result = tps.dump(tp)

    return jsonify(result)

@bp_role.route('/tipopessoa/criar')
def create():
    dscr = request.json['descricao']

    new_role = TipoPessoaTable(dscr)

    current_app.db.add(new_role)
    current_app.db.commit()