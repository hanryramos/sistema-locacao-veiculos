"""Textos e configurações dos menus do sistema."""

MENU_PRINCIPAL = """========== SISTEMA DE LOCAÇÃO DE VEÍCULOS ==========
Menu Principal
1 - Relatórios
2 - Inserir
3 - Remover
4 - Atualizar
0 - Sair
"""

MENU_RELATORIOS = """========== RELATÓRIOS ==========
1 - Total arrecadado por modelo de veículo (GROUP BY)
2 - Locações com dados dos clientes e veículos (JOIN)
0 - Voltar
"""

MENU_ENTIDADES = """========== ENTIDADES ==========
1 - Clientes
2 - Veículos
3 - Locações
0 - Voltar
"""

# Consulta usada pela tela inicial para contar os registros de cada tabela.
QUERY_COUNT = "SELECT COUNT(1) AS total_{tabela} FROM {tabela}"


def clear_console(wait_time: int = 1):
    """Limpa o terminal após o tempo informado."""
    import os
    from time import sleep

    if wait_time > 0:
        sleep(wait_time)
    os.system("clear")
