from datetime import datetime

from conexion.oracle_queries import OracleQueries
from model.clientes import Cliente
from model.veiculos import Veiculo
from model.locacoes import Locacao


class Controller_Locacao:
    def __init__(self):
        pass

    # Exibe as locações com o cliente e o modelo do veículo.
    def listar_locacoes(self, oracle: OracleQueries = None, need_connect: bool = False):
        if oracle is None:
            oracle = OracleQueries()
            oracle.connect()
        elif need_connect:
            oracle.connect()

        query = """
            SELECT l.ID, c.NOME AS CLIENTE, v.MODELO AS VEICULO,
                   l.DATA_RETIRADA, l.DATA_DEVOLUCAO, l.VALOR_TOTAL
            FROM LOCACOES l
            JOIN CLIENTES c ON c.ID = l.ID_CLIENTE
            JOIN VEICULOS v ON v.ID = l.ID_VEICULO
            ORDER BY l.ID
        """
        df_locacoes = oracle.sqlToDataFrame(query)
        if df_locacoes.empty:
            print("Nenhuma locação cadastrada.")
        else:
            print(df_locacoes.to_string(index=False))
        return df_locacoes

    # Retorna True quando o ID da locação já está cadastrado.
    def verifica_existencia_locacao(self, oracle: OracleQueries, id_locacao: int) -> bool:
        query = f"SELECT ID FROM LOCACOES WHERE ID = {int(id_locacao)}"
        return not oracle.sqlToDataFrame(query).empty

    def verificar_existencia(self, oracle: OracleQueries, id_locacao: int) -> bool:
        return self.verifica_existencia_locacao(oracle, id_locacao)

    def _ler_id(self, mensagem: str) -> int:
        while True:
            try:
                id_registro = int(input(mensagem))
                if id_registro > 0:
                    return id_registro
            except ValueError:
                pass
            print("Digite um ID inteiro maior que zero.")

    def _ler_data(self, mensagem: str):
        while True:
            try:
                return datetime.strptime(input(mensagem), "%d/%m/%Y").date()
            except ValueError:
                print("Data inválida. Use o formato DD/MM/AAAA.")

    def _ler_valor_total(self) -> float:
        while True:
            try:
                valor = float(input("Valor total: R$ ").replace(",", "."))
                if 0 <= valor <= 99999999.99:
                    return round(valor, 2)
            except ValueError:
                pass
            print("Informe um valor entre 0 e 99.999.999,99.")

    def _buscar_cliente(self, oracle: OracleQueries, id_cliente: int):
        query = ("SELECT ID, NOME, CPF, TELEFONE FROM CLIENTES "
                 f"WHERE ID = {id_cliente}")
        df_cliente = oracle.sqlToDataFrame(query)
        if df_cliente.empty:
            return None
        linha = df_cliente.iloc[0]
        return Cliente(int(linha["id"]), linha["nome"], linha["cpf"], linha["telefone"])

    def _buscar_veiculo(self, oracle: OracleQueries, id_veiculo: int):
        query = ("SELECT ID, MODELO, PLACA, ANO, VALOR_DIARIA FROM VEICULOS "
                 f"WHERE ID = {id_veiculo}")
        df_veiculo = oracle.sqlToDataFrame(query)
        if df_veiculo.empty:
            return None
        linha = df_veiculo.iloc[0]
        return Veiculo(int(linha["id"]), linha["modelo"], linha["placa"],
                       int(linha["ano"]), float(linha["valor_diaria"]))

    def _buscar_locacao(self, oracle: OracleQueries, id_locacao: int):
        query = f"""
            SELECT l.ID AS ID_LOCACAO, l.DATA_RETIRADA, l.DATA_DEVOLUCAO,
                   l.VALOR_TOTAL, c.ID AS ID_CLIENTE, c.NOME, c.CPF, c.TELEFONE,
                   v.ID AS ID_VEICULO, v.MODELO, v.PLACA, v.ANO, v.VALOR_DIARIA
            FROM LOCACOES l
            JOIN CLIENTES c ON c.ID = l.ID_CLIENTE
            JOIN VEICULOS v ON v.ID = l.ID_VEICULO
            WHERE l.ID = {id_locacao}
        """
        df_locacao = oracle.sqlToDataFrame(query)
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

    # Solicita os campos que podem ser inseridos ou atualizados.
    def _solicitar_dados(self, oracle: OracleQueries):
        print("\nClientes disponíveis:")
        print(oracle.sqlToDataFrame("SELECT ID, NOME FROM CLIENTES ORDER BY NOME")
              .to_string(index=False))
        id_cliente = self._ler_id("ID do cliente: ")
        cliente = self._buscar_cliente(oracle, id_cliente)
        if cliente is None:
            print("Cliente não encontrado. Operação cancelada.")
            return None

        print("\nVeículos disponíveis:")
        print(oracle.sqlToDataFrame("SELECT ID, MODELO, PLACA FROM VEICULOS ORDER BY MODELO")
              .to_string(index=False))
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

    def inserir_locacao(self) -> Locacao:
        oracle = OracleQueries(can_write=True)
        oracle.connect()
        dados = self._solicitar_dados(oracle)
        if dados is None:
            return None

        cliente, veiculo, retirada, devolucao, valor = dados
        data_retirada = retirada.strftime("%Y-%m-%d")
        data_devolucao = devolucao.strftime("%Y-%m-%d")

        # Evita cadastrar duas vezes uma locação com os mesmos dados principais.
        consulta = f"""
            SELECT ID FROM LOCACOES
            WHERE ID_CLIENTE = {cliente.get_id()}
              AND ID_VEICULO = {veiculo.get_id()}
              AND DATA_RETIRADA = TO_DATE('{data_retirada}', 'YYYY-MM-DD')
              AND DATA_DEVOLUCAO = TO_DATE('{data_devolucao}', 'YYYY-MM-DD')
        """
        if not oracle.sqlToDataFrame(consulta).empty:
            print("Já existe uma locação com esse cliente, veículo e período.")
            return None

        df_id = oracle.sqlToDataFrame("SELECT LOCACOES_ID_SEQ.NEXTVAL AS ID FROM DUAL")
        id_locacao = int(df_id.iloc[0]["id"])
        if self.verifica_existencia_locacao(oracle, id_locacao):
            print("O ID da locação já existe. Operação cancelada.")
            return None

        query = f"""
            INSERT INTO LOCACOES
                (ID, ID_CLIENTE, ID_VEICULO, DATA_RETIRADA, DATA_DEVOLUCAO, VALOR_TOTAL)
            VALUES
                ({id_locacao}, {cliente.get_id()}, {veiculo.get_id()},
                 TO_DATE('{data_retirada}', 'YYYY-MM-DD'),
                 TO_DATE('{data_devolucao}', 'YYYY-MM-DD'), {valor:.2f})
        """
        oracle.write(query)
        nova_locacao = self._buscar_locacao(oracle, id_locacao)
        print("Locação inserida com sucesso!")
        print(nova_locacao.to_string())
        return nova_locacao

    def atualizar_locacao(self) -> Locacao:
        oracle = OracleQueries(can_write=True)
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
        query = f"""
            UPDATE LOCACOES
            SET ID_CLIENTE = {cliente.get_id()},
                ID_VEICULO = {veiculo.get_id()},
                DATA_RETIRADA = TO_DATE('{retirada:%Y-%m-%d}', 'YYYY-MM-DD'),
                DATA_DEVOLUCAO = TO_DATE('{devolucao:%Y-%m-%d}', 'YYYY-MM-DD'),
                VALOR_TOTAL = {valor:.2f}
            WHERE ID = {id_locacao}
        """
        oracle.write(query)
        locacao_atualizada = self._buscar_locacao(oracle, id_locacao)
        print("Locação atualizada com sucesso!")
        print(locacao_atualizada.to_string())
        return locacao_atualizada

    def remover_locacao(self):
        oracle = OracleQueries(can_write=True)
        oracle.connect()
        if self.listar_locacoes(oracle).empty:
            return None

        id_locacao = self._ler_id("ID da locação que deseja remover: ")
        if not self.verifica_existencia_locacao(oracle, id_locacao):
            print("Locação não encontrada.")
            return None

        locacao = self._buscar_locacao(oracle, id_locacao)
        confirmacao = input(f"Confirma a remoção da locação {id_locacao}? (S/N): ")
        if confirmacao.strip().lower() != "s":
            print("Remoção cancelada.")
            return None

        oracle.write(f"DELETE FROM LOCACOES WHERE ID = {id_locacao}")
        print("Locação removida com sucesso!")
        print(locacao.to_string())
        return locacao

    # Nome alternativo, seguindo os controllers do projeto de exemplo.
    def excluir_locacao(self):
        return self.remover_locacao()
