# Sistema de Locação de Veículos

Sistema de CRUD em Python com banco Oracle, desenvolvido para a disciplina de
Banco de Dados. O sistema possui três entidades:

- **CLIENTES**: id, nome, cpf, telefone
- **VEICULOS**: id, modelo, placa, ano, valor_diaria
- **LOCACOES**: id, id_cliente, id_veiculo, data_retirada, data_devolucao, valor_total

O sistema oferece:

- Tela inicial com a quantidade de registros de cada tabela
- Inserir, atualizar, listar e remover clientes, veículos e locações
- Relatório de total arrecadado por modelo de veículo (GROUP BY)
- Relatório de locações com os dados dos clientes e veículos (JOIN)

## Estrutura

- `scripts/create_tables.sql`: criação das tabelas, constraints, sequences e FKs
- `docs/diagrama.mmd`: diagrama relacional (formato Mermaid)
- `src/principal.py`: menu principal do sistema
- `src/controller/`: controllers de cliente, veículo e locação
- `src/model/`: classes de modelo
- `src/reports/relatorios.py`: execução dos relatórios
- `src/sql/`: consultas SQL dos relatórios
- `src/utils/`: menus, limpeza de tela e tela inicial
- `src/conexion/oracle_queries.py`: acesso ao Oracle (consultas, DML e DDL)

## Requisitos

- Python 3.8 ou superior (recomendado 3.10)
- Oracle Database XE (ou outra versão) com usuário e senha válidos
- Oracle Instant Client, quando o `cx_Oracle` for usado em modo thick

## Configuração do banco

1. Edite `src/conexion/passphrase/authentication.oracle` com o usuário e a
   senha do banco, separados por vírgula e **sem espaços**:

   ```
   usuario,senha
   ```

2. Crie as tabelas. Você pode executar `scripts/create_tables.sql` no SQL
   Developer/SQLcl **ou** rodar:

   ```shell
   python src/create_tables_and_records.py
   ```

   Na primeira execução, os `DROP` do início do script podem gerar
   `ORA-00942`/`ORA-02289`; o script Python ignora esses erros de propósito.

3. Teste a conexão:

   ```shell
   python src/test.py
   ```

## Instalação das dependências

```shell
pip install -r src/requirements.txt
```

> Em Python 3.11+ o `cx-Oracle` não possui instalação. Nesse caso o
> `requirements.txt` instala o `oracledb`, que é usado automaticamente pelo
> `oracle_queries.py` e dispensa o Instant Client no modo thin.

## Execução

```shell
python src/principal.py
```

Também é possível entrar em `src` e executar `python principal.py`.

## Conexão com o Oracle em container

O sistema tenta primeiro a conexão pelo SID `XE`. Se ela falhar, tenta
automaticamente pelo service name `XEPDB1` (usado em containers Oracle XE).
Se o seu banco usar outro serviço ou outra porta, ajuste `host`, `port`,
`sid` e `service_name` em `src/conexion/oracle_queries.py`.

## Observações

- Os comandos SQL usam variáveis de bind (`:nome`), evitando problemas com
  apóstrofos e SQL injection.
- As datas são lidas no formato `DD/MM/AAAA`.
- A remoção de cliente/veículo com locações vinculadas pede confirmação antes
  de apagar as locações, preservando a integridade referencial.
