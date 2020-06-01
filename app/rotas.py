from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


@app.route('/')
def index():
    return ("fodase")

