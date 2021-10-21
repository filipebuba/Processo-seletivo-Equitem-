import sqlite3


class Cliente():
    def __init__(self):
        self.cnpj = None
        self.nome = None
        self.site = None

    def cria_tabela(self):
        conn = sqlite3.connect("clientes.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS clientes(
            CNPJ char(18) primary key, 
            RAZAO_SOCIAL char(100),
            SITE char(2))
                ''')
        conn.commit

    def salvar(self):
        self.cria_tabela()

        conn = sqlite3.connect("clientes.db")
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO clientes VALUES('{self.cnpj}', '{self.nome}','{self.site}')")

        conn.commit()
