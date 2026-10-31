/*
    Relatório 1: total arrecadado por modelo de veículo.
    Soma o valor total das locações agrupando pelo modelo.
*/
SELECT
    V.MODELO,
    COUNT(L.ID) AS TOTAL_LOCACOES,
    SUM(L.VALOR_TOTAL) AS TOTAL_ARRECADADO
FROM VEICULOS V
INNER JOIN LOCACOES L ON L.ID_VEICULO = V.ID
GROUP BY V.MODELO
ORDER BY TOTAL_ARRECADADO DESC
