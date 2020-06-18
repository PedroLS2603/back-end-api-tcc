from flask_sqlalchemy import SQLAlchemy
from __init__ import db

#Tabelas

class SysAccessTable(db.Model):
    __tablename__ = 'sysaccess'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), unique=True, nullable=False)
    senha = db.Column(db.String(20), nullable=False)

class TipoPessoaTable(db.Model):
    __tablename__ = 'tipopessoa'

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(50), unique=True, nullable=False)

    #Configuração dos relacionamentos
    pessoa = db.relationship('PessoaTable', backref='tipopessoa')

    def __init__(self, descricao):
        self.descricao = descricao


class PessoaTable(db.Model):
    __tablename__ = 'pessoa'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(45), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    rg = db.Column(db.String(12), unique=True, nullable=False)
    foto = db.Column(db.String(80), unique=True, nullable=False)
    tp = db.Column(db.Integer, db.ForeignKey('tipopessoa.id'))

    #Configuração dos relacionamentos
    funcionario_idpessoa = db.relationship('FuncionarioTable', backref='funcionario_idpessoa')
    morador_idpessoa = db.relationship('MoradorTable', backref='morador_idpessoa')
    entrada_idpessoa = db.relationship('EntradaTable', backref='entrada_idpessoa')
    saida_idpessoa = db.relationship('SaidaTable', backref='saida_idpessoa')
    encomenda_idpessoa = db.relationship('EncomendaTable', backref='encomenda_idpessoa')

    def __init__(self, nome, cpf, rg, foto, tp):
        self.nome = nome
        self.cpf = cpf
        self.rg = rg
        self.foto = foto
        self.tp = tp
        

class FuncionarioTable(db.Model):
    __tablename__= 'funcionario'

    id = db.Column(db.Integer, primary_key=True)
    func_idpessoa = db.Column(db.Integer, db.ForeignKey('pessoa.id'), unique=True, nullable=False)

    def __init__(self, login, senha, funcionario_idpessoa):
        self.login = login
        self.senha = senha
        self.funcionario_idpessoa = funcionario_idpessoa

class PredioTable(db.Model):
    __tablename__ = 'predio'

    id = db.Column(db.Integer, primary_key=True)
    evento = db.Column(db.Boolean, nullable=False)

    #Configuração dos relacionamentos
    apartamento_idpredio = db.relationship('ApartamentoTable', backref='apartamento_idpredio')
    morador_idpredio = db.relationship('MoradorTable', backref='morador_idpredio')
    entrada_idpredio = db.relationship('EntradaTable', backref='entrada_idpredio')
    evento_idpredio = db.relationship('EventoTable', backref='evento_idpredio')
    problema_idpredio = db.relationship('ProblemaTable', backref='problema_idpredio')

    def __init__(self, evento):
        self.evento = evento

class ApartamentoTable(db.Model):
    __tablename__ = 'apartamento'   

    id = db.Column(db.Integer, primary_key=True)
    apartamento_idprd = db.Column(db.Integer, db.ForeignKey('predio.id'), unique=True, nullable=False)

    #Configuração dos relacionamentos
    morador_idapartamento = db.relationship('MoradorTable', backref='morador_idapartamento')
    entrada_idapartamento = db.relationship('EntradaTable', backref='entrada_idapartamento')
    problema_idapartamento = db.relationship('ProblemaTable', backref='problema_idapartamento')

    def __init__(self, apartamento_idpredio):
        self.apartamento_idpredio = apartamento_idpredio

class MoradorTable(db.Model):
    __tablename__ = 'morador'
    
    id = db.Column(db.Integer, primary_key=True)
    morador_idapt = db.Column(db.Integer, db.ForeignKey('apartamento.id'), unique=True, nullable=False)
    morador_idprd = db.Column(db.Integer, db.ForeignKey('predio.id'), unique=True, nullable=False)
    morador_idpes = db.Column(db.Integer, db.ForeignKey('pessoa.id'), unique=True, nullable=False)

    #Configuração dos relacionamentos
    evento_idmrd = db.relationship('EventoTable', backref='evento_idmorador')

    def __init__(self, morador_idapartamento, morador_idpredio, morador_idpessoa):
        self.morador_idapartamento = morador_idapartamento
        self.morador_idpredio = morador_idpredio
        self.morador_idpessoa = morador_idpessoa


