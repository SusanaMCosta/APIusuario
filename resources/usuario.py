from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST
import sqlite3

#login e o email

atributos = reqparse.RequestParser()
atributos.add_argument('id_usuario', type=str, required=True, help="O campo id_usuario n���o pode ser deixado em branco")
atributos.add_argument('nome', type=str, required=True, help="O campo nome n���o pode ser deixado em branco")
atributos.add_argument('matricula', type=str, required=True, help="O campo matricula n���o pode ser deixado em branco")
atributos.add_argument('email', type=str, required=True, help="O campo login n���o pode ser deixado em branco")
atributos.add_argument('senha', type=str, required=True, help="O campo senha n���o pode ser deixado em branco")
atributos.add_argument('curso', type=int, required=True, help="O campo matricula n���o pode ser deixado em branco")

class User(Resource):



    def get(self, id_user):
        user = UserModel.find_user(id_user)
        if user:
            return user.json()
        return {'message':'User not found'}, 440

    @jwt_required
    def delete(self, id_user):
        user = UserModel.find_user(id_user)
        if user:
            try:
                user.delete_user()
            except:
                return {'message':'houve um erro interno, por favor tente novamente'}, 500
            return {'message': 'User deleted.'}
        return {'message': 'User not found.'}, 404

class UserRegister(Resource):

    # Cadastro
    def post(self):
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['email']):
            return {"message":"o email '{}' ja foi cadastrado".format(dados['email'])}

        user = UserModel(**dados)
        user.save_user()
        return {'message':'usuario criado com sucesso!'}, 201

class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        user = UserModel.find_by_login(dados['email'])

        if user and safe_str_cmp(user.senha,dados['senha']):
            token_de_acesso = create_access_token(identity=user.id_user)
            return {'access_token':token_de_acesso}, 200
        return {'message':'email ou senha esta incorreto'}, 401

class UserLogout(Resource):

    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message':'logout com sucesso'}, 200

'''
from flask import Flask
from flask_restful import Resource, reqparse

usuarios = [
        {
        'id_usuario':1,
        'nome':'Susana',
        'matricula':'402510',
        'email':'suzanasuzy12@hotmail.com',
        'senha':'testando',
        'curso':1
        },
        {
        'id_aluno':2,
        'nome':'Marlo',
        'matricula':'403010',
        'email':'marloLouco@hotmail.com',
        'senha':'teste',
        'curso':1
        }
]

class Usuarios(Resource):
    def get(self):
        return {'usuario': usuarios}

class Usuario(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('matricula')
    argumentos.add_argument('email')
    argumentos.add_argument('senha')
    argumentos.add_argument('curso')

    def encontre_usuario(id_usuario):
        for usuario in usuarios:
            if usuario['id_usuario'] == id_usuario:
                return usuario
        return None

    def get(self, id_usuario):

        usuario = Usuario.encontre_usuario(id_usuario)
        if usuario:
            return usuario
        return {'message':'usuario não encontrado'}, 404

    def post(self, id_usuario):

        dados = Usuario.argumentos.parse_args()

        novo_usuario = {
            'id_usuario': id_usuario,
            'nome': dados['nome'],
            'matricula': dados['matricula'],
            'email': dados['email'],
            'senha': dados['senha'],
            'curso': dados['curso']
        }

        usuarios.append(novo_usuario)
        return novo_usuario, 200

    def put(self, id_usuario):

        dados = Usuario.argumentos.parse_args()
        novo_usuario = {'id_usuario':id_usuario, **dados}

        usuario = Usuario.encontre_usuario(id_usuario)
        if usuario:
            usuario.update(novo_usuario)
            return novo_usuario, 200
        usuarios.append(novo_usuario)
        return novo_usuario, 201

    def delete(self, id_usuario):
        global usuarios
        usuarios = [usuario for usuario in usuarios if usuario['id_usuario'] != id_usuario]
        return {'message':'Usuario apagado'}
'''
