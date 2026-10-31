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


## 0 - Elaboração dos prompts e orientação inicial

- Fonte: Claude (claude.ai)
- Data: 29/10/2026
- Quem fez:/ Hanry
- Prompt: Enviamos o PDF do edital do trabalho e pedimos ajuda para criar um prompt para gerar o código, além de orientações sobre GitHub, divisão de tarefas entre os cinco integrantes e passo a passo de uso do Git.
- O que o grupo fez com a resposta:** Recebemos um prompt base, um guia de Git/GitHub e uma sugestão de divisão de tarefas, que o grupo adotou. O prompt base foi usado com o tema Locação de Veículos (Prompt 1).

## Etapas 1 e 2: script SQL, diagrama e models

- Fonte: opencode (modelo exibido na ferramenta: Big Pickle)
- Data: 29/10/2026
- Quem fez: Hanry
- Prompt: Prompt base adaptado do projeto de exemplo (CRUD Python + Oracle), com o tema Locação de Veículos (tabelas CLIENTES, VEICULOS e LOCACOES), as regras do edital (sem ORM, menu, splash, relatórios, inserir/remover/atualizar) e a instrução de trabalhar em etapas, parando ao fim de cada uma. Foram executadas as etapas 1 (modelagem e script SQL) e 2 (models).
- O que o grupo fez com a resposta:** Os arquivos gerados (`scripts/create_tables.sql`, `docs/diagrama.mmd`, diagrama em PNG e os models de cliente, veículo e locação) foram adicionados ao repositório, e os models do projeto de exemplo foram removidos. As etapas seguintes foram divididas entre os integrantes. O opencode informou que não havia Python no ambiente Windows para validar o código, e a execução contra o Oracle não foi feita.

## Etapa 3: controller de locação

- Fonte: opencode
- Data: 29/10
- Quem fez:Hugo Gonçalves Rigo
- Prompt: Prompt enviado à IA:

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

Minha contribuição foi o desenvolvimento do controller responsável pelas operações de cadastro, consulta, atualização e exclusão das locações de veículos



## Etapa 4: controller de veículo

- Fonte: Gemini
- Data:30/10/2026
- Quem fez: Davi Nicolini Seschini
- Prompt enviado à IA:


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


## Etapa 5: controller de Cliente


- *Fonte:* Gemini (Google)
- *Data:* 30/10/2026
- *Quem fez:* Gustavo Reserva dos Santos
- *Prompt:* [Prompt enviado à IA:

"crie minha parte do codigo e depois faça o relatorio da minha parte"

Contexto fornecido:

Foram enviados os arquivos do projeto (guia.pdf, scripts/create_tables.sql e os arquivos de exemplo em src/model e src/controller), contendo as instruções do trabalho de Banco de Dados para adaptação ao tema de Locação de Veículos.

Parte desenvolvida:

Fiquei responsável pelo desenvolvimento do arquivo src/controller/controller_cliente.py, que realiza o gerenciamento completo dos clientes no sistema com banco de dados Oracle sem ORM.

Foram implementadas as seguintes funcionalidades:

Inserir cliente: cadastra um novo cliente utilizando a sequence cliente_id_seq, realizando validação prévia para evitar duplicidade de CPF e abrindo uma conexão dedicada por instrução.

Atualizar cliente: permite modificar os dados cadastrais de um cliente existente (exceto a chave primária), exibindo o registro atualizado após a alteração.

Remover cliente: exclui um cliente mediante confirmação, verificando previamente a integridade referencial (chave estrangeira na tabela LOCACOES). Caso existam locações vinculadas, o sistema avisa e pergunta se o usuário deseja remover também os registros filhos.

Listar clientes: apresenta os clientes cadastrados exibindo a chave primária (ID) e o campo descritivo (nome).

Verificar existência: consulta o banco de dados para identificar se um cliente está cadastrado tanto por ID quanto por CPF.

O que foi revisado e corrigido:

Durante a elaboração, foram conferidos estritamente os nomes das tabelas (clientes, locacoes), colunas e da sequence (cliente_id_seq) de acordo com o script SQL fornecido (scripts/create_tables.sql). As queries foram estruturadas em strings concatenadas, respeitando a proibição de uso de ORM e garantindo a abertura correta da conexão via módulo conexion.

O código utiliza comandos SQL diretos como SELECT, INSERT, UPDATE, DELETE e COUNT(1), integrando a biblioteca pandas para manipulação de DataFrames.

Foram realizadas verificações de sintaxe, estruturação e alinhamento com os padrões dos demais controllers do projeto.

Resultado:

O arquivo controller_cliente.py foi estruturado para a pasta src/controller/ do projeto. Realizei a validação dos métodos para integração no sistema de locação de veículos do grupo.

Minha contribuição foi o desenvolvimento completo do controller responsável pelas operações de cadastro, consulta, atualização, exclusão e regras de integridade referencial da entidade Clientes.]

## Prompt 6 - Relatórios, Menus e Tela Splash

- Fonte: Gemini (Google)
- Data: 30/10/2026
- Quem fez: Marcus 

[Nota: O prompt exato utilizado por Marcus não foi registrado no momento da execução. Caso lembre, preenchi abaixo com um formato padrão alinhado ao que foi pedido para estruturar a tela de splash, menus e relatórios]

"Crie os módulos de utilitários, splash screen com contagem de registros e menus em Python para o sistema de locação de veículos, além das consultas SQL com JOIN para a emissão de relatórios."

O que o grupo fez com a resposta: Os códigos gerados foram organizados nas pastas de utilitários, menus e relatórios. O integrante Marcus revisou a navegação do terminal, conferiu se as queries traziam os dados corretos e ajustou a formatação visual das telas.

## Etapa 7 -  Correção e integração final do projeto

- Fonte: Claude (claude.ai)
- Data:30/10/2026
- Quem fez: Hanry
- Prompt: Enviamos o projeto completo em .zip e pedimos que o código fosse corrigido e deixado pronto para a entrega, e que o registro de prompts fosse organizado.
-  O que o grupo fez com a resposta:** A IA devolveu o projeto com as seguintes alterações: `principal.py` reescrito para o tema (ainda era o do projeto de exemplo); controller de cliente corrigido (nome da sequence, método de escrita, nomes de colunas e validações); controller de veículo corrigido (nomes de colunas em minúsculas, validações); controller de locação com nomes de métodos padronizados; ajustes em `conexion/oracle_queries.py` (leitura do arquivo de credenciais e inicialização do cursor); relatórios, menus e splash revisados; remoção dos arquivos do projeto de exemplo; script e dados de exemplo (`scripts/inserting_samples.sql`); e novo README. O fluxo dos menus foi exercitado com um banco simulado (SQLite).

