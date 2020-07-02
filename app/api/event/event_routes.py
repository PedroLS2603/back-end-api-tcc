from flask import Flask, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from __init__ import db
from models import  EventoTable, ListaConvidadoTable
from serializer import EventoSchema, ListaConvidadoSchema

bp_evento = Blueprint('evento', __name__)