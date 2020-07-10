from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from serializer import FuncionarioSchema
from models import PessoaTable, FuncionarioTable
from __init__ import db


bp_employee = Blueprint('employee', __name__)

@bp_employee.route('/funcionario/criar', methods=['POST'])
def create():
    cpf = request.json['cpf']
    funcao = request.json['funcao']
    
    pes = PessoaTable.query.filter_by(cpf=cpf).first()

    try:
        new_func = FuncionarioTable(pes.id, funcao)

        db.session.add(new_func)
        db.session.commit()

        return jsonify('Funcionário criado com sucesso!')
    
    except:
        return jsonify('Não foi possível criar funcionário.')

@bp_employee.route('/funcionario/mostrar', methods=['GET'])
def show_all():
    
    all_func = FuncionarioTable.query.all()
    
    cont = 0 
    output = []

    try:
        for f in all_func:
            pes = PessoaTable.query.get(all_func[cont].func_idpessoa)
            output.append({"id":func.id, "nome": pes.nome, "funcao": all_func[cont].funcao})
            cont = cont+1

        return jsonify(output)

    except:
        return jsonify('Sem registros.')

@bp_employee.route('/funcionario/mostrar/<id>', methods=['GET'])
def show_by_id(id):
    

    func = FuncionarioTable.query.get(id)
    pes = PessoaTable.query.get(func.func_idpessoa)

    try:
        output = {"id":func.id, "nome": pes.nome, "funcao": func.funcao}

        return jsonify(output)

    except:
        return jsonify('Sem registro.')

@bp_employee.route('/funcionario/alterar/<id>', methods=['PUT'])
def modify(id):
    
    func = FuncionarioTable.query.get(id)

    funcao = request.json['funcao']
    cpf = request.json['cpf']

    try:    
        if cpf != "":
            fc = PessoaTable.query.filter_by(cpf=cpf).first()
            func.func_idpessoa = fc.id
        if funcao != '':
            func.funcao = funcao
        db.session.commit()

        return jsonify('Informações do funcionário alterada com sucesso!')

    except:
        return jsonify('Não foi possível alterar as informações do funcionário')

@bp_employee.route('/funcionario/deletar/<id>', methods=['DELETE'])
def delete(id):
    
    try:
        func = FuncionarioTable.query.get(id)

        db.session.delete(func)
        db.session.commit()

        return jsonify('Funcionário deletado com sucesos!')
    
    except:
        return jsonify('Erro ao deletar funcionário.')