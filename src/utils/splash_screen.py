from conexion.oracle_queries import OracleQueries
from utils import config


class SplashScreen:
    """Apresenta informações do trabalho e a quantidade de registros."""

    def __init__(self):
        self.tabelas = ("clientes", "veiculos", "locacoes")
        self.created_by = [
            "Hanry",
            "Gustavo",
            "Davi Nicolini",
            "Hugo Rigo",
            "Marcus",
        ]
        self.professor = "Howard Roatti"
        self.disciplina = "Banco de Dados"
        self.semestre = "2026/2"
        self.nome_sistema = "SISTEMA DE LOCAÇÃO DE VEÍCULOS"

    def _get_total(self, tabela: str):
        """Retorna a quantidade de registros de uma tabela."""
        oracle = OracleQueries()
        try:
            oracle.connect()
            consulta = config.QUERY_COUNT.format(tabela=tabela)
            resultado = oracle.sqlToDataFrame(consulta)
            coluna_total = f"total_{tabela}"
            return int(resultado[coluna_total].values[0])
        finally:
            try:
                oracle.close()
            except Exception:
                pass

    def get_total_clientes(self):
        return self._get_total("clientes")

    def get_total_veiculos(self):
        return self._get_total("veiculos")

    def get_total_locacoes(self):
        return self._get_total("locacoes")

    def get_updated_screen(self):
        # Uma falha de conexão não deve esconder as informações do sistema.
        totais = {}
        for tabela in self.tabelas:
            try:
                totais[tabela] = str(self._get_total(tabela))
            except Exception:
                totais[tabela] = "indisponível"

        integrantes = ", ".join(self.created_by)
        return f"""
+--------------------------------------------------------------+
|                 {self.nome_sistema:<36} |
+--------------------------------------------------------------+
| TOTAL DE REGISTROS                                            |
|   CLIENTES:  {totais['clientes']:<10}                                  |
|   VEÍCULOS:  {totais['veiculos']:<10}                                  |
|   LOCAÇÕES:  {totais['locacoes']:<10}                                  |
+--------------------------------------------------------------+
| INTEGRANTES: {integrantes}
| DISCIPLINA:  {self.disciplina}
| SEMESTRE:    {self.semestre}
| PROFESSOR:   {self.professor}
+--------------------------------------------------------------+
"""
