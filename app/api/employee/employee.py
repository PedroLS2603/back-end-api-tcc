from flask import jsonify
from models import SysAccessTable
from flask_sqlalchemy import SQLAlchemy

class Funcionario():
    def authenticate_login(account, psw):
        comp_login = sysaccess.query.filter(sysaccess.login=account).all()
        comp_senha = sysaccess.query.filter(sysaccess.senha=psw).all()
        if comp_login and comp_senha == True:
            return True
        else:
            return False

    def create_account(account, psw):
        new_account = SysAccessTable(account, psw)

        session.add(new_account)
        session.commit()

        