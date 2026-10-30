class Cliente:
    def __init__(self, 
                 id:int=None, 
                 nome:str=None, 
                 cpf:str=None, 
                 telefone:str=None
                 ):
        self.set_id(id)
        self.set_nome(nome)
        self.set_cpf(cpf)
        self.set_telefone(telefone)

    def set_id(self, id:int):
        self.id = id

    def set_nome(self, nome:str):
        self.nome = nome

    def set_cpf(self, cpf:str):
        self.cpf = cpf

    def set_telefone(self, telefone:str):
        self.telefone = telefone

    def get_id(self) -> int:
        return self.id

    def get_nome(self) -> str:
        return self.nome

    def get_cpf(self) -> str:
        return self.cpf

    def get_telefone(self) -> str:
        return self.telefone

    def to_string(self) -> str:
        return f"ID: {self.get_id()} | Nome: {self.get_nome()} | CPF: {self.get_cpf()} | Telefone: {self.get_telefone()}"
