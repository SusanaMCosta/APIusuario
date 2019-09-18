from flask import Flask, jsonify
from flask_restful import Api
from resources.usuario import Users, User, UserRegister, UserLogin, UserLogout

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
api = Api(app)

@app.before_first_request
def cria_banco():
    banco.create_all()

api.add_resource(Users, '/usuarios')
api.add_resource(User, '/usuarios/<string:email>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)

# http://127.0.0.1:5000/usuarios
