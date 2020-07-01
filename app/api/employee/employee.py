from flask import jsonify
from models import SysAccessTable
from flask_sqlalchemy import SQLAlchemy

class Funcionario():
    def authenticate_login(self, account, psw):
        user = SysAccessTable.query.filter_by(login=account).first()

    if not user.login and user.senha:
        auth = False

    def create_account(self, account, psw):
        new_account = SysAccessTable(account, psw)

        session.add(new_account)
        session.commit()

        