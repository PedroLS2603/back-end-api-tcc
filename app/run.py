from __init__ import app
from api.role.role_routes import bp_role

app.register_blueprint(bp_role)

if __name__ == '__main__':
    app.run()