class EntradaTable(db.Model):
    __tablename__ = 'entrada'

    id = db.Column(db.Integer, primary_key=True)
    entrada_idapt = db.Column(db.Integer, db.ForeignKey('apartamento.id'), unique=True, nullable=False)
    entrada_idprd = db.Column(db.Integer, db.ForeignKey('predio.id'), unique=True, nullable=False)
    entrada_idpes = db.Column(db.Integer, db.ForeignKey('pessoa.id'), unique=True, nullable=False)
    datahora = db.Column(db.DateTime, unique=True, nullable=False)

    #Configuração dos relacionamentos
    saida_identrada = db.relationship('SaidaTable', backref='saida_identrada')

    def __init__(self, entrada_idapartamento, entrada_idpredio, entrada_idpessoa, datahora):
        self.entrada_idapartamento = entrada_idapartamento
        self.entrada_idpredio = entrada_idpredio
        self.entrada_idpessoa = entrada_idpessoa
        self.datahora=datahora

class SaidaTable(db.Model):
    __tablename__ = 'saida'

    id = db.Column(db.Integer, primary_key=True)
    saida_idpes = db.Column(db.Integer, db.ForeignKey('pessoa.id'), unique=True, nullable=False)
    saida_ident = db.Column(db.Integer, db.ForeignKey('entrada.id'), unique=True)
    datahora = db.Column(db.DateTime, unique=True, nullable=False)

    def __init__(self, saida_idpessoa, saida_identrada, datahora):
        self.saida_idpessoa = saida_idpessoa
        self.saida_identrada = saida_identrada        
        self.datahora = datahora

class EncomendaTable(db.Model):
    __tablename__ = 'encomenda'

    id = db.Column(db.Integer, primary_key=True)
    encomenda_idpes = db.Column(db.Integer, db.ForeignKey('pessoa.id'), unique=True, nullable=False)

    def __init__(self, encomenda_idpessoa):
        self.encomenda_idpessoa = encomenda_idpessoa

class EventoTable(db.Model):
    __tablename__ = 'evento'

    id = db.Column(db.Integer, primary_key=True)
    datahora = db.Column(db.DateTime, unique=True, nullable=False)
    evento_idmrd = db.Column(db.Integer, db.ForeignKey('morador.id'), unique=True, nullable=False)
    evento_idprd = db.Column(db.Integer, db.ForeignKey('predio.id'), unique=True, nullable=False)

    #Configuração dos relacionamentos
    listaconvidados_idevento = db.relationship('ListaConvidadosTable', backref='listaconvidados_idevento')

    def __init__(self, datahora, evento_idmorador, evento_idpredio):
        self.datahora = datahora
        self.evento_idmorador = evento_idmorador
        self.evento_idpredio = evento_idpredio

class ListaConvidadosTable(db.Model):
    __tablename__ = 'listaconvidados'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(45), unique=True, nullable=False)
    rg = db.Column(db.String(12), unique=True, nullable=False)
    listaconvidados_idevt = db.Column(db.Integer, db.ForeignKey('evento.id'), unique=True, nullable=False)

    def __init(self, nome, rg, listaconvidados_idevento):
        self.nome = nome 
        self.rg = rg
        self.listaconvidados_idevento = listaconvidados_idevento

class ProblemaTable(db.Model):
    __tablename__ = 'problema'

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), unique=True, nullable=False)
    problema_idprd = db.Column(db.Integer, db.ForeignKey('predio.id'), unique=True, nullable=False)
    problema_idapt = db.Column(db.Integer, db.ForeignKey('apartamento.id'), unique=True, nullable=False)

    def __init__(self, descricao, problema_idpredio, problema_idapartamento):
        self.descricao = descricao
        self.problema_idpredio = problema_idpredio
        self.problema_idapartamento = problema_idapartamento

