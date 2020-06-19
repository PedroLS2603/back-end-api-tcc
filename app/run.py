from __init__ import app
from api.role.role_routes import bp_role
from api.users.users_routes import bp_users
from api.predio.predio_routes import bp_predio
from api.apartamento.apartamento_routes import bp_apartamento
from api.access.access_routes import bp_entrada

app.register_blueprint(bp_role)
app.register_blueprint(bp_users)
app.register_blueprint(bp_predio)
app.register_blueprint(bp_apartamento)
app.register_blueprint(bp_entrada)






if __name__ == '__main__':
    app.run()