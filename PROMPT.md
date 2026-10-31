# PROMPTS.md

Registro do uso de ferramentas de IA neste projeto, conforme o edital.

- Disciplina:Banco de Dados (2026/2)
- Professor: Howard Roatti
- Projeto: Sistema de Locação de Veículos
- Integrantes: Hanry, Hugo, Davi Nicolini, Marcus, Gustavo Reserva  

## Ferramentas de IA utilizadas

| Ferramenta | Para que usamos |
| Claude (claude.ai) | Ajuda para elaborar o prompt do opencode e orientações de uso do Git/GitHub |
| opencode ([modelo/provedor usado]) | Adaptação do projeto de exemplo e geração do código do sistema |

> Preencha tudo que estiver entre colchetes `[ ]` com o que de fato aconteceu.
> Apague este aviso antes de entregar.

---


## Etapa 1: modelagem e script SQL

- **Fonte:** opencode ([modelo/provedor])
- **Data:** [data]
- **Quem fez:** [nome]
- **Prompt:** [texto exato que foi enviado]
- **O que o grupo fez com a resposta:** [ex.: conferimos tipos e chaves, rodamos o script na VM, ajustamos X]

## Etapa 2: classes de model

- **Fonte:** opencode ([modelo/provedor])
- **Data:** [data]
- **Quem fez:** [nome]
- **Prompt:** [texto exato que foi enviado]
- **O que o grupo fez com a resposta:** [...]

## Etapa 3: controllers

- **Fonte:** opencode ([modelo/provedor])
- **Data:** [29/10]
- **Quem fez:** [Hugo Gonçalves Rigo]
- **Prompt:** [Prompt enviado à IA:

"crie minha parte do codigo e depois faça o relatorio da minha parte"

Contexto fornecido:

Foram enviados os arquivos guia.pdf e relatotio.md, contendo as instruções do trabalho, a divisão das tarefas e o modelo de relatório.

Parte desenvolvida:

Fiquei responsável pelo desenvolvimento do arquivo src/controller/controller_locacao.py, que realiza o gerenciamento das locações de veículos no sistema.

Foram implementadas as seguintes funcionalidades:

Inserir locação: cadastra uma nova locação, verificando a existência do cliente e do veículo.

Atualizar locação: permite modificar os dados de uma locação existente.

Remover locação: exclui uma locação mediante confirmação do usuário.

Listar locações: apresenta as locações cadastradas, mostrando o cliente e o veículo.

Verificar existência: consulta o banco para identificar se uma locação está cadastrada.

O que foi revisado e corrigido:

Durante a elaboração, foram conferidos os nomes das tabelas, colunas e sequence com o script SQL do projeto. Também foram considerados os models existentes e o padrão de conexão com o banco Oracle.

O código utiliza comandos SQL como SELECT, INSERT, UPDATE e DELETE, além de JOIN e TO_DATE.

Foram realizadas verificações de sintaxe e testes simulados durante a geração do código. Não foram realizados testes no banco Oracle real.

Resultado:

O arquivo controller_locacao.py foi adicionado à pasta src/controller do projeto. Realizei o commit e o push para o repositório do grupo no GitHub.

Minha contribuição foi o desenvolvimento do controller responsável pelas operações de cadastro, consulta, atualização e exclusão das locações de veículos.]

- **O que o grupo fez com a resposta:** [...]



- **Fonte:** Gemini ([modelo/provedor])
- **Data:** 30/10/2026
- **Quem fez:** Davi Nicolini Seschini
- **Prompt enviado à IA:**


Crie a classe ControllerVeiculo no arquivo src/controller/controller_veiculo.py para um sistema em Python que utiliza banco de dados Oracle sem ORM. Faça um relatório da minha parte.

Requisitos funcionais do ControllerVeiculo:
1. Método inserir():
   - Solicita a placa do veículo (chave alternativa/única).
   - Verifica se a placa já existe através do método auxiliar verificar_existencia(). Se existir, exibe mensagem e cancela a inserção.
   - Solicita os dados: modelo, ano e valor_diaria.
   - Executa o INSERT na tabela VEICULOS usando a sequence VEICULOS_ID_SEQ.NEXTVAL para o campo ID (Primary Key).
   - Recupera os dados do registro recém-criado, instancia e retorna o objeto Veiculo (de model.veiculos), exibindo a confirmação com to_string().

2. Método atualizar():
   - Solicita a placa do veículo alvo e verifica se ele existe no banco. Se não existir, avisa e encerra.
   - Solicita os novos valores para modelo, ano e valor_diaria (mantendo o ID e a PLACA inalterados).
   - Executa o UPDATE no banco e exibe o registro atualizado.

