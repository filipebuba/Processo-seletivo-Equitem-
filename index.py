import requests
import json
import sqlite3
from cliente import Cliente


# dictonary = None
# op = None
# request = None


def executar(opcao):
    if opcao == 1:
        consulta()
    elif opcao == 2:
        sair = False
        while not sair:
            empresa = input("Digite qual CNPJ deseja verificar: ")
            cnpjTratado = tratarCNPJ(empresa)
            req = requisicao(cnpjTratado)
            if req['status'] == "ERROR":
                print(req['message'])
            else:
                exibir_dados(req)
                confirmacao = input("Deseja cria cliente: ")
                if confirmacao.lower() == "sim" or confirmacao.lower() == "s":
                    armazenar_dados_tabela(req)
                    sair = True
                sair = True


def requisicao(cnpj):

    try:
        request = requests.get(
            "https://www.receitaws.com.br/v1/cnpj/"+cnpj)
        print(requests.status_codes)
        dictonary = json.loads(request.text)
        return dictonary
    except:
        print("Erro de conexão")
        return None


def tratarCNPJ(cnpj):
    cnpj = cnpj.replace(".", "")
    cnpj = cnpj.replace("/", "")
    cnpj = cnpj.replace("-", "")
    return cnpj


def armazenar_dados_tabela(dados):
    cliente = Cliente()
    cliente.cnpj = dados['cnpj']
    cliente.nome = dados['nome']
    cliente.site = dados['uf']
    cliente.salvar()
    return cliente


def exibir_dados(dados):
    print("CNPJ: ", dados['cnpj'])
    print("Razão Social:", dados['nome'])
    print("Site: ", dados['uf'])
    print("")


def listar(tabela):
    lista = []
    for item in tabela:
        lista.append(item[0])
    return lista


def consulta():
    consulta_cnpj = 'SELECT CNPJ FROM clientes'
    consulta_geral = 'SELECT * FROM clientes'

    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()
    cursor.execute(consulta_cnpj)
    linhas = cursor.fetchall()
    lista = listar(linhas)
    print("")
    print(f"Lista de CNPJ\'s: {lista}", "\n")

    cursor.execute(consulta_geral)
    linhas = cursor.fetchall()
    for linha in linhas:
        print(f'CNPJ: {linha[0]}')
        print(f'RAZÃO:{linha[1]}',)
        print(f'RAZÃO:{linha[2]}', '\n')


while True:
    op = int(input(''' Digite uma Opção:

        1 - Listar CNPJ\'s cadastrados
        2 - Importar dados do CNPJ
        :'''))
    executar(op)
