from datetime import date
from model.clientes import Cliente
from model.veiculos import Veiculo

class Locacao:
    def __init__(self, 
                 id:int=None, 
                 data_retirada:date=None, 
                 data_devolucao:date=None, 
                 valor_total:float=None, 
                 cliente:Cliente=None, 
                 veiculo:Veiculo=None
                 ):
        self.set_id(id)
        self.set_data_retirada(data_retirada)
        self.set_data_devolucao(data_devolucao)
        self.set_valor_total(valor_total)
        self.set_cliente(cliente)
        self.set_veiculo(veiculo)

    def set_id(self, id:int):
        self.id = id

    def set_data_retirada(self, data_retirada:date):
        self.data_retirada = data_retirada

    def set_data_devolucao(self, data_devolucao:date):
        self.data_devolucao = data_devolucao

    def set_valor_total(self, valor_total:float):
        self.valor_total = valor_total

    def set_cliente(self, cliente:Cliente):
        self.cliente = cliente

    def set_veiculo(self, veiculo:Veiculo):
        self.veiculo = veiculo

    def get_id(self) -> int:
        return self.id

    def get_data_retirada(self) -> date:
        return self.data_retirada

    def get_data_devolucao(self) -> date:
        return self.data_devolucao

    def get_valor_total(self) -> float:
        return self.valor_total

    def get_cliente(self) -> Cliente:
        return self.cliente

    def get_veiculo(self) -> Veiculo:
        return self.veiculo

    def to_string(self) -> str:
        return f"ID: {self.get_id()} | Cliente: {self.get_cliente().get_nome()} | Veículo: {self.get_veiculo().get_modelo()} ({self.get_veiculo().get_placa()}) | Retirada: {self.get_data_retirada()} | Devolução: {self.get_data_devolucao()} | Valor Total: {self.get_valor_total()}"