3. Método remover():
   - Solicita a placa do veículo e verifica se ele existe.
   - Recupera a PK (ID) do veículo.
   - Verifica a integridade referencial com a tabela LOCACOES (checa se existem registros com ID_VEICULO igual ao ID do veículo).
   - Se existirem locações vinculadas, exibe um aviso e pergunta se o usuário deseja remover também todas as locações do veículo (S/N). Se o usuário confirmar ('S'), remove primeiro os registros em LOCACOES e depois o registro em VEICULOS. Caso contrário, cancela a operação.
   - Se não houver locações vinculadas, pede confirmação padrão e remove o veículo.

4. Método listar():
   - Executa um SELECT trazendo os campos ID, PLACA e MODELO da tabela VEICULOS e exibe o DataFrame do pandas (ou mensagem de que está vazio).

5. Método auxiliar verificar_existencia(oracle, placa):
   - Executa uma consulta por PLACA na tabela VEICULOS e retorna True se encontrar registro ou False caso contrário.

Diretrizes técnicas:
- Utilizar a classe OracleQueries (de conexion.oracle_queries) para execução de SQL e conversão para DataFrame via sqlToDataFrame().
- Não utilizar ORM; apenas comandos SQL diretos.
- Respeitar estritamente os nomes de tabelas, colunas e sequences definidos em scripts/create_tables.sql.
- Código simples, comentários curtos em português.


Parte desenvolvida:

Fiquei responsável pelo desenvolvimento do arquivo src/controller/controller_veiculo.py, que realiza o gerenciamento dos veículos no sistema.

Foram implementadas as seguintes funcionalidades:

Inserir veículo: cadastra um novo veículo, solicitando a placa, modelo, ano e valor da diária. O método consulta a existência prévia da placa para evitar duplicidades e utiliza a sequence VEICULOS_ID_SEQ.NEXTVAL no Oracle para a geração da chave primária (ID), retornando o objeto Veiculo instanciado e exibindo a confirmação via to_string().

Atualizar veículo: permite alterar o modelo, o ano e o valor da diária de um veículo cadastrado a partir da consulta pela placa, mantendo inalteradas a chave primária e a própria placa.

Remover veículo: realiza a exclusão do veículo após consulta pela placa e obtenção do seu ID. Para garantir a integridade referencial, o método verifica se o ID do veículo consta como Chave Estrangeira na tabela LOCACOES. Se houver vínculos, alerta o usuário e possibilita a exclusão prévia em cascata das locações associadas antes de deletar o registro pai em VEICULOS.

Listar veículos: realiza um SELECT dos campos ID, PLACA e MODELO da tabela VEICULOS e exibe os dados cadastrados em tela através de um DataFrame do pandas (ou mensagem informando caso a tabela esteja vazia).

Verificar existência: função auxiliar que realiza uma consulta pela chave alternativa (PLACA) na tabela VEICULOS e retorna um boolean indicando se o veículo já se encontra cadastrado.

O que foi revisado e corrigido:

Durante o desenvolvimento, validou-se a correspondência exata dos nomes da tabela (VEICULOS), colunas (ID, MODELO, PLACA, ANO, VALOR_DIARIA) e da sequence (VEICULOS_ID_SEQ) com o script SQL do projeto. Ajustaram-se as conexões com o banco utilizando a classe OracleQueries (com can_write=True nos métodos de escrita) e garantiu-se a conversão e leitura direta dos dados via sqlToDataFrame().

O código utiliza comandos SQL nativos como SELECT, INSERT, UPDATE e DELETE, sem a utilização de ORM.

Foram realizadas verificações de sintaxe, validações da lógica de tratamento de FK (remoção em cascata) e testes de fluxo no controller.

Resultado:

O arquivo controller_veiculo.py foi finalizado e integrado à pasta src/controller do repositório. O commit e o push foram realizados com sucesso no GitHub do grupo.

Minha contribuição foi o desenvolvimento do controller responsável pelo CRUD completo e pelo controle de integridade referencial dos veículos no sistema.

- **O que o grupo fez com a resposta:** [...]




## Etapa 4: relatórios

- **Fonte:** opencode ([modelo/provedor])
- **Data:** [data]
- **Quem fez:** [nome]
- **Prompt:** [texto exato que foi enviado]
- **O que o grupo fez com a resposta:** [...]

## Etapa 5: utils, splash screen e menus

- **Fonte:** opencode ([modelo/provedor])
- **Data:** [data]
- **Quem fez:** [nome]
- **Prompt:** [texto exato que foi enviado]
- **O que o grupo fez com a resposta:** [...]

