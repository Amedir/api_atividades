from models import Pessoas, Usuarios

#Insere dados na tabela de pessoas
def insere_pessoas():
    pessoa = Pessoas(nome='Nate', idade=20)
    print(pessoa)
    pessoa.save()

# Realiza consulta na tabela pessoa
def consulta():
    pessoa = Pessoas.query.all()
    print(pessoa)
    pessoa = Pessoas.query.filter_by(nome = 'Ademir').first()
    print(pessoa.nome)

# Altera dados de uma pessoa
def altera_pessoa():
    pessoa = Pessoas.query.filter_by(nome='Ademir').first()
    pessoa.idade = 10
    pessoa.save()

# Exclui uma pessoa no banco de dados
def exclui_pessoa():
    pessoa =    Pessoas.query.filter_by(nome='Nate').first()
    pessoa.delete()

def insere_usuarios(login, senha):
    usuario = Usuarios(login=login, senha=senha)
    usuario.save()

def consulta_todos_usuarios():
    usuarios = Usuarios.query.all()
    print(usuarios)

if __name__ == '__main__':
    # insere_pessoas()
    # altera_pessoa()
    # exclui_pessoa()
    # consulta()
    # insere_usuarios('ademir', '123')
    # insere_usuarios('rafa', '123')
    consulta_todos_usuarios()