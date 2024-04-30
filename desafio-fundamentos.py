import os

# Sistema Bancário

menu = """
[D]epositar
[S]acar
[E]xtrato
[F]echar
Digite a opção desejada => """

saldo = 0
limite = 500
numero_saques = 0
LIMITE_SAQUES = 3 # constante
extrato = []

while True:
    opcao = input(menu).upper()
    os.system('cls')

    if (opcao == 'D'):
        valor = float(input('Informe o valor do depósito: R$'))

        if (valor > 0):
            saldo += valor
            operacao = 'Depósito'
            extrato.append({'Operacao': operacao, 'Valor': valor})
            print(f'Depósito efetuado no valor de: R${valor}')

        else:
            print('Operação falhou! Valor inválido.')

    elif (opcao == 'S'):
        valor = float(input('Informe o valor de saque: R$'))

        if (numero_saques > LIMITE_SAQUES):
            print('Número de saques excedidos.')

        elif (valor > saldo):
            print('Saldo indisponível para saque')

        elif (valor > 0):
            saldo -= valor
            numero_saques += 1
            operacao = 'Saque'
            extrato.append({'Operacao': operacao, 'Valor': valor})
            print(f'Saque efetuado no valor de: R${valor}')

        else:
            print('Operação falhou! Valor inválido.')

    elif (opcao == 'E'):
        print('---Extrato---')
        for i in extrato:
            print(f'{i['Operacao']}: R${i['Valor']}')

        print(f'Saldo atual: R${saldo}')
        input('------------')

    elif (opcao == 'F'):
        break

    else:
        print('Opção inválida, por favor selecione novamente a operação desejada.')

print('Programa encerrado!')