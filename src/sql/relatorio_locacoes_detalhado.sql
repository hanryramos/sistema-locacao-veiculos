/*
    Relatório 2: locações com os dados do cliente e do veículo.
    Utiliza JOIN entre as três tabelas do sistema.
*/
SELECT
    L.ID AS ID_LOCACAO,
    C.NOME AS CLIENTE,
    C.CPF,
    V.MODELO AS VEICULO,
    V.PLACA,
    L.DATA_RETIRADA,
    L.DATA_DEVOLUCAO,
    L.VALOR_TOTAL
FROM LOCACOES L
INNER JOIN CLIENTES C ON C.ID = L.ID_CLIENTE
INNER JOIN VEICULOS V ON V.ID = L.ID_VEICULO
ORDER BY L.DATA_RETIRADA DESC, L.ID DESC
