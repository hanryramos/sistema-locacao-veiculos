class Veiculo:
    def __init__(self, 
                 id:int=None, 
                 modelo:str=None, 
                 placa:str=None, 
                 ano:int=None, 
                 valor_diaria:float=None
                 ):
        self.set_id(id)
        self.set_modelo(modelo)
        self.set_placa(placa)
        self.set_ano(ano)
        self.set_valor_diaria(valor_diaria)

    def set_id(self, id:int):
        self.id = id

    def set_modelo(self, modelo:str):
        self.modelo = modelo

    def set_placa(self, placa:str):
        self.placa = placa

    def set_ano(self, ano:int):
        self.ano = ano

    def set_valor_diaria(self, valor_diaria:float):
        self.valor_diaria = valor_diaria

    def get_id(self) -> int:
        return self.id

    def get_modelo(self) -> str:
        return self.modelo

    def get_placa(self) -> str:
        return self.placa

    def get_ano(self) -> int:
        return self.ano

    def get_valor_diaria(self) -> float:
        return self.valor_diaria

    def to_string(self) -> str:
        return f"ID: {self.get_id()} | Modelo: {self.get_modelo()} | Placa: {self.get_placa()} | Ano: {self.get_ano()} | Valor da Diária: {self.get_valor_diaria()}"
