from pathlib import Path

from conexion.oracle_queries import OracleQueries


def run():
    """Executa o script scripts/create_tables.sql no banco configurado."""
    sql_path = Path(__file__).resolve().parents[1] / "scripts" / "create_tables.sql"
    comandos = sql_path.read_text(encoding="utf-8")

    oracle = OracleQueries(can_write=True)
    try:
        oracle.connect()
        print("Criando tabelas, sequences e relacionamentos...")

        for comando in comandos.split(";"):
            comando = comando.strip()
            if not comando:
                continue
            try:
                oracle.executeDDL(comando)
                print("OK")
            except Exception as erro:
                mensagem = str(erro)
                # Na primeira execução os DROP não encontram os objetos.
                if "ORA-00942" in mensagem or "ORA-02289" in mensagem:
                    print("(objeto ainda não existia, ignorado)")
                else:
                    raise

        print("Banco criado com sucesso!")
    finally:
        oracle.close()


if __name__ == '__main__':
    run()
