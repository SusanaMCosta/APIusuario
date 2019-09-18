from flask_restful import Resource, reqparse
from models.usuario import UserModel
import sqlite3

class Users(Resource):
    def get(self):
        return {'usuarios': [usuario.json() for usuario in UserModel.query.all()]}

#login e o email
atributos = reqparse.RequestParser()
atributos.add_argument('nome', type=str, required=True, help="O campo nome nome pode ser deixado em branco")
atributos.add_argument('matricula', type=str, required=True, help="O campo matricula não pode ser deixado em branco")
atributos.add_argument('email', type=str, required=True, help="O campo login não pode ser deixado em branco")
atributos.add_argument('senha', type=str, required=True, help="O campo senha não pode ser deixado em branco")
atributos.add_argument('curso', type=int, required=True, help="O campo matricula não pode ser deixado em branco")

class User(Resource):

    def get(self, email):
        user = UserModel.find_user(email)
        if user:
            return user.json()
        return {'message':'User not found'}, 440

    def delete(self, email):
        user = UserModel.find_user(email)
        if user:
            try:
                user.delete_user()
            except:
                return {'message':'houve um erro interno, por favor tente novamente'}, 500
            return {'message': 'User deleted.'}
        return {'message': 'User not found.'}, 404

    def put(self, email):
        dados = atributos.parse_args()
        user_encontrado = UserModel.find_user(dados['email'])
        if user_encontrado:
            user_encontrado.update_user(**dados)
            user_encontrado.save_user()
            return user_encontrado.json(), 200 #hotel atualizado
        user = UserModel(**dados)
        try:
            user.save_user()
        except:
            return {'message':'houve um erro interno, por favor tente novamente'}, 500 # erro no servidor
        return user.json(), 201 # hotel criado

class UserRegister(Resource):
    # Cadastro
    def post(self):
        dados = atributos.parse_args()

        if UserModel.find_user(dados['email']):
            return {"message":"o email '{}' ja foi cadastrado".format(dados['email'])}

        user = UserModel(**dados)
        user.save_user()
        return {'message':'usuario criado com sucesso!'}, 201

class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        user = UserModel.find_user(dados['email'])

        if user and safe_str_cmp(user.senha,dados['senha']):
            return {'message':'usuario logado'}, 200
        return {'message':'email ou senha esta incorreto'}, 401

class UserLogout(Resource):

    def post(self):
        jwt_id = get_raw_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message':'logout com sucesso'}, 200

'''
    def put(self, id_usuario):

        dados = Usuario.argumentos.parse_args()
        novo_usuario = {'id_usuario':id_usuario, **dados}

        usuario = Usuario.encontre_usuario(id_usuario)
        if usuario:
            usuario.update(novo_usuario)
            return novo_usuario, 200
        usuarios.append(novo_usuario)
        return novo_usuario, 201
'''
