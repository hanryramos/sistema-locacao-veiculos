import sys

from utils import config
from utils.splash_screen import SplashScreen
from reports.relatorios import Relatorio
from controller.controller_cliente import ControllerCliente
from controller.controller_veiculo import ControllerVeiculo
from controller.controller_locacao import ControllerLocacao


def ler_opcao(mensagem: str) -> int:
    while True:
        try:
            return int(input(mensagem).strip())
        except ValueError:
            print("Digite apenas números.")


def perguntar_sim_nao(mensagem: str) -> bool:
    while True:
        resposta = input(mensagem).strip().lower()
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "nao", "não"):
            return False
        print("Responda com 's' (sim) ou 'n' (não).")


def executar_acao(acao):
    """Executa uma operação e evita que um erro do banco derrube o sistema."""
    try:
        return acao()
    except Exception as erro:
        print(f"\nErro ao executar a operação: {erro}")
        input("Pressione Enter para continuar...")
        return None


class Sistema:
    def __init__(self):
        self.tela_inicial = SplashScreen()
        self.relatorio = Relatorio()
        self.ctrl_cliente = ControllerCliente()
        self.ctrl_veiculo = ControllerVeiculo()
        self.ctrl_locacao = ControllerLocacao()

    def mostrar_tela_inicial(self):
        print(self.tela_inicial.get_updated_screen())
        config.clear_console(1)

    # ------------------------------------------------------------------
    # Menus
    # ------------------------------------------------------------------
    def menu_relatorios(self):
        while True:
            print(config.MENU_RELATORIOS)
            opcao = ler_opcao("Escolha um relatório [0-2]: ")

            if opcao == 0:
                return
            if opcao == 1:
                executar_acao(self.relatorio.get_relatorio_arrecadacao_por_modelo)
            elif opcao == 2:
                executar_acao(self.relatorio.get_relatorio_locacoes_detalhado)
            else:
                print("Opção inválida.")

    def escolher_entidade(self) -> int:
        while True:
            print(config.MENU_ENTIDADES)
            opcao = ler_opcao("Escolha uma entidade [0-3]: ")
            if opcao in (0, 1, 2, 3):
                return opcao
            print("Opção inválida.")

    def executar_operacoes(self, acoes, pergunta_continuar):
        """Executa a ação escolhida e pergunta se o usuário deseja repetir."""
        while True:
            opcao = self.escolher_entidade()
            if opcao == 0:
                return

            resultado = executar_acao(acoes[opcao])

            # Operação cancelada, sem registro ou com erro: volta ao menu principal.
            if resultado is None:
                return

            if not perguntar_sim_nao(pergunta_continuar):
                return

    # ------------------------------------------------------------------
    # Operações
    # ------------------------------------------------------------------
    def inserir(self):
        self.executar_operacoes({
            1: self.ctrl_cliente.inserir,
            2: self.ctrl_veiculo.inserir,
            3: self.ctrl_locacao.inserir_locacao,
        }, "Deseja inserir mais algum registro? (s/n): ")

    def remover(self):
        self.executar_operacoes({
            1: self.ctrl_cliente.remover,
            2: self.ctrl_veiculo.remover,
            3: self.ctrl_locacao.remover_locacao,
        }, "Deseja excluir mais algum registro? (s/n): ")

    def atualizar(self):
        self.executar_operacoes({
            1: self.ctrl_cliente.atualizar,
            2: self.ctrl_veiculo.atualizar,
            3: self.ctrl_locacao.atualizar_locacao,
        }, "Deseja atualizar mais algum registro? (s/n): ")

    # ------------------------------------------------------------------
    # Loop principal
    # ------------------------------------------------------------------
    def executar(self):
        self.mostrar_tela_inicial()

        while True:
            print(config.MENU_PRINCIPAL)
            opcao = ler_opcao("Escolha uma opção [0-4]: ")
            config.clear_console()

            if opcao == 0:
                print("Obrigado por utilizar o nosso sistema.")
                break

            if opcao == 1:
                self.menu_relatorios()
                config.clear_console()
            elif opcao == 2:
                self.inserir()
                self.mostrar_tela_inicial()
            elif opcao == 3:
                self.remover()
                self.mostrar_tela_inicial()
            elif opcao == 4:
                self.atualizar()
                self.mostrar_tela_inicial()
            else:
                print("Opção inválida.")


def run():
    try:
        Sistema().executar()
    except KeyboardInterrupt:
        print("\nSistema encerrado.")
        sys.exit(0)


if __name__ == "__main__":
    run()
