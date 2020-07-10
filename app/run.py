from __init__ import app
from api.role.role_routes import bp_role
from api.users.users_routes import bp_users
from api.predio.predio_routes import bp_predio
from api.apartamento.apartamento_routes import bp_apartamento
from api.access.access_routes import bp_acesso
from api.dweller.dweller_routes import bp_morador
from api.problem.problem_routes import bp_problema
from api.employee.employee_routes import bp_employee
from api.mail.mail_routes import bp_encomenda
from api.event.event_routes import bp_evento
from api.convidado.listaConvidado_routes import bp_convidado

app.register_blueprint(bp_role)
app.register_blueprint(bp_users)
app.register_blueprint(bp_predio)
app.register_blueprint(bp_apartamento)
app.register_blueprint(bp_acesso)
app.register_blueprint(bp_morador)
app.register_blueprint(bp_problema)
app.register_blueprint(bp_employee)
app.register_blueprint(bp_encomenda)
app.register_blueprint(bp_evento)
app.register_blueprint(bp_convidado)


if __name__ == '__main__':
    app.run()