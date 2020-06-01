from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from run import app

#instanciando o banco
db = SQLAlchemy(app)

#configurando migrações
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)



#Tabelas
class TipoPessoaTable(db.Model):
    __tablename__ = 'tipopessoa'

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(50), unique=True, nullable=False)

    #Configuração dos relacionamentos
    pessoa = db.relationship('Pessoa', backref='tipopessoa')

    def __init__(self, descricao):
        self.descricao = descricao


class PessoaTable(db.Model):
    __tablename__ = 'pessoa'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(45), unique=True, nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    rg = db.Column(db.String(12), unique=True, nullable=False)
    foto = db.Column(db.String(80), unique=True, nullable=False)
    tipopessoa = db.Column(db.Integer, db.ForeignKey('tipopessoa.id'))

    #Configuração dos relacionamentos
    funcionario_idpessoa = db.relationship('Funcionario', backref='funcionario_idpessoa')
    morador_idpessoa = db.relationship('Morador', backref='morador_idpessoa')
    entrada_idpessoa = db.relationship('Entrada', backref='entrada_idpessoa')
    saida_idpessoa = db.relationship('Saida', backref='saida_idpessoa')
    encomenda_idpessoa = db.relationship('Encomenda', backref='encomenda_idpessoa')

    def __init__(self, nome, cpf, rg, foto):
        self.nome = nome
        self.cpf = cpf
        self.rg = rg
        self.foto = foto

class FuncionarioTable(db.Model):
    __tablename__= 'funcionario'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), unique=True, nullable=False)
    senha = db.Column(db.String(20), unique=True, nullable=False)
    funcionario_idpessoa = db.Column(db.Integer, db.ForeignKey('pessoa.id'), unique=True, nullable=False)

    def __init__(self, login, senha, funcionario_idpessoa):
        self.login = login
        self.senha = senha
        self.funcionario_idpessoa = funcionario_idpessoa

class PredioTable(db.Model):
    __tablename__ = 'predio'

    id = db.Column(db.Integer, primary_key=True)
    evento = db.Column(db.Boolean, unique=True, nullable=False)

    #Configuração dos relacionamentos
    apartamento_idpredio = db.relationship('Apartamento', backref='apartamento_idpredio')
    morador_idpredio = db.relationship('Morador', backref='morador_idpredio')
    entrada_idpredio = db.relationship('Entrada', backref='entrada_idpredio')
    evento_idpredio = db.relationship('Evento', backref='evento_idpredio')
    problema_idpredio = db.relationship('Problema', backref='problema_idpredio')

    def __init__(self, evento):
        self.evento = evento

class ApartamentoTable(db.Model):
    __tablename__ = 'apartamento'   

    id = db.Column(db.Integer, primary_key=True)
    apartamento_idpredio = db.Column(db.Integer, db.ForeignKey('predio.id'), unique=True, nullable=False)

    #Configuração dos relacionamentos
    morador_idapartamento = db.relationship('Morador', backref='morador_idapartamento')
    entrada_idapartamento = db.relationship('Entrada', backref='entrada_idapartamento')
    problema_idapartamento = db.relationship('Problema', backref='problema_idapartamento')

    def __init__(self, apartamento_idpredio):
        self.apartamento_idpredio = apartamento_idpredio

class MoradorTable(db.Model):
    __tablename__ = 'morador'
    
    id = db.Column(db.Integer, primary_key=True)
    morador_idapartamento = db.Column(db.Integer, db.ForeignKey('apartamento.id'), unique=True, nullable=False)
    morador_idpredio = db.Column(db.Integer, db.ForeignKey('predio.id'), unique=True, nullable=False)
    morador_idpessoa = db.Column(db.Integer, db.ForeignKey('pessoa.id'), unique=True, nullable=False)

    #Configuração dos relacionamentos
    evento_idmorador = db.relationship('Evento', backref='evento_idmorador')

    def __init__(self, morador_idapartamento, morador_idpredio, morador_idpessoa):
        self.morador_idapartamento = morador_idapartamento
        self.morador_idpredio = morador_idpredio
        self.morador_idpessoa = morador_idpessoa


