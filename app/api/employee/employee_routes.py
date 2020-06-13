from flask import Blueprint, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
from serializer import FuncionarioSchema
from employee import authenticate_login, create_account

bp_employee = Blueprint('employee', __name__)

@bp_employee.route('/funcionario/mostrar', methods=['GET'])
def show():
    fs = FuncionarioSchema(many=True)
    all_func = funcionario.query.all()
    result = fs.dump(all_func)

    return jsonify(result)

@bp_employee.route('/funcionario/mostrar/<id>', methods=['GET'])
def show_by_id(id):
    
    fs = FuncionarioSchema()
    func = funcionario.query.filter(id=id)
    result = rs.dump(func)

    return jsonify(result)

@bp_employee.route('/funcionario/login', methods=['GET', 'POST'])
def login():
    pass

@bp_employee.route('/funcionario/', methods=['GET', 'POST'])
def create():
    pass


