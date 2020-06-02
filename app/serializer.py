from flask_marshmallow import Marshmallow
from run import app

ma = Marshmallow(app)

class TipoPessoaSchema(ma.Schema):
    class Meta:
        fields = ("descricao")

class PessoaSchema(ma.Schema):
    class Meta:
        fields = ("nome","cpf","rg","foto","tipopessoa")

class FuncionarioSchema(ma.Schema):
    class Meta:
        fields = ("login", "senha","funcionario_idpessoa")

class PredioSchema(ma.Schema):
    class Meta:
        fields = ("evento")

class ApartamentoSchema(ma.Schema):
    class Meta:
        fields = ("apartamento_idpredio")

class MoradorSchema(ma.Schema):
    class Meta:
        fields = ("morador_idapartamento". "morador_idpredio", "morador_idpessoa")

class EntradaSchema(ma.Schema):
    class Meta:
        fields = ("entrada_idapartamento", "entrada_idpredio", "entrada_idpessoa", "datahora")

class SaidaSchema(ma.Schema):
    class Meta:
        fields = ("saida_idpessoa", "saida_identrada", "datahora ")

class EncomendaSchema(ma.Schema):
    class Meta:
        fields = ("encomenda_idpessoa")

class EventoSchema(ma.Schema):
    class Meta:
        fields = ("datahora", "evento_idmorador", "evento_idpredio")

class ListaConvidadosSchema(ma.Schema):
    class Meta:
        fields = ("nome", "rg", "listaconvidados_idevento")

class ProblemaSchema(ma.Schema):
    class Meta:
        fields = ("descricao", "problema_idpredio", "problema_idapartamento")