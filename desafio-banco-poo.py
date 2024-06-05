from abc import ABC, abstractmethod
import os

class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionarConta(self, conta):
        self._contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        self._nome = nome
        self._cpf = cpf
        self._data_nascimento = data_nascimento
        super().__init__(endereco)

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        self.valor = valor

        if (valor > self._saldo):
            input('Saldo insuficiente')
            return False

        elif (valor > 0):
            self._saldo-=valor
            self._historico.registrar(Saque(valor))
            input(f'Saque efetuado no valor de: R${valor}')
            return True
        
        else:
            input('Operação falhou! Valor inválido.')
            return False
            
    def depositar(self, valor):
        self.valor = valor

        if valor > 0:
            self._saldo += valor
            self._historico.registrar(Deposito(valor))
            input(f'Depósito efetuado no valor de: R${valor}')
            return True
        
        print('Operação falhou! Valor inválido.')
        return False
    
    def extrato(self):
        print('------Extrato------')
        for transacao in self._historico.transacoes:
            if isinstance(transacao, Deposito):
                print(f"Depósito efetuado no valor de: R${transacao._valor}")
            elif isinstance(transacao, Saque):
                print(f"Saque efetuado no valor de: R${transacao._valor}")
        
        print(f'Saldo atual: {self._saldo}')
        input('-------------------')
    
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes
             if isinstance(transacao, Saque)]
        )
        
        if (valor > self._limite):
            input('Operacao falhou! O valor do saque excede o limite.')

        elif (numero_saques >= self._limite_saques):
            input('Número de saques excedidos.')

        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f'''
Agência: {self._agencia}
C/C: {self._numero}
Titular: {self.cliente._nome}
        '''

class Historico:
    def __init__(self):
        self.transacoes = []

    def registrar(self, transacao):
        self.transacoes.append(transacao)

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    def registrar(self, conta):
        conta.historico.registrar(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    def registrar(self, conta):
        conta.historico.registrar(self)


def buscar_cliente_por_cpf(clientes, cpf):
    for cliente in clientes:
        if cliente._cpf == cpf:
            return cliente
    return None

def menu():
    menu = """
[D]\tDepositar
[S]\tSacar
[E]\tExtrato
[NC]\tNova conta
[LC]\tListar contas
[NU]\tNovo usuário
[LU]\tListar usuários
[F]\tFechar
Digite a opção desejada => """

    return input(menu).upper()

clientes = []

while(True):
    opcao = menu()

    if opcao == 'D':
        os.system('cls')
        cpf = input('Digite o CPF do usuário: ')
        valida_cpf = buscar_cliente_por_cpf(clientes, cpf)
        if valida_cpf:
            numero_conta = int(input('Digite o número da conta: '))
            valor = float(input('Digite o valor a ser depositado: '))
            conta = next((conta for conta in cliente._contas if conta.numero == numero_conta), None)
            if conta:
                conta.depositar(valor)
                os.system('cls')
            else:
                input('Conta não encontrada.')
                os.system('cls')
        else:
            input('Usuário não encontrado.')
            os.system('cls')

    elif opcao == 'S':
        os.system('cls')
        cpf = input('Digite o CPF do usuário: ')
        valida_cpf = buscar_cliente_por_cpf(clientes, cpf)
        if valida_cpf:
            numero_conta = int(input('Digite o número da conta: '))
            valor = float(input('Digite o valor a ser sacado: '))
            conta = next((conta for conta in cliente._contas if conta.numero == numero_conta), None)
            if conta:
                conta.sacar(valor)
                os.system('cls')
            else:
                input('Conta não encontrada.')
                os.system('cls')
        else:
            input('Usuário não encontrado.')
            os.system('cls')

    elif opcao == 'E':
        os.system('cls')
        cpf = input('Digite o CPF do usuário: ')
        valida_cpf = buscar_cliente_por_cpf(clientes, cpf)
        if valida_cpf:
            numero_conta = int(input('Digite o número da conta: '))
            conta = next((conta for conta in cliente._contas if conta.numero == numero_conta), None)
            if conta:
                os.system('cls')
                conta.extrato()
            else:
                print('Conta não encontrada.')
        else:
            print('Usuário não encontrado.')

    elif opcao == 'NU':
        os.system('cls')
        cpf = input('Informe o CPF (somente números): ')
        valida_cpf = buscar_cliente_por_cpf(clientes, cpf)
        if valida_cpf:
            input('Já existe usuário com esse CPF!')
        else:
            nome = input('Informe o nome completo: ')
            data_nascimento = input('Informe a data de nascimento (dd-mm-aaaa): ')
            endereco = input('Informe o endereço: ')
            cliente = PessoaFisica(nome, cpf, data_nascimento, endereco)
            clientes.append(cliente)
            input('Usuário criado com sucesso')

    elif opcao == 'LU':
        os.system('cls')
        if not clientes:
            input('Não existem usuários cadastrados')

        else:
            print('------Usuarios------')
            for cliente_nome in clientes:
                print(cliente_nome._nome)
            input('--------------------')

    elif opcao == 'NC':
        os.system('cls')
        cpf = input('Digite o CPF do usuário: ')
        valida_cpf = buscar_cliente_por_cpf(clientes, cpf)
        if valida_cpf:
            numero_conta = len(cliente._contas) + 1
            conta = ContaCorrente(numero_conta, cliente)
            cliente.adicionarConta(conta)
            input('Conta criada com sucesso!')
        else:
            input('Usuário não encontrado!')

    elif opcao == 'LC':
        os.system('cls')
        if not clientes:
            input('Não existem contas cadastradas.')
        else:
            print('------Contas------')
            for cliente in clientes:
                for conta in cliente._contas:
                    print(conta)
            input('--------------------')

    elif opcao == 'F':
        break

os.system('cls')
print('Programa encerrado')