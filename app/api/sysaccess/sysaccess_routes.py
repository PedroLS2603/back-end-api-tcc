from flask import Flask, request, Blueprint, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from __init__ import db
from models import SysAccessTable

bp_auth = Blueprint('auth', __name__)

@bp_auth.route('/login', methods=['POST'])
def login():
    login = request.json["usuario"]
    senha = request.json["senha"]
    try:

        user = SysAccessTable.query.filter_by(login=login, senha=senha).first()

        if user:
            return jsonify({"message":"Bem-vindo "+login+'!', "status":True})
        else:
            return jsonify({"message":'Acesso negado!', "status": False, "login":login, "senha": senha})
    except:
        return jsonify({"message":"Ocorreu um erro", "status":False, "login": login, "senha": senha})

@bp_auth.route('/cadastrar', methods=['POST'])
def sign_up():
    try:
        login = request.json['usuario']
        senha = request.json['senha']

        user = SysAccessTable.query.filter_by(login=login, senha=senha).first()
        
        if user:
            return jsonify({"message":'Nome de usuário já cadastrado.'})
        
        new_ac = SysAccessTable(login, senha)

        db.session.add(new_ac)
        db.session.commit()

        return jsonify({"message":'Conta criada com sucesso!'})
    except:
        return jsonify({"message":"Houve um erro ao cadastrar a conta, verifique as informações inseridas."})