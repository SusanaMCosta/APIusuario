from sql_alchemy import banco

class UserModel(banco.Model):
    __tablename__ = 'usuarios'

    id_user = banco.Column(banco.Integer, primary_key=True)
    nome = banco.Column(banco.String(40))
    matricula = banco.Column(banco.Integer)
    email = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))
    curso = banco.Column(banco.Integer)

    def __init__(self, nome, matricula, email, senha, curso):
        self.nome = nome
        self.matricula = matricula
        self.email = email
        self.senha = senha
        self.curso = curso

    def json(self):
        return {
            'id_user': self.id_user,
            'nome': self.nome,
            'matricula': self.matricula,
            'email': self.email,
            'senha': self.senha,
            'curso': self.curso
            }

    @classmethod
    def find_user(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_login(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user
        return None

    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()
