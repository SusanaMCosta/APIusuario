from flask import Flask, jsonify
from flask_restful import Api
from resources.usuario import User, UserRegister, UserLogin, UserLogout
from flask_jwt_extended import JWTManager #cuidar da autenticação
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)

api.add_resource(Usuarios, '/usuarios')
api.add_resource(Usuario, '/usuarios/<int:id_usuario>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')


if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)

# http://127.0.0.1:5000/usuarios
