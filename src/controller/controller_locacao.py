from datetime import datetime

from conexion.oracle_queries import OracleQueries
from model.clientes import Cliente
from model.veiculos import Veiculo
from model.locacoes import Locacao


class ControllerLocacao:
    def __init__(self):
        pass

    # ------------------------------------------------------------------
    # Leitura e validação de dados
    # ------------------------------------------------------------------
    def _ler_id(self, mensagem: str) -> int:
        while True:
            try:
                id_registro = int(input(mensagem).strip())
                if id_registro > 0:
                    return id_registro
            except ValueError:
                pass
            print("Digite um ID inteiro maior que zero.")

    def _ler_data(self, mensagem: str):
        while True:
            try:
                return datetime.strptime(input(mensagem).strip(), "%d/%m/%Y").date()
            except ValueError:
                print("Data inválida. Use o formato DD/MM/AAAA.")

    def _ler_valor_total(self) -> float:
        while True:
            try:
                valor = float(input("Valor total: R$ ").strip().replace(",", "."))
                if 0 <= valor <= 99999999.99:
                    return round(valor, 2)
            except ValueError:
                pass
            print("Informe um valor entre 0 e 99.999.999,99.")

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

    def _buscar_veiculo(self, oracle: OracleQueries, id_veiculo: int):
        df_veiculo = oracle.sqlToDataFrame(
            "SELECT ID, MODELO, PLACA, ANO, VALOR_DIARIA FROM VEICULOS "
            "WHERE ID = :id",
            {"id": id_veiculo},
        )
        if df_veiculo.empty:
            return None
        linha = df_veiculo.iloc[0]
        return Veiculo(int(linha["id"]), linha["modelo"], linha["placa"],
                       int(linha["ano"]), float(linha["valor_diaria"]))

    def _buscar_locacao(self, oracle: OracleQueries, id_locacao: int):
        query = """
            SELECT l.ID AS ID_LOCACAO, l.DATA_RETIRADA, l.DATA_DEVOLUCAO,
                   l.VALOR_TOTAL, c.ID AS ID_CLIENTE, c.NOME, c.CPF, c.TELEFONE,
                   v.ID AS ID_VEICULO, v.MODELO, v.PLACA, v.ANO, v.VALOR_DIARIA
            FROM LOCACOES l
            JOIN CLIENTES c ON c.ID = l.ID_CLIENTE
            JOIN VEICULOS v ON v.ID = l.ID_VEICULO
            WHERE l.ID = :id
        """
        df_locacao = oracle.sqlToDataFrame(query, {"id": id_locacao})
        if df_locacao.empty:
            return None

        linha = df_locacao.iloc[0]
        cliente = Cliente(int(linha["id_cliente"]), linha["nome"],
                          linha["cpf"], linha["telefone"])
        veiculo = Veiculo(int(linha["id_veiculo"]), linha["modelo"],
                          linha["placa"], int(linha["ano"]),
                          float(linha["valor_diaria"]))
        return Locacao(int(linha["id_locacao"]), linha["data_retirada"],
                       linha["data_devolucao"], float(linha["valor_total"]),
                       cliente, veiculo)

    def verifica_existencia_locacao(self, oracle: OracleQueries,
                                    id_locacao: int) -> bool:
        df_locacao = oracle.sqlToDataFrame(
            "SELECT ID FROM LOCACOES WHERE ID = :id",
            {"id": int(id_locacao)},
        )
        return not df_locacao.empty

    def verificar_existencia(self, oracle: OracleQueries, id_locacao: int) -> bool:
        return self.verifica_existencia_locacao(oracle, id_locacao)

    # ------------------------------------------------------------------
    # Solicitação dos dados de uma locação
    # ------------------------------------------------------------------
    def _solicitar_dados(self, oracle: OracleQueries):
        print("\nClientes disponíveis:")
        df_clientes = oracle.sqlToDataFrame(
            "SELECT ID, NOME FROM CLIENTES ORDER BY NOME"
        )
        if df_clientes.empty:
            print("Nenhum cliente cadastrado. Cadastre um cliente antes.")
            return None
        print(df_clientes.to_string(index=False))
        id_cliente = self._ler_id("ID do cliente: ")
        cliente = self._buscar_cliente(oracle, id_cliente)
        if cliente is None:
            print("Cliente não encontrado. Operação cancelada.")
            return None

        print("\nVeículos disponíveis:")
        df_veiculos = oracle.sqlToDataFrame(
            "SELECT ID, MODELO, PLACA FROM VEICULOS ORDER BY MODELO"
        )
        if df_veiculos.empty:
            print("Nenhum veículo cadastrado. Cadastre um veículo antes.")
            return None
        print(df_veiculos.to_string(index=False))
        id_veiculo = self._ler_id("ID do veículo: ")
        veiculo = self._buscar_veiculo(oracle, id_veiculo)
        if veiculo is None:
            print("Veículo não encontrado. Operação cancelada.")
            return None

        data_retirada = self._ler_data("Data de retirada (DD/MM/AAAA): ")
        data_devolucao = self._ler_data("Data de devolução (DD/MM/AAAA): ")
        if data_devolucao < data_retirada:
            print("A devolução não pode acontecer antes da retirada.")
            return None

        valor_total = self._ler_valor_total()
        return cliente, veiculo, data_retirada, data_devolucao, valor_total

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------
    def listar_locacoes(self, oracle: OracleQueries = None,
                        need_connect: bool = False):
        fechar_conexao = oracle is None
        if fechar_conexao:
            oracle = OracleQueries()

        try:
            if fechar_conexao or need_connect:
                oracle.connect()

            query = """
                SELECT l.ID, c.NOME AS CLIENTE, v.MODELO AS VEICULO,
                       v.PLACA, l.DATA_RETIRADA, l.DATA_DEVOLUCAO, l.VALOR_TOTAL
                FROM LOCACOES l
                JOIN CLIENTES c ON c.ID = l.ID_CLIENTE
                JOIN VEICULOS v ON v.ID = l.ID_VEICULO
                ORDER BY l.ID
            """
            df_locacoes = oracle.sqlToDataFrame(query)
            print("\n--- Lista de Locações ---")
            if df_locacoes.empty:
                print("Nenhuma locação cadastrada.")
            else:
                print(df_locacoes.to_string(index=False))
            return df_locacoes
        finally:
            if fechar_conexao:
                oracle.close()

    def inserir_locacao(self) -> Locacao:
        oracle = OracleQueries(can_write=True)
        try:
            oracle.connect()
            dados = self._solicitar_dados(oracle)
            if dados is None:
                return None

            cliente, veiculo, retirada, devolucao, valor = dados

            # Evita cadastrar duas vezes uma locação com os mesmos dados.
            consulta = """
                SELECT ID FROM LOCACOES
                WHERE ID_CLIENTE = :id_cliente
                  AND ID_VEICULO = :id_veiculo
                  AND DATA_RETIRADA = :retirada
                  AND DATA_DEVOLUCAO = :devolucao
            """
            if not oracle.sqlToDataFrame(consulta, {
                "id_cliente": cliente.get_id(),
                "id_veiculo": veiculo.get_id(),
                "retirada": retirada,
                "devolucao": devolucao,
            }).empty:
                print("Já existe uma locação com esse cliente, veículo e período.")
                return None

            df_id = oracle.sqlToDataFrame(
                "SELECT LOCACOES_ID_SEQ.NEXTVAL AS ID FROM DUAL"
            )
            id_locacao = int(df_id.iloc[0]["id"])

            oracle.write(
                "INSERT INTO LOCACOES (ID, ID_CLIENTE, ID_VEICULO, "
                "DATA_RETIRADA, DATA_DEVOLUCAO, VALOR_TOTAL) "
                "VALUES (:id, :id_cliente, :id_veiculo, :retirada, "
                ":devolucao, :valor)",
                {"id": id_locacao,
                 "id_cliente": cliente.get_id(),
                 "id_veiculo": veiculo.get_id(),
                 "retirada": retirada,
                 "devolucao": devolucao,
                 "valor": valor},
            )

            nova_locacao = self._buscar_locacao(oracle, id_locacao)
            print("\nLocação inserida com sucesso!")
            if nova_locacao is not None:
                print(nova_locacao.to_string())
            return nova_locacao
        finally:
            oracle.close()

    def atualizar_locacao(self) -> Locacao:
        oracle = OracleQueries(can_write=True)
        try:
            oracle.connect()
            if self.listar_locacoes(oracle).empty:
                return None

            id_locacao = self._ler_id("ID da locação que deseja atualizar: ")
            if not self.verifica_existencia_locacao(oracle, id_locacao):
                print("Locação não encontrada.")
                return None

            dados = self._solicitar_dados(oracle)
            if dados is None:
                return None

            cliente, veiculo, retirada, devolucao, valor = dados
            oracle.write(
                "UPDATE LOCACOES SET ID_CLIENTE = :id_cliente, "
                "ID_VEICULO = :id_veiculo, DATA_RETIRADA = :retirada, "
                "DATA_DEVOLUCAO = :devolucao, VALOR_TOTAL = :valor "
                "WHERE ID = :id",
                {"id_cliente": cliente.get_id(),
                 "id_veiculo": veiculo.get_id(),
                 "retirada": retirada,
                 "devolucao": devolucao,
                 "valor": valor,
                 "id": id_locacao},
            )

            locacao_atualizada = self._buscar_locacao(oracle, id_locacao)
            print("\nLocação atualizada com sucesso!")
            if locacao_atualizada is not None:
                print(locacao_atualizada.to_string())
            return locacao_atualizada
        finally:
            oracle.close()

    def remover_locacao(self):
        oracle = OracleQueries(can_write=True)
        try:
            oracle.connect()
            if self.listar_locacoes(oracle).empty:
                return None

            id_locacao = self._ler_id("ID da locação que deseja remover: ")
            if not self.verifica_existencia_locacao(oracle, id_locacao):
                print("Locação não encontrada.")
                return None

            locacao = self._buscar_locacao(oracle, id_locacao)
            confirmacao = input(f"Confirma a remoção da locação {id_locacao}? (s/n): ")
            if confirmacao.strip().lower() != "s":
                print("Remoção cancelada.")
                return None

            oracle.write("DELETE FROM LOCACOES WHERE ID = :id", {"id": id_locacao})
            print("Locação removida com sucesso!")
            if locacao is not None:
                print(locacao.to_string())
            return locacao
        finally:
            oracle.close()

    # Nome alternativo, seguindo os controllers do projeto de exemplo.
    def excluir_locacao(self):
        return self.remover_locacao()