class EntradaTable(db.Model):
    __tablename__ = 'entrada'

    id = db.Column(db.Integer, primary_key=True)
    entrada_idapartamento = db.Column(db.Integer, db.ForeignKey('apartamento.id'), unique=True, nullable=False)
    entrada_idpredio = db.Column(db.Integer, db.ForeignKey('predio.id'), unique=True, nullable=False)
    entrada_idpessoa = db.Column(db.Integer, db.ForeignKey('pessoa.id'), unique=True, nullable=False)
    datahora = db.Column(db.DateTime, unique=True, nullable=False)

    #Configuração dos relacionamentos
    saida_identrada = db.relationship('Saida', backref='saida_identrada')

    def __init__(self, entrada_idapartamento, entrada_idpredio, entrada_idpessoa, datahora):
        self.entrada_idapartamento = entrada_idapartamento
        self.entrada_idpredio = entrada_idpredio
        self.entrada_idpessoa = entrada_idpessoa
        self.datahora=datahora

class SaidaTable(db.Model):
    __tablename__ = 'saida'

    id = db.Column(db.Integer, primary_key=True)
    saida_idpessoa = db.Column(db.Integer, db.ForeignKey('pessoa.id'), unique=True, nullable=False)
    saida_identrada = db.Column(db.Integer, db.ForeignKey('entrada.id'), unique=True)
    datahora = db.Column(db.DateTime, unique=True, nullable=False)

    def __init__(self, saida_idpessoa, saida_identrada, datahora):
        self.saida_idpessoa = saida_idpessoa
        self.saida_identrada = saida_identrada        
        self.datahora = datahora

class EncomendaTable(db.Model):
    __tablename__ = 'encomenda'

    id = db.Column(db.Integer, primary_key=True)
    encomenda_idpessoa = db.Column(db.Integer, db.ForeignKey('pessoa.id'), unique=True, nullable=False)

    def __init__(self, encomenda_idpessoa):
        self.encomenda_idpessoa = encomenda_idpessoa

class EventoTable(db.Model):
    __tablename__ = 'evento'

    id = db.Column(db.Integer, primary_key=True)
    datahora = db.Column(db.DateTime, unique=True, nullable=False)
    evento_idmorador = db.Column(db.Integer, db.ForeignKey('morador.id'), unique=True, nullable=False)
    evento_idpredio = db.Column(db.Integer, db.ForeignKey('predio.id'), unique=True, nullable=False)

    #Configuração dos relacionamentos
    listaconvidados_idevento = db.relationship('ListaConvidados', backref='listaconvidados_idevento')

    def __init__(self, datahora, evento_idmorador, evento_idpredio):
        self.datahora = datahora
        self.evento_idmorador = evento_idmorador
        self.evento_idpredio = evento_idpredio

class ListaConvidadosTable(db.Model):
    __tablename__ = 'listaconvidados'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(45), unique=True, nullable=False)
    rg = db.Column(db.String(12), unique=True, nullable=False)
    listaconvidados_idevento = db.Column(db.Integer, db.ForeignKey('evento.id'), unique=True, nullable=False)

    def __init(self, nome, rg, listaconvidados_idevento):
        self.nome = nome 
        self.rg = rg
        self.listaconvidados_idevento = listaconvidados_idevento

class ProblemaTable(db.Model):
    __tablename__ = 'problema'

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), unique=True, nullable=False)
    problema_idpredio = db.Column(db.Integer, db.ForeignKey('predio.id'), unique=True, nullable=False)
    problema_idapartamento = db.Column(db.Integer, db.ForeignKey('apartamento.id'), unique=True, nullable=False)

    def __init__(self, descricao, problema_idpredio, problema_idapartamento):
        self.descricao = descricao
        self.problema_idpredio = problema_idpredio
        self.problema_idapartamento = problema_idapartamento

#Migrando dados

if __name__ == '__main__':
    manager.run()
