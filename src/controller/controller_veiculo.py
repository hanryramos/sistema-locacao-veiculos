import pandas as pd
from model.veiculos import Veiculo
from conexion.oracle_queries import OracleQueries

class ControllerVeiculo:
    def __init__(self):
        pass

    def inserir(self) -> Veiculo:
        # Abre a conexão com permissão de escrita
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        placa = input("Informe a placa do veículo (Nova): ")

        # Só permite inserir se o veículo NÃO existir
        if self.verificar_existencia(oracle, placa):
            print(f"O veículo com placa {placa} já existe no sistema.")
            return None

        modelo = input("Informe o modelo do veículo: ")
        ano = input("Informe o ano do veículo: ")
        valor_diaria = input("Informe o valor da diária: ")

        # SQL usando a sequence VEICULOS_ID_SEQ
        sql_insert = f"INSERT INTO VEICULOS (ID, MODELO, PLACA, ANO, VALOR_DIARIA) VALUES (VEICULOS_ID_SEQ.NEXTVAL, '{modelo}', '{placa}', {ano}, {valor_diaria})"
        oracle.write(sql_insert)

        # Recupera os dados inseridos
        df_veiculo = oracle.sqlToDataFrame(f"SELECT ID, MODELO, PLACA, ANO, VALOR_DIARIA FROM VEICULOS WHERE PLACA = '{placa}'")
        novo_veiculo = Veiculo(
            df_veiculo["ID"].values[0],
            df_veiculo["MODELO"].values[0],
            df_veiculo["PLACA"].values[0],
            df_veiculo["ANO"].values[0],
            df_veiculo["VALOR_DIARIA"].values[0]
        )
        
        print("Veículo cadastrado com sucesso:")
        print(novo_veiculo.to_string())
        return novo_veiculo

    def atualizar(self) -> Veiculo:
        # Abre a conexão
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        placa = input("Informe a placa do veículo que deseja atualizar: ")

        # Verifica se o veículo alvo existe
        if not self.verificar_existencia(oracle, placa):
            print(f"O veículo com placa {placa} não está cadastrado.")
            return None

        novo_modelo = input("Novo Modelo: ")
        novo_ano = input("Novo Ano: ")
        novo_valor_diaria = input("Novo Valor da Diária: ")

        # Atualiza os dados (exceto a PK e a própria placa)
        sql_update = f"UPDATE VEICULOS SET MODELO = '{novo_modelo}', ANO = {novo_ano}, VALOR_DIARIA = {novo_valor_diaria} WHERE PLACA = '{placa}'"
        oracle.write(sql_update)

        # Exibe o registro atualizado
        df_veiculo = oracle.sqlToDataFrame(f"SELECT ID, MODELO, PLACA, ANO, VALOR_DIARIA FROM VEICULOS WHERE PLACA = '{placa}'")
        veiculo_atualizado = Veiculo(
            df_veiculo["ID"].values[0],
            df_veiculo["MODELO"].values[0],
            df_veiculo["PLACA"].values[0],
            df_veiculo["ANO"].values[0],
            df_veiculo["VALOR_DIARIA"].values[0]
        )
        
        print("Veículo atualizado com sucesso:")
        print(veiculo_atualizado.to_string())
        return veiculo_atualizado

    def remover(self):
        # Abre a conexão
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        placa = input("Informe a placa do veículo que deseja remover: ")

        if not self.verificar_existencia(oracle, placa):
            print(f"O veículo com placa {placa} não existe.")
            return None

        # Pega a PK (ID) do veículo para verificar a integridade da FK em locações
        df_veiculo = oracle.sqlToDataFrame(f"SELECT ID FROM VEICULOS WHERE PLACA = '{placa}'")
        id_veiculo = int(df_veiculo["ID"].values[0])

        # Verifica se o veículo aparece como Chave Estrangeira em LOCACOES
        df_locacoes = oracle.sqlToDataFrame(f"SELECT ID FROM LOCACOES WHERE ID_VEICULO = {id_veiculo}")

        if not df_locacoes.empty:
            print("Aviso: Este veículo possui locações vinculadas e não pode ser excluído diretamente.")
            confirma = input("Deseja remover também TODAS as locações deste veículo antes de excluí-lo? (S/N): ").strip().upper()
            if confirma == 'S':
                # Remove registros filhos para preservar a integridade
                oracle.write(f"DELETE FROM LOCACOES WHERE ID_VEICULO = {id_veiculo}")
            else:
                print("Operação de remoção cancelada.")
                return None
        else:
            confirma = input("Tem certeza que deseja excluir este veículo? (S/N): ").strip().upper()
            if confirma != 'S':
                print("Operação de remoção cancelada.")
                return None

        # Exclui o registro pai
        oracle.write(f"DELETE FROM VEICULOS WHERE ID = {id_veiculo}")
        print("Veículo removido com sucesso!")

    def listar(self):
        # Abre a conexão
        oracle = OracleQueries()
        oracle.connect()

        # Lista os veículos trazendo a PK e os campos descritivos
        df_veiculos = oracle.sqlToDataFrame("SELECT ID, PLACA, MODELO FROM VEICULOS")
        if df_veiculos.empty:
            print("Nenhum veículo cadastrado no momento.")
        else:
            print(df_veiculos)

    def verificar_existencia(self, oracle: OracleQueries, placa: str) -> bool:
        # Consulta simples usando a placa
        df_veiculo = oracle.sqlToDataFrame(f"SELECT PLACA FROM VEICULOS WHERE PLACA = '{placa}'")
        return not df_veiculo.empty