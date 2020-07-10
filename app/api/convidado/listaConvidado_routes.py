from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from __init__ import db
from models import EventoTable, ListaConvidadosTable, PessoaTable, MoradorTable
from serializer import ListaConvidadosSchema


bp_convidado = Blueprint("convidado", __name__)

@bp_convidado.route('/convidado/criar', methods=['POST'])
def create():
    nome = request.json['nome']
    rg = request.json['rg']
    cpforganizador = request.json['cpforganizador']

    try:
        organizador = PessoaTable.query.filter_by(cpf=cpforganizador).first()
        organizador = MoradorTable.query.filter_by(morador_idpes=organizador.id).first()
        evento = EventoTable.query.order_by(EventoTable.id.desc()).filter_by(evento_idmrd=organizador.id).first()

        new_lista = ListaConvidadosTable(nome, rg, evento.id)

        db.session.add(new_lista)
        db.session.commit()

        return jsonify({"message":'Convidado inserido com sucesso!'})

    except:
        return jsonify({"message":'Não foi possível inserir o convidado, favor verificar as informações inseridas.'})

@bp_convidado.route('/convidado/<idevt>/mostrar/', methods=['GET'])
def show_lista_by_cpf_organizador(idevt):
    evento = EventoTable.query.get(idevt)

    try:
        organizador = MoradorTable.query.get(evento.evento_idmrd)
        organizador = PessoaTable.query.filter_by(id=organizador.morador_idpes).first()

        convidados = ListaConvidadosTable.query.filter_by(listaconvidados_idevt=evento.id).all() 

        output = []
        cont = 0

        for c in convidados:
            output.append({"id": convidados[cont].id,"nome":convidados[cont].nome, "rg": convidados[cont].rg, "evento": idevt, "organizador": organizador.nome})
            cont = cont+1

        return jsonify(output)

    except:
        return jsonify({"message":'Sem registros. Favor verificar as informações inseridas'})

@bp_convidado.route('/convidado/<idevt>/mostrar/<rg>', methods=['GET'])
def show_convidado_by_id(idevt, rg):
    evento = EventoTable.query.get(idevt)
    try:
        convidado = ListaConvidadosTable.query.filter_by(listaconvidados_idevt=evento.id, rg=rg).first() 
        organizador = MoradorTable.query.get(evento.evento_idmrd)
        organizador = PessoaTable.query.filter_by(id=organizador.morador_idpes).first()

        output = {"id": convidado.id, "nome":convidado.nome,"rg":convidado.rg, "evento": convidado.listaconvidados_idevt, "organizador": organizador.nome}
        return jsonify(output)
        
    except:
        return jsonify({"message":'Sem registros. Favor verificar as informações inseridas'})


@bp_convidado.route('/convidado/<idevt>/alterar/<rg>', methods=['PUT'])
def modify(idevt, rg):
    nome = request.json['nome']
    rgnovo = request.json['rg']

    evento = EventoTable.query.get(idevt)

    convidado = ListaConvidadosTable.query.filter_by(listaconvidados_idevt=evento.id, rg=rg).first()
    

    try:
        if rgnovo != '':
            convidado.rg = rgnovo
        if nome != '':
            convidado.nome = nome

        db.session.commit()

        return jsonify({"message":'Informações do convidado alteradas com sucesso!'})
    
    except:
        return jsonify({"message":'Não foi possível alterar as informações do convidado.'})

@bp_convidado.route('/convidado/<idevt>/deletar', methods=['DELETE'])
def delete_lista(idevt):


    evento = EventoTable.query.get(idevt)
    convidados = ListaConvidadosTable.query.filter_by(listaconvidados_idevt=evento.id).all() 

    cont = 0

    try:
        for c in convidados:
            convidado = convidados[cont]
            db.session.delete(convidado)
            cont = cont+1

        db.session.commit()

        return jsonify({"message":'Lista de convidados do evento '+evento.id+' deletada com sucesso!'})

    except:
        return jsonify({"message":'Ocorreu um erro ao apagar a lista de convidados, favor verificar as informações inseridas.'})

@bp_convidado.route('/convidado/<idevt>/deletar/<rg>', methods=['DELETE'])
def delete_convidado(idevt, rg):
    convidado = ListaConvidadosTable.query.filter_by(listaconvidados_idevt=idevt, rg=rg).first()

    try:
        db.session.delete(convidado)
        db.session.commit()

        return jsonify({"message":'Convidado deletado com sucesso!'})
    
    except:
        return jsonify({"message":'Não foi possível deletar o convidado, favor verificar as informações inseridas.'})
            