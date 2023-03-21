from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades, Usuarios
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)

# USERS = {
#     'rafael':'123',
#     'ademir':'123'
# }

@auth.verify_password
def verificacao(login, senha):
    if not (login, senha):
        return False
    return Usuarios.query.filter_by(login=login, senha=senha).first()

class Pessoa(Resource):
    @auth.login_required
    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        try:
            response = {
                'nome':pessoa.nome,
                'idade':pessoa.id,
                'id':pessoa.id
            }
        except AttributeError:
            response = {
                'status':'error',
                'mensagem':'Pessoa não encontrada'
            }
        return response

    def put(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        dados = request.json
        if 'nome' in dados:
            pessoa.nome = dados['nome']
        if 'idade' in dados:
            pessoa.idade = dados['idade']
        pessoa.save()
        response = {
            'nome':pessoa.nome,
            'idade':pessoa.id,
            'id':pessoa.id
        }
        return response
    
    def delete(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        mensagem = f'Pessoa {pessoa.nome} excluida com sucesso'
        pessoa.delete()
        return {'status':'sucesso', 'mensagem':mensagem}
    
class ListaPessoas(Resource):
    @auth.login_required
    def get(self):
        pessoas = Pessoas.query.all()
        response = [{'id':pessoa.id, 'nome':pessoa.nome, 'idade':pessoa.idade} for pessoa in pessoas]
        return response
    
    def post(self):
        data = request.json
        pessoa = Pessoas(nome=data['nome'], idade=data['idade'])
        pessoa.save()
        response = {
            'nome':pessoa.nome,
            'idade':pessoa.id,
            'id':pessoa.id
        }
        return response

class Atividade(Resource):
    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        atividades = Atividades.query.filter_by(pessoa=pessoa).all()
        response = [{'id':atividade.id, 'nome':atividade.nome, 'status':atividade.status,'pessoa':atividade.pessoa.nome} for atividade in atividades]
        return response

class StatusAtividade(Resource):
    def get(self, id):
        atividade = Atividades.query.filter_by(id=id).first()
        response = {
            'id':atividade.id, 
            'status':atividade.status
        }
        return response
    
    def put(self, id):
        data = request.json
        atividade = Atividades.query.filter_by(id=id).first()
        atividade.status = data['status']
        response = {
            'id':atividade.id, 
            'status':atividade.status
        }
        return response

class ListaAtividade(Resource):
    def get(self):
        atividades = Atividades.query.all()
        response = [{'id':atividade.id, 'nome':atividade.nome, 'status':atividade.status, 'pessoa':atividade.pessoa.nome} for atividade in atividades]
        return response
    
    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()
        atividade = Atividades(nome=dados['nome'], pessoa=pessoa, status=dados['status'])
        atividade.save()
        response ={
            'status':atividade.status,
            'pessoa':atividade.pessoa.nome,
            'nome':atividade.nome,
            'id': atividade.id
        }
        return response
            
api.add_resource(Pessoa, '/pessoa/<string:nome>/')
api.add_resource(ListaPessoas, '/pessoa/')
api.add_resource(ListaAtividade, '/atividades/')
api.add_resource(Atividade, '/atividades/<string:nome>/')
api.add_resource(StatusAtividade, '/atividades/status/<int:id>/')

if __name__== '__main__':
    app.run(debug=True)