###########################################################################
# Author: Howard Roatti
# Created: 02/09/2022
# Last Update: 03/09/2022
#
# Essa classe auxilia na conexão com o Banco de Dados Oracle
# Documentação base:
#                  (1) https://cx-oracle.readthedocs.io/en/latest/user_guide/sql_execution.html
#                  (2) https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html
#                  (3) https://cx-oracle.readthedocs.io/en/latest/index.html
###########################################################################
import json
from pathlib import Path

try:
    import cx_Oracle
except ImportError:
    # O cx_Oracle não possui instalação para Python 3.11+.
    # O oracledb é o driver oficial atual e mantém a mesma API básica.
    import oracledb as cx_Oracle

from pandas import DataFrame


class OracleQueries:

    def __init__(self, can_write: bool = False):
        self.can_write = can_write
        self.host = "localhost"
        self.port = 1521
        self.service_name = 'XEPDB1'
        self.sid = 'XE'
        self.conn = None
        self.cur = None

        # O caminho é relativo a este arquivo, então o sistema pode ser
        # executado a partir de qualquer diretório.
        auth_file = (Path(__file__).resolve().parent
                     / "passphrase" / "authentication.oracle")
        with open(auth_file, "r", encoding="utf-8") as f:
            # strip() remove o \n final e evita ORA-01017 (senha inválida).
            self.user, self.passwd = (parte.strip() for parte in f.read().split(",", 1))

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass

    def connectionString(self, in_container: bool = False):
        '''
        Esse método cria uma string de conexão utilizando os parâmetros necessários
        Parameters:
        - host: endereço da localização do servidor
        - port: porta a qual o Oracle está escutando
        - service_name: nome do serviço criado para o banco de dados Oracle
        - sid: id do serviço
        return: string de conexão
        '''
        if not in_container:
            string_connection = cx_Oracle.makedsn(host=self.host,
                                                  port=self.port,
                                                  sid=self.sid
                                                  )
        else:
            string_connection = cx_Oracle.makedsn(host=self.host,
                                                  port=self.port,
                                                  service_name=self.service_name
                                                  )
        return string_connection

    def connect(self):
        '''
        Esse método realiza a conexão com o banco de dados Oracle
        Parameters:
        - user: nome do usuário criado para utilização do banco de dados
        - password: senha do usuário criado para utilização do banco de dados
        - dsn: string de conexão para acessar o banco de dados oracle
        - enconding: codificação de caracteres para não haver erros com caracteres em português
        return: um cursor que permite utilizar as funções da biblioteca cx_Oracle
        '''

        try:
            self.conn = cx_Oracle.connect(user=self.user,
                                          password=self.passwd,
                                          dsn=self.connectionString()
                                          )
        except Exception:
            # Se a conexão por SID falhar (comum em containers Oracle XE),
            # tenta pelo service_name (ex.: XEPDB1).
            self.conn = cx_Oracle.connect(user=self.user,
                                          password=self.passwd,
                                          dsn=self.connectionString(in_container=True)
                                          )
        self.cur = self.conn.cursor()
        return self.cur

    def _execute(self, query: str, params=None):
        """Executa a query, com ou sem variáveis de bind."""
        if params is None:
            self.cur.execute(query)
        else:
            self.cur.execute(query, params)

    def sqlToDataFrame(self, query: str, params=None) -> DataFrame:
        '''
        Esse método irá executar uma query
        Parameters:
        - query: consulta utilizada para recuperação dos dados
        - params: dicionário (ou lista) com os valores das variáveis de bind
        return: um DataFrame da biblioteca Pandas
        '''
        self._execute(query, params)
        rows = self.cur.fetchall()
        return DataFrame(rows, columns=[col[0].lower() for col in self.cur.description])

    def sqlToMatrix(self, query: str, params=None) -> tuple:
        '''
        Esse método irá executar uma query
        Parameters:
        - query: consulta utilizada para recuperação dos dados
        - params: dicionário (ou lista) com os valores das variáveis de bind
        return: uma matriz (lista de listas), uma lista com os nomes das colunas(atributos) da(s) tabela(s)
        '''
        self._execute(query, params)
        rows = self.cur.fetchall()
        matrix = [list(row) for row in rows]
        columns = [col[0].lower() for col in self.cur.description]
        return matrix, columns

    def sqlToJson(self, query: str, params=None):
        '''
        Esse método irá executar uma query
        Parameters:
        - query: consulta utilizada para recuperação dos dados
        - params: dicionário (ou lista) com os valores das variáveis de bind
        return: um objeto json
        '''
        self._execute(query, params)
        columns = [col[0].lower() for col in self.cur.description]
        self.cur.rowfactory = lambda *args: dict(zip(columns, args))
        rows = self.cur.fetchall()
        return json.dumps(rows, default=str)

    def write(self, query: str, params=None):
        if not self.can_write:
            raise Exception('Can\'t write using this connection')

        self._execute(query, params)
        self.conn.commit()

    def close(self):
        if self.cur is not None:
            self.cur.close()
            self.cur = None
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def executeDDL(self, query: str):
        '''
        Esse método irá executar o comando DDL enviado no atributo query
        Parameters:
        - query: consulta utilizada para comandos DDL
        '''
        self.cur.execute(query)
