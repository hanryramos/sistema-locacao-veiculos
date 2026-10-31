from conexion.oracle_queries import OracleQueries


def run():
    """Testa a conexão com o Oracle configurado em authentication.oracle."""
    oracle = OracleQueries()
    try:
        oracle.connect()
        resultado = oracle.sqlToDataFrame("SELECT 1 AS OK FROM DUAL")
        print("Conexão com o Oracle realizada com sucesso!")
        print(resultado.to_string(index=False))
    finally:
        oracle.close()


if __name__ == '__main__':
    run()
