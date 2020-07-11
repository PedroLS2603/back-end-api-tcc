from flask import Flask, Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import EntradaTable, PessoaTable, SaidaTable
from __init__ import db
import datetime



bp_acesso = Blueprint('acesso', __name__)


#Rotas de entrada
@bp_acesso.route('/acesso/entrada/criar', methods=['POST'])
def createEntrada():

    ap = request.json['apartamento']
    prd = request.json['predio']
    cpf = request.json ['cpf']

    try:
        pessoa = PessoaTable.query.filter_by(cpf=cpf).first()

        pessoa = pessoa.id

        datahora = datetime.datetime.now()


        new_entrada = EntradaTable(ap, prd, pessoa, datahora)

        db.session.add(new_entrada)
        db.session.commit()
    
        return jsonify({"message":'Registro de entrada criado com sucesso!'})
    
    except:
        return jsonify({"message":"Ocorreu um erro! Caso os dados inseridos sejam válidos, tente novamente dentro de alguns minutos."})

@bp_acesso.route('/acesso/entrada/mostrar', methods=['GET'])
def show_allEntrada():
    entrds = EntradaTable.query.all()

    output = []
    cont = 0
    try:
        for i in entrds:
            output.append({"id":entrds[cont].id, "apartamento":entrds[cont].entrada_idapt, "predio": entrds[cont].entrada_idprd, "pessoa": entrds[cont].entrada_idpes, "datahora": entrds[cont].datahora})
            
            #Formatando a data e a hora
            datahora = output[cont]["datahora"]
            datahora = datahora.strftime('%d/%m/%Y %H:%M')
            output[cont]["datahora"] = datahora
            
            #Convertendo a saída de id pra nome da pessoa
            pessoa = PessoaTable.query.get(output[cont]['pessoa'])
            output[cont]["pessoa"] = pessoa.nome
            
            
            
            cont = cont+1


        return jsonify(output)

    except:
        return jsonify({"message":"Sem registro. Favor verificar as informações inseridas"}) 

@bp_acesso.route('/acesso/entrada/mostrar/<id>', methods=['GET'])
def showEntrada_by_id(id):

    entrd = EntradaTable.query.get(id)

    try:
        output = {"id": entrd.id,
                "apartamento": entrd.entrada_idapt,
                "predio": entrd.entrada_idprd,
                "pessoa": entrd.entrada_idpes,
                "datahora": entrd.datahora
        }
        
        #Convertendo o atributo pessoa do ID para o nome
        pessoa = PessoaTable.query.get(output['pessoa'])
        output['pessoa'] = pessoa.nome

        #Formatando a string datahora
        output['datahora'] = output['datahora'].strftime('%d/%m/%Y %H:%M')

        return jsonify(output)

    except:
        return jsonify({"message":"Sem registro. Favor verificar as informações inseridas"})

@bp_acesso.route('/acesso/entrada/deletar/<id>', methods=['DELETE'])
def deleteEntrada(id):

    try:
        entrada = EntradaTable.query.get(id)

        db.session.delete(entrada)
        db.session.commit()
        
        return jsonify({"message":'Registro deletado com sucesso!'})

    except:
        return jsonify({"message":'Não foi possível deletar o registro'})


#Rotas de saída
@bp_acesso.route('/acesso/saida/criar', methods=['POST'])
def createSaida():
    
    cpf = request.json['cpf']

    try:
        pessoa = PessoaTable.query.filter_by(cpf=cpf).first()
        pessoa = pessoa.id

        entrada = EntradaTable.query.filter_by(entrada_idpes=pessoa).all()
        entrada.reverse()
        entrada = entrada[0].id

        datahora = datetime.datetime.now()

        new_saida = SaidaTable(pessoa, entrada, datahora)

        db.session.add(new_saida)
        db.session.commit()

        return jsonify('Tudo certo')

    except:
        return jsonify({"message":'Não foi possível criar o registro'})

@bp_acesso.route('/acesso/saida/mostrar', methods=['GET'])
def show_allSaida():
    sds = SaidaTable.query.all()

    try:
        output = []
        cont = 0
        for i in sds:
            output.append({"idsaida":sds[cont].id, "entrada":sds[cont].saida_ident, "pessoa": sds[cont].saida_idpes, "datahora": sds[cont].datahora})
            
            #Formatando a data e a hora
            datahora = output[cont]["datahora"]
            datahora = datahora.strftime('%d/%m/%Y %H:%M')
            output[cont]["datahora"] = datahora
            
            #Convertendo a saída de id pra nome da pessoa
            pessoa = PessoaTable.query.get(output[cont]['pessoa'])
            output[cont]["pessoa"] = pessoa.nome
            
            
            cont = cont+1

        return jsonify(output)

    except:
        return jsonify({"message":"Sem registros. Favor verificar as informações inseridas"})

@bp_acesso.route('/acesso/saida/mostrar/<id>', methods=['GET'])
def showSaida_by_id(id):
    
    sd = SaidaTable.query.get(id)

    try:
        output = {"idsaida": sd.id,
                "entrada": sd.saida_ident,
                "pessoa": sd.saida_idpes,
                "datahora": sd.datahora
        }
        
        #Convertendo o atributo pessoa do ID para o nome
        pessoa = PessoaTable.query.get(output['pessoa'])
        output['pessoa'] = pessoa.nome

        #Formatando a string datahora
        output['datahora'] = output['datahora'].strftime('%d/%m/%Y %H:%M')


        return jsonify(output)

    except:
        return jsonify({"message":'Sem registros. Favor verificar as informações inseridas'})

@bp_acesso.route('/acesso/saida/deletar/<id>', methods=['DELETE'])
def deleteSaida(id):
    
    try:
        saida = SaidaTable.query.get(id)

        db.session.delete(saida)
        db.session.commit()

        return jsonify({"message":'Registro deletado com sucesso!'})
    except:
        return jsonify({"message":'Não foi possível apagar o registro.'})