import os

saldo = 0
limite = 500
numero_saques = 0
cpf = 0
LIMITE_SAQUES = 3 # constante
extrato = []
usuarios = []
contas = []
AGENCIA = "0001"

def Menu():
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

def Depositar(saldo):
    valor = float(input('Informe o valor do depósito: R$'))
    
    if (valor < 0):
        print('Operação falhou! Valor inválido.')

    else:
        saldo+=valor
        operacao = 'Depósito'
        extrato.append({'Operacao': operacao, 'Valor': valor})
        print(f'Depósito efetuado no valor de: R${valor}')

    input()
    return saldo

def Sacar(saldo, numero_saques):
    valor = float(input('Informe o valor de saque: R$'))
    
    if (valor < 0):
        print('Operação falhou! Valor inválido.')

    elif (valor > saldo):
        print('Saldo insuficiente')

    else:
        saldo-=valor
        numero_saques+=1
        operacao = 'Saque'
        extrato.append({'Operacao': operacao, 'Valor': valor})
        print(f'Saque efetuado no valor de: R${valor}')

    input()
    return saldo, numero_saques

def Extrato():
    global saldo
    
    if (not extrato):
        input('Não foram realizadas movimentações.')

    else:
        print('------Extrato------')
        for i in extrato:
            print(f'{i['Operacao']}: R${i['Valor']}')

        print(f'Saldo atual: R${saldo}')
        input('------------------')

def Filtrar_Cpf(cpf, usuarios):
     for usuario in usuarios:
        if cpf == usuario['cpf']:
            return usuario

def Criar_Usuario(usuarios):
    cpf = input('Informe o CPF (somente, números): ')
    usuario = Filtrar_Cpf(cpf, usuarios)

    if (usuario):
        input('Já existe usuário com esse CPF!')
        return
    
    nome = input('Informe o nome completo: ')
    data_nascimento = input('Informe a data de nascimento (dd-mm-aaaa): ')
    endereco = input('Informe o endereço: ')

    usuarios.append({'nome': nome, 'data_nascimento': data_nascimento, 'cpf': cpf, 'endereco': endereco})
    input('Usuário criado com sucesso!')

def Listar_Usuarios():
    if (not usuarios):
        input('Não existem usuários cadastrados.')

    else:
        print('------Usuários------\n')
        for usuario in usuarios:
            print(usuario)

        input('\n--------------------')

def Criar_Conta(AGENCIA, numero_conta, usuarios):
    cpf = input('Digite o CPF do usuário: ')
    usuario = Filtrar_Cpf(cpf, usuarios)

    if usuario:
        input('Conta criada com sucesso!')
        return {"agencia": AGENCIA, "numero_conta": numero_conta, "usuario": usuario}
    
    else:
        input('Usuário não encontrado!')
        return None


def Listar_contas(contas):
    if not contas:
        input('Não existem contas cadastradas.')
    else:
        print('------Contas------\n')
        for conta in contas:
            titular = Filtrar_Cpf(conta['usuario']['cpf'], usuarios)
            cpf_titular = titular['cpf'] if titular else 'Usuário não encontrado'
            print(f"Agência: {conta['agencia']}, Conta: {conta['numero_conta']}, CPF Titular: {cpf_titular}")

        input('\n--------------------')


def Main():
    global LIMITE_SAQUES, numero_saques, usuarios

    while (True):
        global saldo
        opcao = Menu()
        os.system('cls')

        if (opcao == 'D'):
            saldo = Depositar(saldo)

        elif (opcao == 'S'):    
            if (numero_saques >= LIMITE_SAQUES):
                input('Número de saques excedidos.')

            else:
                saldo, numero_saques = Sacar(saldo, numero_saques)

        elif (opcao == 'E'):
            Extrato()

        elif (opcao == 'NC'):
            numero_conta = len(contas) + 1
            conta = Criar_Conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif (opcao == 'LC'):
            Listar_contas(contas)

        elif (opcao == 'NU'):   
            Criar_Usuario(usuarios)

        elif (opcao == 'LU'):
            Listar_Usuarios()

        elif (opcao == 'F'):
            break

Main()
print('Programa encerrado!')