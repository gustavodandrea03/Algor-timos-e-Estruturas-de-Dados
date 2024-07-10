class Torre:
    def __init__(self, id, nome, endereco):
        self.id = id
        self.nome = nome
        self.endereco = endereco

    def cadastrar(self):
        print(f"Torre {self.nome} cadastrada com sucesso!")

    def imprimir(self):
        print(f"Torre ID: {self.id}, Nome: {self.nome}, Endereço: {self.endereco}")


class Apartamento:
    def __init__(self, id, numero, torre, vaga=None):
        self.id = id
        self.numero = numero
        self.torre = torre
        self.vaga = vaga
        self.proximo = None

    def cadastrar(self):
        print(f"Apartamento {self.numero} cadastrado com sucesso!")

    def imprimir(self):
        print(f"Apartamento ID: {self.id}, Número: {self.numero}, Torre: {self.torre.nome}, Vaga: {self.vaga}")


class ApartamentoFila:  # encapsula um apartamento e adiciona um ponteiro que aponta para o próximo que estiver na fila.
    def __init__(self, apartamento):
        self.apartamento = apartamento
        self.proximo = None


class FilaEspera:   # a fila de espera inicia vazia
    def __init__(self):
        self.primeiro = None
        self.ultimo = None

    def adicionar(self, apartamento): # adiciona novo apartamento ao final da fila
        novo_apartamento = ApartamentoFila(apartamento)
        if self.ultimo:
            self.ultimo.proximo = novo_apartamento
        else:
            self.primeiro = novo_apartamento
        self.ultimo = novo_apartamento
        print(f"Apartamento {apartamento.numero} adicionado à fila de espera.")

    def retirar(self, vaga):    # retirar o primeiro apartamento da fila e atribui a ele uma vaga disponivel.
        if self.primeiro:
            apartamento_fila = self.primeiro
            self.primeiro = apartamento_fila.proximo
            if not self.primeiro:
                self.ultimo = None
            apartamento_fila.apartamento.vaga = vaga
            return apartamento_fila.apartamento
        else:
            print("Fila de espera está vazia.")
            return None

    def imprimir(self):
        if not self.primeiro:
            print("Não há apartamentos na fila de espera.")
        else:
            print("Fila de espera:")
            atual = self.primeiro
            while atual:
                atual.apartamento.imprimir()
                atual = atual.proximo


class Condominio:
    def __init__(self):
        self.apartamentos_com_vaga = None #  lista inicia vazia
        self.fila_espera = FilaEspera()
        self.vagas_disponiveis = list(range(1, 11))

    def cadastrar_apartamento(self, apartamento):
        if self.vagas_disponiveis:  # se não encontrar vagas disponiveis, transfere para fila de espera.
            vaga = self.vagas_disponiveis.pop(0)
            apartamento.vaga = vaga
            self.adicionar_apartamento_na_lista(apartamento)
            print(f"Apartamento {apartamento.numero} cadastrado com vaga {vaga}.")
        else:
            self.fila_espera.adicionar(apartamento)
            print(f"Apartamento {apartamento.numero} está esperando abrir uma vaga.")



    def liberar_vaga(self, vaga):   #Libera uma vaga e tenta adicionar essa vaga ao próximo apartamento na fila de espera.
        if self.apartamentos_com_vaga is None and not self.fila_espera.primeiro:
            print("Não há vagas registradas com esse número.")
            return

        anterior = None
        atual = self.apartamentos_com_vaga

        while atual and atual.vaga != vaga:
            anterior = atual
            atual = atual.proximo

        if atual:
            if anterior:
                anterior.proximo = atual.proximo
            else:
                self.apartamentos_com_vaga = atual.proximo

            atual.vaga = None
            self.fila_espera.adicionar(atual)
            print(f"A vaga {vaga} do Apartamento {atual.numero} foi liberada e está disponível.")

            novo_apartamento = self.fila_espera.retirar(vaga)
            if novo_apartamento:
                self.adicionar_apartamento_na_lista(novo_apartamento)
                print(f"Apartamento {novo_apartamento.numero} retirado da fila de espera e foi cadastrado com vaga {vaga}.")
            else:
                self.vagas_disponiveis.append(vaga)
                self.vagas_disponiveis.sort()
        else:
            print("Vaga não encontrada.")



    def adicionar_apartamento_na_lista(self, apartamento): # adiciona o apartamento  dentro da lista de apartamentos com vaga.
        if not self.apartamentos_com_vaga or self.apartamentos_com_vaga.vaga > apartamento.vaga:
            apartamento.proximo = self.apartamentos_com_vaga
            self.apartamentos_com_vaga = apartamento
        else:
            atual = self.apartamentos_com_vaga
            while atual.proximo and atual.proximo.vaga < apartamento.vaga:
                atual = atual.proximo
            apartamento.proximo = atual.proximo
            atual.proximo = apartamento

    def imprimir_apartamentos_com_vaga(self):
        if self.apartamentos_com_vaga is None:
            print("Não há apartamentos com vaga registrados.")
        else:
            print("Lista de apartamentos com vaga:")
            atual = self.apartamentos_com_vaga
            while atual:
                atual.imprimir()
                atual = atual.proximo

    def imprimir_fila_de_espera(self):
        self.fila_espera.imprimir()


def menu():
    condominio = Condominio()

   # ______________________________________________________________________________________________ 
            #   MENU DE OPÇÔES

    while True:

        print("\n       Bem Vindo!      ")
        print("  - - -  MENU - - - ")
        print("1. Cadastrar apartamento")
        print("2. Liberar vaga")
        print("3. Imprimir a lista de apartamentos com vaga")
        print("4. Imprimir a fila de apartamentos esperando por vaga")
        print("5. Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            try:
                id_apartamento = int(input("ID do apartamento: "))
            except ValueError:
                print("ID inválido. Tente novamente.")
                continue
            
            try:    
                numero = int(input("Número do apartamento: "))
            except ValueError:
                print("Inválido. Tente Novamente.")
                continue

            try:
                id_torre = int(input("ID da torre: "))
            except ValueError:
                print("ID da torre inválido. Tente novamente.")
                continue

            nome_torre = input("Nome da torre: ")
            endereco_torre = input("Endereço da torre: ")

            torre = Torre(id_torre, nome_torre, endereco_torre)
            apartamento = Apartamento(id_apartamento, numero, torre)
            condominio.cadastrar_apartamento(apartamento)


        elif opcao == '2':
            try:
                vaga = int(input("Número da vaga a ser liberada: "))
            except ValueError:
                print("Número da vaga inválido. Tente novamente.")
                continue

            condominio.liberar_vaga(vaga)


        elif opcao == '3':
            condominio.imprimir_apartamentos_com_vaga()


        elif opcao == '4':
            condominio.imprimir_fila_de_espera()


        elif opcao == '5':
            print("Encerrando...")
            break

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()