from pathlib import Path

from conexion.oracle_queries import OracleQueries


class Relatorio:
    """Executa e apresenta os relatórios do sistema de locação."""

    def __init__(self):
        # Localiza os arquivos SQL a partir da pasta deste arquivo.
        pasta_sql = Path(__file__).resolve().parents[1] / "sql"

        self.query_arrecadacao_por_modelo = (
            pasta_sql / "relatorio_arrecadacao_por_modelo.sql"
        ).read_text(encoding="utf-8")

        self.query_locacoes_detalhado = (
            pasta_sql / "relatorio_locacoes_detalhado.sql"
        ).read_text(encoding="utf-8")

    def _exibir_relatorio(self, consulta, descricao):
        """Abre a conexão, executa a consulta e mostra o resultado."""
        oracle = OracleQueries()
        try:
            oracle.connect()
            resultado = oracle.sqlToDataFrame(consulta)
            if resultado.empty:
                print("\\nNenhum registro encontrado.")
            else:
                print(resultado.to_string(index=False))
        finally:
            # Fecha a conexão mesmo se ocorrer algum erro na consulta.
            try:
                oracle.close()
            except Exception:
                pass

        input(f"\\nPressione Enter para sair de {descricao}...")

    def get_relatorio_arrecadacao_por_modelo(self):
        self._exibir_relatorio(
            self.query_arrecadacao_por_modelo,
            "Relatório de Arrecadação por Modelo"
        )

    def get_relatorio_locacoes_detalhado(self):
        self._exibir_relatorio(
            self.query_locacoes_detalhado,
            "Relatório de Locações"
        )

    # Métodos com nomes curtos para facilitar a chamada pelo principal.py.
    def get_relatorio_1(self):
        self.get_relatorio_arrecadacao_por_modelo()

    def get_relatorio_2(self):
        self.get_relatorio_locacoes_detalhado()
