from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from __init__ import db
from models import  EventoTable, ListaConvidadosTable, PessoaTable, MoradorTable
from serializer import EventoSchema, ListaConvidadosSchema
import datetime


bp_evento = Blueprint('evento', __name__)

@bp_evento.route('/evento/criar', methods=['POST'])
def create():

    cpf = request.json['cpf']
    data = request.json['data']
    hinicio = request.json['inicio']
    hfinal = request.json['final']
    predio = request.json['predio']

    inicio = data+' '+hinicio
    final = data+' '+hfinal

    inicio = datetime.datetime.strptime(inicio, '%d/%m/%Y %H:%M')
    final = datetime.datetime.strptime(final, '%d/%m/%Y %H:%M')

    mrd = PessoaTable.query.filter_by(cpf=cpf).first()
    mrd = MoradorTable.query.filter_by(morador_idpes=mrd.id).first()
    mrd = mrd.id

    new_evento = EventoTable(inicio, final, mrd, predio)

    db.session.add(new_evento)
    db.session.commit()  
    return jsonify('Tudo certo')

@bp_evento.route('/evento/mostrar', methods=['GET'])
def show_all():

    eventos = EventoTable.query.all()
    output = []
    cont = 0

    for e in eventos:
        pes = MoradorTable.query.get(eventos[cont].evento_idmrd)
        pes = PessoaTable.query.get(pes.morador_idpes)
        pes = pes.nome


        output.append({"ID":eventos[cont].id, "Organizador": pes, "Data": eventos[cont].inicio.strftime('%d/%m/%Y'), "Horário de início": eventos[cont].inicio.strftime('%H:%M'), "Horário de encerramento": eventos[cont].final.strftime('%H:%M'), "Local": "Prédio "+str(eventos[cont].evento_idprd) })
        cont = cont+1

    return jsonify(output)

@bp_evento.route('/evento/mostrar/<id>', methods=['GET'])
def show_by_id(id):
    evento = EventoTable.query.get(id)
    pes = MoradorTable.query.get(evento.evento_idmrd)
    pes = PessoaTable.query.get(pes.morador_idpes)
    pes = pes.nome


    output = {"ID":evento.id, "Organizador": pes, "Data": evento.inicio.strftime('%d/%m/%Y'), "Horário de início": evento.inicio.strftime('%H:%M'), "Horário de encerramento": evento.final.strftime('%H:%M'), "Local": "Prédio "+str(evento.evento_idprd) }

    return jsonify(output)

@bp_evento.route('/evento/alterar/<id>', methods=['PUT'])
def modify(id):
    evento = EventoTable.query.get(id)

    cpf = request.json['cpf']
    data = request.json['data']
    hinicio = request.json['inicio']
    hfinal = request.json['final']
    predio = request.json['predio']


    if cpf != '':
        mrd = PessoaTable.query.filter_by(cpf=cpf).first()
        mrd = MoradorTable.query.filter_by(morador_idpes=mrd.id).first()
        evento.evento_idmrd = mrd.id

    if hinicio != '':
        evento.inicio = datetime.datetime.strptime(evento.inicio.strftime('%d/%m/%Y')+' '+hinicio, '%d/%m/%Y %H:%M')

    if hfinal != '':
        evento.final = datetime.datetime.strptime(evento.final.strftime('%d/%m/%Y')+' '+hfinal, '%d/%m/%Y %H:%M')

    if data != '':
        dinicio = data+' '+evento.inicio.strftime('%H:%M')
        dfinal = data+' '+evento.final.strftime('%H:%M')
        
        evento.inicio = datetime.datetime.strptime(dinicio, '%d/%m/%Y %H:%M')
        evento.final = datetime.datetime.strptime(dfinal, '%d/%m/%Y %H:%M')

    if predio != '':
        evento.evento_idprd = predio

    db.session.commit()
    return jsonify('Tudo certo')

@bp_evento.route('/evento/deletar/<id>', methods=['DELETE'])
def delete(id):
    evento = EventoTable.query.get(id)
    
    db.session.delete(evento)
    db.session.commit()

    return jsonify('Tudo certo')