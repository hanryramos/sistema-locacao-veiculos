# PROMPTS.md

Registro do uso de ferramentas de IA neste projeto, conforme o edital (Observações Importantes, item 5).

- **Disciplina:** Banco de Dados (2026/2)
- **Professor:** Howard Roatti
- **Projeto:** [nome do sistema do grupo]
- **Integrantes:** [nome 1], [nome 2], [nome 3], [nome 4], [nome 5]

## Ferramentas de IA utilizadas

| Ferramenta | Para que usamos |
|---|---|
| Claude (claude.ai) | Ajuda para elaborar o prompt do opencode e orientações de uso do Git/GitHub |
| opencode ([modelo/provedor usado]) | Adaptação do projeto de exemplo e geração do código do sistema |

> Preencha tudo que estiver entre colchetes `[ ]` com o que de fato aconteceu.
> Apague este aviso antes de entregar.

---

## Prompt 0 - Elaboração do prompt e orientação inicial

- **Fonte:** Claude (claude.ai)
- **Data:** [data]
- **Quem fez:** [nome]
- **Prompt:** Enviamos o PDF do edital do trabalho e pedimos ajuda para criar um prompt para o opencode gerar o código, além de orientações sobre GitHub.
- **O que o grupo fez com a resposta:** Recebemos um prompt base e orientações de organização do repositório. [Descreva o que vocês mudaram: tema escolhido, banco de dados, ajustes nas regras, etc.]

---

## Prompt 1 - Prompt base (estrutura do projeto, em etapas)

- **Fonte:** opencode ([modelo/provedor])
- **Data:** [data]
- **Quem fez:** [nome]
- **Prompt:**

```text
Você vai me ajudar a adaptar o projeto de exemplo desta pasta (CRUD Python + Oracle)
para um trabalho da disciplina de Banco de Dados. Antes de qualquer coisa, leia todo
o src/ do projeto (model, controller, conexion, sql, reports, utils, principal.py)
e siga exatamente a mesma arquitetura e estilo.

[TEMA]
Sistema de Locação de Veículos, com 3 tabelas:
- CLIENTES (id, nome, cpf, telefone)
- VEICULOS (id, modelo, placa, ano, valor_diaria)
- LOCACOES (id, id_cliente FK, id_veiculo FK, data_retirada, data_devolucao, valor_total)
Não pode ser o tema do exemplo (vendas/pedidos).

BANCO
- Banco Oracle, rodando na VM da disciplina (Linux). Mantenha a biblioteca de
  conexão e as sequences usadas no projeto de exemplo.
- Os dados de conexão (usuário, senha, host, porta, serviço) ficam em variáveis de
  ambiente ou num arquivo .env que NÃO vai para o GitHub (inclua um .env.example
  sem senha real).

REGRAS OBRIGATÓRIAS DO EDITAL
- Python, rodando em Linux.
- PROIBIDO usar ORM ou biblioteca que gere SQL. As queries devem ser strings
  montadas por concatenação com os atributos, como no exemplo.
- Ao iniciar: splash screen com nome do sistema, contagem de registros de cada
  tabela (select count(1) total_<entidade> from <entidade>), nomes dos integrantes
  (lista fácil de editar), disciplina Banco de Dados, semestre 2026/2, professor
  Howard Roatti.
- Menu principal sempre exibido: 1-Relatórios, 2-Inserir, 3-Remover, 4-Atualizar, 0-Sair.
- Relatórios (mínimo 2): (i) um com agregação + GROUP BY (ex.: total arrecadado
  por modelo de veículo); (ii) um com JOIN entre tabelas (ex.: locações com nome
  do cliente e modelo do veículo). Consultas em arquivos .sql dentro de src/sql.
- Inserir: menu de entidades -> pede cada atributo -> insere -> pergunta se quer
  inserir mais.
- Remover: menu de entidades -> lista registros (PK + campo descritivo) -> usuário
  escolhe -> confirma -> se o registro for FK em outra tabela, avisa e pergunta se
  quer remover também os registros filhos -> pergunta se quer remover mais.
- Atualizar: menu de entidades -> lista registros -> escolhe -> informa os novos
  valores (exceto PK) -> atualiza -> exibe o registro atualizado -> pergunta se
  quer atualizar mais.
- Cada controller deve ter método que verifica se o registro existe (não deve
  existir ao inserir; deve existir ao atualizar/remover) e abrir a conexão antes
  de executar o SQL.
- Classes de model com getters, setters e to_string; associações guardam a
  instância do outro objeto, como em itens_pedido.py / pedidos.py.

ENTREGAR
1. scripts/create_tables.sql com tabelas, PKs, FKs, constraints e sequences.
2. Diagrama relacional em Mermaid (docs/diagrama.mmd).
3. Código em src/ organizado como o exemplo.
4. README.md com passo a passo para rodar no Linux (dependências, variáveis de
   ambiente, como criar as tabelas, como executar).
5. requirements.txt e .gitignore (credenciais NUNCA no repositório).

COMO TRABALHAR
- Faça em etapas e PARE ao fim de cada uma para eu revisar: (1) modelagem e SQL,
  (2) models, (3) controllers, (4) relatórios, (5) utils/splash/menus, (6) principal.
- NÃO faça commits e não mexa no git; eu faço os commits.
- Código simples, legível, comentários curtos em português, nomes em português.
  O grupo precisa conseguir explicar cada parte, então evite abstrações desnecessárias.
- Ao fim de cada etapa, liste os arquivos criados/alterados e explique em 3-4
  linhas o que cada um faz.
```

- **O que o grupo fez com a resposta:** [Descreva: o que foi revisado, o que foi testado na VM, o que foi corrigido ou alterado manualmente e por quê.]

---

## Prompt 2 - Etapa 1: modelagem e script SQL

- **Fonte:** opencode ([modelo/provedor])
- **Data:** [data]
- **Quem fez:** [nome]
- **Prompt:** [texto exato que foi enviado]
- **O que o grupo fez com a resposta:** [ex.: conferimos tipos e chaves, rodamos o script na VM, ajustamos X]

## Prompt 3 - Etapa 2: classes de model

- **Fonte:** opencode ([modelo/provedor])
- **Data:** [data]
- **Quem fez:** [nome]
- **Prompt:** [texto exato que foi enviado]
- **O que o grupo fez com a resposta:** [...]

## Prompt 4 - Etapa 3: controllers

- **Fonte:** opencode ([modelo/provedor])
- **Data:** [data]
- **Quem fez:** [nome]
- **Prompt:** [texto exato que foi enviado]
- **O que o grupo fez com a resposta:** [...]

## Prompt 5 - Etapa 4: relatórios

- **Fonte:** opencode ([modelo/provedor])
- **Data:** [data]
- **Quem fez:** [nome]
- **Prompt:** [texto exato que foi enviado]
- **O que o grupo fez com a resposta:** [...]

## Prompt 6 - Etapa 5: utils, splash screen e menus

- **Fonte:** opencode ([modelo/provedor])
- **Data:** [data]
- **Quem fez:** [nome]
- **Prompt:** [texto exato que foi enviado]
- **O que o grupo fez com a resposta:** [...]

## Prompt 7 - Etapa 6: principal

- **Fonte:** opencode ([modelo/provedor])
- **Data:** [data]
- **Quem fez:** [nome]
- **Prompt:** [texto exato que foi enviado]
- **O que o grupo fez com a resposta:** [...]

---

## Outros prompts (correções e ajustes)

Registre aqui qualquer outro prompt usado (correção de erro, ajuste de menu, etc.), no mesmo formato acima.
