from __init__ import app
from api.role.role_routes import bp_role
from api.users.users_routes import bp_users

app.register_blueprint(bp_role)
app.register_blueprint(bp_users)






if __name__ == '__main__':
    app.run()