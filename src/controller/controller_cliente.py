from conexion.oracle_queries import OracleQueries
from model.clientes import Cliente


class ControllerCliente:

    def __init__(self):
        pass

    # ------------------------------------------------------------------
    # Leitura e validação de dados
    # ------------------------------------------------------------------
    @staticmethod
    def _ler_texto(mensagem: str, tamanho_maximo: int = None) -> str:
        while True:
            valor = input(mensagem).strip()
            if not valor:
                print("Este campo não pode ficar vazio.")
                continue
            if tamanho_maximo and len(valor) > tamanho_maximo:
                print(f"Use no máximo {tamanho_maximo} caracteres.")
                continue
            return valor

    @staticmethod
    def _ler_cpf(mensagem: str) -> str:
        while True:
            cpf = "".join(caractere for caractere in input(mensagem)
                          if caractere.isdigit())
            if len(cpf) == 11:
                return cpf
            print("O CPF deve conter exatamente 11 dígitos.")

    @staticmethod
    def _ler_id(mensagem: str) -> int:
        while True:
            try:
                valor = int(input(mensagem).strip())
                if valor > 0:
                    return valor
            except ValueError:
                pass
            print("Digite um ID inteiro maior que zero.")

    # ------------------------------------------------------------------
    # Consultas auxiliares
    # ------------------------------------------------------------------
    def _buscar_cliente(self, oracle: OracleQueries, id_cliente: int):
        df_cliente = oracle.sqlToDataFrame(
            "SELECT ID, NOME, CPF, TELEFONE FROM CLIENTES WHERE ID = :id",
            {"id": id_cliente},
        )
        if df_cliente.empty:
            return None
        linha = df_cliente.iloc[0]
        return Cliente(int(linha["id"]), linha["nome"],
                       linha["cpf"], linha["telefone"])

    def verificar_existencia(self, oracle: OracleQueries, id_cliente: int) -> bool:
        df_cliente = oracle.sqlToDataFrame(
            "SELECT COUNT(1) FROM CLIENTES WHERE ID = :id",
            {"id": id_cliente},
        )
        return int(df_cliente.iloc[0, 0]) > 0

    def verificar_existencia_por_cpf(self, oracle: OracleQueries, cpf: str) -> bool:
        df_cliente = oracle.sqlToDataFrame(
            "SELECT COUNT(1) FROM CLIENTES WHERE CPF = :cpf",
            {"cpf": cpf},
        )
        return int(df_cliente.iloc[0, 0]) > 0

    def exibir_cliente(self, oracle: OracleQueries, id_cliente: int):
        cliente = self._buscar_cliente(oracle, id_cliente)
        if cliente is not None:
            print(cliente.to_string())
        return cliente

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------
    def inserir(self) -> Cliente:
        oracle = OracleQueries(can_write=True)
        try:
            oracle.connect()

            print("\n--- Cadastrar Novo Cliente ---")
            nome = self._ler_texto("Nome do cliente: ", 255)
            cpf = self._ler_cpf("CPF (somente números): ")
            telefone = self._ler_texto("Telefone: ", 20)

            if self.verificar_existencia_por_cpf(oracle, cpf):
                print(f"O CPF {cpf} já está cadastrado no sistema.")
                return None

            df_id = oracle.sqlToDataFrame(
                "SELECT CLIENTES_ID_SEQ.NEXTVAL AS ID FROM DUAL"
            )
            id_cliente = int(df_id.iloc[0]["id"])

            oracle.write(
                "INSERT INTO CLIENTES (ID, NOME, CPF, TELEFONE) "
                "VALUES (:id, :nome, :cpf, :telefone)",
                {"id": id_cliente, "nome": nome, "cpf": cpf, "telefone": telefone},
            )

            cliente = Cliente(id_cliente, nome, cpf, telefone)
            print("\nCliente cadastrado com sucesso!")
            print(cliente.to_string())
            return cliente
        finally:
            oracle.close()

    def atualizar(self) -> Cliente:
        oracle = OracleQueries(can_write=True)
        try:
            oracle.connect()
            if self._listar_dataframe(oracle).empty:
                return None

            print("\n--- Atualizar Cliente ---")
            id_cliente = self._ler_id("ID do cliente que deseja atualizar: ")

            if not self.verificar_existencia(oracle, id_cliente):
                print(f"Cliente com ID {id_cliente} não encontrado.")
                return None

            print("\nInforme os novos dados:")
            novo_nome = self._ler_texto("Novo nome: ", 255)
            novo_cpf = self._ler_cpf("Novo CPF (somente números): ")
            novo_telefone = self._ler_texto("Novo telefone: ", 20)

            outro_cliente = oracle.sqlToDataFrame(
                "SELECT COUNT(1) FROM CLIENTES WHERE CPF = :cpf AND ID <> :id",
                {"cpf": novo_cpf, "id": id_cliente},
            )
            if int(outro_cliente.iloc[0, 0]) > 0:
                print(f"O CPF {novo_cpf} já pertence a outro cliente.")
                return None

            oracle.write(
                "UPDATE CLIENTES SET NOME = :nome, CPF = :cpf, "
                "TELEFONE = :telefone WHERE ID = :id",
                {"nome": novo_nome, "cpf": novo_cpf,
                 "telefone": novo_telefone, "id": id_cliente},
            )

            print("\nCliente atualizado com sucesso!")
            return self.exibir_cliente(oracle, id_cliente)
        finally:
            oracle.close()

    def remover(self):
        oracle = OracleQueries(can_write=True)
        try:
            oracle.connect()
            if self._listar_dataframe(oracle).empty:
                return None

            print("\n--- Remover Cliente ---")
            id_cliente = self._ler_id("ID do cliente que deseja remover: ")

            if not self.verificar_existencia(oracle, id_cliente):
                print(f"Cliente com ID {id_cliente} não encontrado.")
                return None

            cliente = self._buscar_cliente(oracle, id_cliente)
            if cliente is not None:
                print(cliente.to_string())

            # Confirma a remoção do cliente ANTES de apagar qualquer locação.
            confirmacao = input(
                f"Tem certeza que deseja excluir o cliente ID {id_cliente}? (s/n): "
            )
            if confirmacao.strip().lower() != "s":
                print("Operação cancelada.")
                return None

            df_locacoes = oracle.sqlToDataFrame(
                "SELECT COUNT(1) FROM LOCACOES WHERE ID_CLIENTE = :id",
                {"id": id_cliente},
            )
            qtd_locacoes = int(df_locacoes.iloc[0, 0])

            if qtd_locacoes > 0:
                print(f"Atenção: este cliente possui {qtd_locacoes} locação(ões).")
                resposta = input(
                    "Deseja remover também as locações deste cliente? (s/n): "
                )
                if resposta.strip().lower() != "s":
                    print("Operação cancelada para preservar as locações.")
                    return None
                oracle.write(
                    "DELETE FROM LOCACOES WHERE ID_CLIENTE = :id",
                    {"id": id_cliente},
                )

            oracle.write("DELETE FROM CLIENTES WHERE ID = :id", {"id": id_cliente})
            print("Cliente removido com sucesso!")
            return cliente
        finally:
            oracle.close()

    def _listar_dataframe(self, oracle: OracleQueries):
        df_clientes = oracle.sqlToDataFrame(
            "SELECT ID, NOME, CPF, TELEFONE FROM CLIENTES ORDER BY ID"
        )
        print("\n--- Lista de Clientes ---")
        if df_clientes.empty:
            print("Nenhum cliente cadastrado.")
        else:
            for _, linha in df_clientes.iterrows():
                print(f"ID: {linha['id']} | Nome: {linha['nome']} | "
                      f"CPF: {linha['cpf']} | Telefone: {linha['telefone']}")
        return df_clientes

    def listar(self):
        oracle = OracleQueries()
        try:
            oracle.connect()
            return self._listar_dataframe(oracle)
        finally:
            oracle.close()
