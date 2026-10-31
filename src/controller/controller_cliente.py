from conexion.oracle_queries import OracleQueries
from model.clientes import Cliente


class ControllerCliente:

  def __init__(self):
    pass

  def inserir(self):
    oracle = OracleQueries()
    oracle.connect()

    print("\n--- Cadastrar Novo Cliente ---")
    nome = input("Digite o nome do cliente: ")
    cpf = input("Digite o CPF do cliente: ")
    telefone = input("Digite o telefone do cliente: ")

    if self.verificar_existencia_por_cpf(oracle, cpf):
      print(f"O CPF {cpf} já está cadastrado no sistema.")
      return

    sql_seq = "SELECT cliente_id_seq.NEXTVAL FROM DUAL"
    id_cliente = oracle.sqlToDataFrame(sql_seq).iloc[0, 0]

    sql_insert = f"INSERT INTO clientes VALUES ({id_cliente}, '{nome}', '{cpf}', '{telefone}')"
    oracle.execute(sql_insert)

    print(
        f"Cliente {nome} cadastrado com sucesso com o ID"
        f" {id_cliente} (ID: {id_cliente})."
    )

  def atualizar(self):
    oracle = OracleQueries()
    oracle.connect()

    print("\n--- Atualizar Cliente ---")
    id_cliente = input("Digite o ID do cliente que deseja atualizar: ")

    if not self.verificar_existencia(oracle, id_cliente):
      print(f"Cliente com ID {id_cliente} não encontrado.")
      return

    print("Informe os novos dados:")
    novo_nome = input("Novo nome: ")
    novo_cpf = input("Novo CPF: ")
    novo_telefone = input("Novo telefone: ")

    sql_update = f"UPDATE clientes SET nome = '{novo_nome}', cpf = '{novo_cpf}', telefone = '{novo_telefone}' WHERE id = {id_cliente}"
    oracle.execute(sql_update)

    print("\nCliente atualizado com sucesso!")
    self.exibir_cliente(oracle, id_cliente)

  def remover(self):
    oracle = OracleQueries()
    oracle.connect()

    print("\n--- Remover Cliente ---")
    id_cliente = input("Digite o ID do cliente que deseja remover: ")

    if not self.verificar_existencia(oracle, id_cliente):
      print(f"Cliente com ID {id_cliente} não encontrado.")
      return

    sql_fk = f"SELECT COUNT(1) FROM locacoes WHERE id_cliente = {id_cliente}"
    qtd_locacoes = oracle.sqlToDataFrame(sql_fk).iloc[0, 0]

    if qtd_locacoes > 0:
      print(
          f"Atenção: Este cliente possui {qtd_locacoes} locação(ões) vinculada(s)."
      )
      pergunta = (
          "Deseja remover também as locações associadas a este cliente? (s/n): "
      )
      if input(pergunta).strip().lower() == "s":
        sql_del_loc = f"DELETE FROM locacoes WHERE id_cliente = {id_cliente}"
        oracle.execute(sql_del_loc)
        print("Locações do cliente removidas com sucesso.")
      else:
        print("Remoção cancelada para evitar inconsistência de chave estrangeira.")
        return

    confirmacao = input(
        f"Tem certeza que deseja excluir o cliente ID {id_cliente}? (s/n): "
    )
    if confirmacao.strip().lower() == "s":
      sql_delete = f"DELETE FROM clientes WHERE id = {id_cliente}"
      oracle.execute(sql_delete)
      print("Cliente removido com sucesso!")
    else:
      print("Operação cancelada.")

  def listar(self):
    oracle = OracleQueries()
    oracle.connect()

    sql = "SELECT id, nome FROM clientes ORDER BY id"
    df = oracle.sqlToDataFrame(sql)

    print("\n--- Lista de Clientes ---")
    if df.empty:
      print("Nenhum cliente cadastrado.")
    else:
      for _, row in df.iterrows():
        print(f"ID: {row['ID']} | Nome: {row['NOME']}")

  def verificar_existencia(self, oracle, id_cliente):
    sql = f"SELECT COUNT(1) FROM clientes WHERE id = {id_cliente}"
    df = oracle.sqlToDataFrame(sql)
    return df.iloc[0, 0] > 0

  def verificar_existencia_por_cpf(self, oracle, cpf):
    sql = f"SELECT COUNT(1) FROM clientes WHERE cpf = '{cpf}'"
    df = oracle.sqlToDataFrame(sql)
    return df.iloc[0, 0] > 0

  def exibir_cliente(self, oracle, id_cliente):
    sql = f"SELECT id, nome, cpf, telefone FROM clientes WHERE id = {id_cliente}"
    df = oracle.sqlToDataFrame(sql)
    if not df.empty:
      print(
          f"Registro Atual - ID: {df.iloc[0]['ID']} | Nome:"
          f" {df.iloc[0]['NOME']} | CPF: {df.iloc[0]['CPF']} | Telefone:"
          f" {df.iloc[0]['TELEFONE']}"
      )