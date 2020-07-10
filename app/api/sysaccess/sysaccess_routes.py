from flask import Flask, request, Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy
from __init__ import db
from models import SysAccessTable

bp_auth = Blueprint('auth', __name__)

@bp_auth.route('/login', methods=['POST'])
def login():
    login = request.json['usuario']
    senha = request.json['senha']

    user = SysAccessTable.query.filter_by(login=login, senha=senha).first()

    if user:
        return jsonify('Bem vindo '+login+'!')
    else:
        return jsonify('Acesso negado!')

@bp_auth.route('/cadastrar', methods=['POST'])
def sign_up():
    login = request.json['usuario']
    senha = request.json['senha']

    user = SysAccessTable.query.filter_by(login=login, senha=senha).first()
    
    if user:
        return jsonify('Nome de usuário já cadastrado.')
    
    new_ac = SysAccessTable(login, senha)

    db.session.add(new_ac)
    db.session.commit()

    return jsonify('Conta criada com sucesso!')