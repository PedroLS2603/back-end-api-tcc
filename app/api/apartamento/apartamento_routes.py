from flask import Blueprint, jsonify, request
from __init__ import db
from flask_sqlalchemy import SQLAlchemy
from serializer import ApartamentoSchema
from models import ApartamentoTable

bp_apartamento = Blueprint('apartamento', __name__)

