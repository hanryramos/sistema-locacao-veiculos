from conexion.oracle_queries import OracleQueries
from model.veiculos import Veiculo


class ControllerVeiculo:

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
    def _ler_placa(mensagem: str) -> str:
        while True:
            placa = input(mensagem).strip().upper()
            if not placa:
                print("A placa não pode ficar vazia.")
                continue
            if len(placa) > 10:
                print("A placa deve ter no máximo 10 caracteres.")
                continue
            return placa

    @staticmethod
    def _ler_ano(mensagem: str) -> int:
        while True:
            try:
                ano = int(input(mensagem).strip())
                if 1900 <= ano <= 2100:
                    return ano
            except ValueError:
                pass
            print("Informe um ano entre 1900 e 2100.")

    @staticmethod
    def _ler_valor_diaria(mensagem: str) -> float:
        while True:
            try:
                valor = float(input(mensagem).strip().replace(",", "."))
                if 0 < valor <= 99999999.99:
                    return round(valor, 2)
            except ValueError:
                pass
            print("Informe um valor maior que zero (ex.: 150.00).")

    # ------------------------------------------------------------------
    # Consultas auxiliares
    # ------------------------------------------------------------------
    def _buscar_veiculo(self, oracle: OracleQueries, placa: str):
        df_veiculo = oracle.sqlToDataFrame(
            "SELECT ID, MODELO, PLACA, ANO, VALOR_DIARIA FROM VEICULOS "
            "WHERE PLACA = :placa",
            {"placa": placa},
        )
        if df_veiculo.empty:
            return None
        linha = df_veiculo.iloc[0]
        return Veiculo(int(linha["id"]), linha["modelo"], linha["placa"],
                       int(linha["ano"]), float(linha["valor_diaria"]))

    def verificar_existencia(self, oracle: OracleQueries, placa: str) -> bool:
        df_veiculo = oracle.sqlToDataFrame(
            "SELECT PLACA FROM VEICULOS WHERE PLACA = :placa",
            {"placa": placa},
        )
        return not df_veiculo.empty

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------
    def inserir(self) -> Veiculo:
        oracle = OracleQueries(can_write=True)
        try:
            oracle.connect()
            self._listar_dataframe(oracle)

            print("\n--- Cadastrar Novo Veículo ---")
            placa = self._ler_placa("Placa do veículo: ")

            if self.verificar_existencia(oracle, placa):
                print(f"O veículo com placa {placa} já existe no sistema.")
                return None

            modelo = self._ler_texto("Modelo do veículo: ", 100)
            ano = self._ler_ano("Ano do veículo: ")
            valor_diaria = self._ler_valor_diaria("Valor da diária: R$ ")

            oracle.write(
                "INSERT INTO VEICULOS (ID, MODELO, PLACA, ANO, VALOR_DIARIA) "
                "VALUES (VEICULOS_ID_SEQ.NEXTVAL, :modelo, :placa, :ano, :valor)",
                {"modelo": modelo, "placa": placa,
                 "ano": ano, "valor": valor_diaria},
            )

            novo_veiculo = self._buscar_veiculo(oracle, placa)
            print("\nVeículo cadastrado com sucesso!")
            if novo_veiculo is not None:
                print(novo_veiculo.to_string())
            return novo_veiculo
        finally:
            oracle.close()

    def atualizar(self) -> Veiculo:
        oracle = OracleQueries(can_write=True)
        try:
            oracle.connect()
            if self._listar_dataframe(oracle).empty:
                return None

            print("\n--- Atualizar Veículo ---")
            placa = self._ler_placa("Placa do veículo que deseja atualizar: ")

            if not self.verificar_existencia(oracle, placa):
                print(f"O veículo com placa {placa} não está cadastrado.")
                return None

            novo_modelo = self._ler_texto("Novo modelo: ", 100)
            novo_ano = self._ler_ano("Novo ano: ")
            novo_valor = self._ler_valor_diaria("Novo valor da diária: R$ ")

            oracle.write(
                "UPDATE VEICULOS SET MODELO = :modelo, ANO = :ano, "
                "VALOR_DIARIA = :valor WHERE PLACA = :placa",
                {"modelo": novo_modelo, "ano": novo_ano,
                 "valor": novo_valor, "placa": placa},
            )

            veiculo = self._buscar_veiculo(oracle, placa)
            print("\nVeículo atualizado com sucesso!")
            if veiculo is not None:
                print(veiculo.to_string())
            return veiculo
        finally:
            oracle.close()

    def remover(self):
        oracle = OracleQueries(can_write=True)
        try:
            oracle.connect()
            if self._listar_dataframe(oracle).empty:
                return None

            print("\n--- Remover Veículo ---")
            placa = self._ler_placa("Placa do veículo que deseja remover: ")

            if not self.verificar_existencia(oracle, placa):
                print(f"O veículo com placa {placa} não existe.")
                return None

            veiculo = self._buscar_veiculo(oracle, placa)
            if veiculo is None:
                print("Não foi possível carregar o veículo.")
                return None
            print(veiculo.to_string())

            df_locacoes = oracle.sqlToDataFrame(
                "SELECT COUNT(1) FROM LOCACOES WHERE ID_VEICULO = :id",
                {"id": veiculo.get_id()},
            )
            qtd_locacoes = int(df_locacoes.iloc[0, 0])

            if qtd_locacoes > 0:
                print(f"Atenção: este veículo possui {qtd_locacoes} locação(ões).")
                resposta = input(
                    "Deseja remover também as locações deste veículo? (s/n): "
                )
                if resposta.strip().lower() != "s":
                    print("Operação cancelada para preservar as locações.")
                    return None
                oracle.write(
                    "DELETE FROM LOCACOES WHERE ID_VEICULO = :id",
                    {"id": veiculo.get_id()},
                )
            else:
                confirmacao = input(
                    f"Tem certeza que deseja excluir o veículo {placa}? (s/n): "
                )
                if confirmacao.strip().lower() != "s":
                    print("Operação cancelada.")
                    return None

            oracle.write(
                "DELETE FROM VEICULOS WHERE ID = :id",
                {"id": veiculo.get_id()},
            )
            print("Veículo removido com sucesso!")
            return veiculo
        finally:
            oracle.close()

    def _listar_dataframe(self, oracle: OracleQueries):
        df_veiculos = oracle.sqlToDataFrame(
            "SELECT ID, PLACA, MODELO, ANO, VALOR_DIARIA FROM VEICULOS ORDER BY ID"
        )
        print("\n--- Lista de Veículos ---")
        if df_veiculos.empty:
            print("Nenhum veículo cadastrado.")
        else:
            for _, linha in df_veiculos.iterrows():
                print(f"ID: {linha['id']} | Placa: {linha['placa']} | "
                      f"Modelo: {linha['modelo']} | Ano: {linha['ano']} | "
                      f"Diária: R$ {linha['valor_diaria']}")
        return df_veiculos

    def listar(self):
        oracle = OracleQueries()
        try:
            oracle.connect()
            return self._listar_dataframe(oracle)
        finally:
            oracle.close()
