from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from __init__ import db
from models import EventoTable, ListaConvidadoTable, PessoaTable, MoradorTable
from serializer import EventoSchema, ListaConvidadoSchema

bp_convidado = Blueprint("convidado", __name__)

@bp_convidado.route('/convidado/criar', methods=['POST'])
def create():
    nome = request.json['nome']
    rg = request.json['rg']
    cpforganizador = request.json['cpforganizador']

    organizador = PessoaTable.query.filter_by(cpf=cpforganizador).first()
    organizador = MoradorTable.query.filter_by(morador_idpes=organizador.id).first()
    evento = EventoTable.query.filter_by(evento_idmrd=organizador.id).first()

    new_lista = ListaConvidadoTable(nome, rg, evento)

    db.session.add(new_lista)
    db.session.commit()

    return jsonify('Tudo certo')


@bp_convidado.route('/convidado/mostrar/<cpforganizador>', methods=['GET'])
def show_lista_by_cpf_organizador(cpforganizador):
    organizador = PessoaTable.query.filter_by(cpf=cpforganizador).first()
    evento = EventoTable.query.filter_by(evento_idmrd=organizador.id).order_by(EventoTable.id.desc()).first()

    convidados = ListaConvidadoTable.query.filter_by(listaconvidados_idevt=evento.id).all() 

    cont = 0

    for c in convidados:
        output.append({"ID": convidados[cont].id,"Nome":convidados[cont].nome, "RG": convidados[cont].rg, "Evento": convidados[cont].listaconvidados_idevt, "Organizador": organizador.nome})
        cont = cont+1

    return jsonify(output)

@bp_convidado.route('/convidado/mostrar/<id>', methods=['GET'])
def show_convidado_by_id(id):

    convidado = ListaConvidadoTable.query.get(id) 

    evento = EventoTable.query.get(listaconvidados_idevt)

    organizador = MoradorTable.query.get(evento.evento_idmrd)
    organizador = PessoaTable.query.filter_by(id=morador_idpes).first()

    output = {"ID": convidado.id, "Nome":convidado.nome,"RG":convidado.rg, "Evento": listaconvidados_idevt, "Organizador": organizador.nome}

    return jsonify(output)

@bp_convidado.route('/convidado/alterar/<id>', methods=['PUT'])
def modify(id):
    nome = request.json['nome']
    rg = request.json['rg']

    convidado = ListaConvidadoTable.query.get(id)
    
    if rg != '':
        convidado.rg = rg
    if nome != '':
        convidado.nome = nome

    db.session.commit()

    return jsonify('Tudo certo')

@bp_convidado.route('/convidado/deletar/<cpf>', methods=['DELETE'])
def delete_lista(cpf):
    convidados = PessoaTable.query.filter_by(cpf=cpf).first()
    evento = EventoTable.query.filter_by(evento_idmrd=organizador.id).order_by(EventoTable.id.desc()).first()

    convidados = ListaConvidadoTable.query.filter_by(listaconvidados_idevt=evento.id).all() 

    db.session.delete(convidados)
    db.session.commit()

    return jsonify('Tudo certo')

@bp_convidado.route('/convidado/deletar/<id>', methods=['DELETE'])
def delete_convidado(id):
    convidado = ListaConvidadoTable.query.get(id)

    db.session.delete(convidado)
    db.session.commit()

    return jsonify('Tudo certo')