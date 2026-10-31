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
            print(f"\n===== {descricao} =====")
            if resultado.empty:
                print("Nenhum registro encontrado.")
            else:
                print(resultado.to_string(index=False))
        except Exception as erro:
            print(f"\nNão foi possível gerar o relatório: {erro}")
        finally:
            try:
                oracle.close()
            except Exception:
                pass

        input("\nPressione Enter para voltar...")

    def get_relatorio_arrecadacao_por_modelo(self):
        self._exibir_relatorio(
            self.query_arrecadacao_por_modelo,
            "Total arrecadado por modelo de veículo"
        )

    def get_relatorio_locacoes_detalhado(self):
        self._exibir_relatorio(
            self.query_locacoes_detalhado,
            "Locações com dados dos clientes e veículos"
        )
