import sqlite3
import time
import datetime as dt

##BANCO DE VENDAS##1

##BANCO DE PRODUTOS
banco_produtos = sqlite3.connect('produtos.db')
cursor_produtos = banco_produtos.cursor()
ver = cursor_produtos.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='infos';").fetchone()
if ver[0] == 0:
    cursor_produtos.execute("CREATE TABLE infos (nome text, preço float, quantidade int)")

##BANCO DE CLIENTES##
banco_clientes = sqlite3.connect('clientes.db')
cursor_clientes = banco_clientes.cursor()
ver = cursor_clientes.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='infos';").fetchone()
if ver[0] == 0:
    cursor_clientes.execute("CREATE TABLE infos (nome text, email text, login text, senha text)")

##BANCO DE VENDAS##
banco_vendas = sqlite3.connect('vendas.db')
cursor_vendas = banco_vendas.cursor()
ver = cursor_vendas.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='infos';").fetchone()
if ver[0] == 0:
    cursor_vendas.execute("CREATE TABLE infos (cliente text, email text, carrinho text, preço float, data_hora text)")

def lin():
    print('-=' * 12)

def menu_adm():
    while True:
        lin()
        print('Menu do ADM')
        lin()
        print('[1] Cadastrar produto')
        print('[2] Ver produtos')
        print('[3] Alterar preço')
        print('[4] Excluir produto')
        print('[5] Alterar quantidade')
        print('[6] Sair')
        lin()

        while True:

            cursor_produtos.execute("SELECT * FROM infos")
            produtos = [produto for produto in cursor_produtos.fetchall()]

            try:
                escolha = int(input('>>>>>>>>>>>>>>>>'))
                while escolha not in range(1, 7):
                    print('Opção inválida')
                    escolha = int(input('>>>>>>>>>>>>>>>>'))
                while escolha in (2, 3, 4) and len(produtos) == 0:
                    print('Erro!, Ainda não há produtos cadastrados')
                    escolha = int(input('>>>>>>>>>>>>>>>>'))
                break
            except ValueError:
                print('Digite um número!!')

        if escolha == 1:
            while True:
                lin()
                print('Cadastro de produto')
                lin()

                cursor_produtos.execute("SELECT * FROM infos")

                produtos = []
                for produto in cursor_produtos.fetchall():
                    produtos.append(produto[0])

                nome_produto = str(input('Nome do produto:'))

                while nome_produto in produtos:
                    print('Produto já cadastrado!')
                    nome_produto = str(input('Nome do produto:'))

                while True:
                    try:
                        preço_produto = float(input('Preço:'))
                        break
                    except ValueError:
                        print('Valor inválido')

                while True:
                    try:
                        quantidade = int(input('Quantidade disponível:'))
                        break
                    except ValueError:
                        print('Digite um número!')

                lin()

                cursor_produtos.execute("INSERT INTO infos VALUES ('" + nome_produto + "','" + str(preço_produto) + "', '" + str(quantidade) + "')")
                banco_produtos.commit()

                continuar = str(input('Continuar a cadastrar? [s/n]:')).lower()

                while continuar not in ('s', 'n'):
                    print('Opção inválida!')
                    continuar = str(input('Continuar a cadastrar? [s/n]:')).lower()

                if continuar == 'n':
                    break

        if escolha == 2:
            cursor_produtos.execute("SELECT * FROM infos")
            for cont, produto in enumerate(cursor_produtos.fetchall()):
                lin()
                print(f'{cont + 1}º Produto')
                print(f'Nome: {produto[0]}')
                print(f'Preço: {produto[1]}')
                print(f'Quantidade: {produto[2]}')
                time.sleep(0.3)

        if escolha == 3:
            lin()
            print('Alterar preço')
            lin()

            while True:
                try:
                    id_alterar = int(input('Id do produto que deseja alterar o preço:'))

                    cursor_produtos.execute("SELECT * FROM infos")

                    produtos = [produto for produto in cursor_produtos.fetchall()]

                    while id_alterar not in range(1, len(produtos) + 1):
                        print('Id inválido')
                        id_alterar = int(input('Id do produto que deseja alterar o preço:'))
                    break

                except ValueError:
                    print('Digite um número!!')

            cursor_produtos.execute("SELECT * FROM infos")
            for cont, produto in enumerate(cursor_produtos.fetchall()):
                if cont + 1 == id_alterar:
                    nome_produto = produto[0]

            while True:
                try:
                    novo_preco = float(input(f'Novo preço do produto "{nome_produto}": '))
                    break
                except ValueError:
                    print('Digite um valor decimal!')

            while True:
                try:
                    cursor_produtos.execute("UPDATE infos SET preço = '" + str(novo_preco) + "' WHERE nome = '" + nome_produto + "'")
                    banco_produtos.commit()
                    print('Preço atualizado com sucesso!')
                    break
                except:
                    print('Erro desconhecido!, não foi possível alterar o preço!')

        if escolha == 4:
            lin()
            print('Deletar produto')
            lin()

            cursor_produtos.execute("SELECT * FROM infos")

            produtos = [produto for produto in cursor_produtos.fetchall()]

            while True:
                try:
                    id_apagar = int(input('Id do produto que desejas apagar:'))
                    while id_apagar not in range(1, len(produtos) + 1):
                        print('Id inválido!')
                        id_apagar = int(input('Id do produto que desejas apagar:'))
                    break
                except ValueError:
                    print('Digite um número!')

            for cont, produto in enumerate(produtos):
                if cont + 1 == id_apagar:
                    nome_produto = produto[0]
                    print(f'Produto "{nome_produto}" deletado!')

            confirm = str(input(f'Deletar o produto "{nome_produto}"[s/n]:')).lower()
            while confirm not in ('s','n'):
                print('Opção inválida!')
                confirm = str(input(f'Deletar o produto "{nome_produto}"[s/n]:')).lower()

            if confirm == 's':
                cursor_produtos.execute("DELETE FROM infos WHERE nome = '" + nome_produto + "'")
                banco_produtos.commit()
                print('Produto deletado!')
            else:
                print('Produto não foi deletado!')

        if escolha == 5:

            cursor_produtos.execute("SELECT * FROM infos")
            produtos = [produto for produto in cursor_produtos.fetchall()]

            while True:
                try:
                    id_quantidade = int(input('Id do item para mudar a quantidade:'))
                    while id_quantidade not in range(1, len(produtos) + 1):
                        print('Id inválido!')
                        id_quantidade = int(input('Id do item para mudar a quantidade:'))
                    break
                except ValueError:
                    print('Digite um id válido!')

            while True:
                try:
                    nova_quantidade = int(input('Nova quantidade:'))
                    break
                except ValueError:
                    print('Digite uma quantidade válida!')

            for cont, produto in enumerate(produtos):
                if cont + 1 == id_quantidade:
                    nome_produto = produto[0]

            confirm = str(input(f'Alterar quantidade do produto "{nome_produto}" para "{nova_quantidade}"[s/n]:')).lower()
            while confirm not in ('n', 's'):
                print('Opção inválida!')
                confirm = str(input(f'Alterar quantidade do produto "{nome_produto}" para "{nova_quantidade}"[s/n]:')).lower()

            if confirm == 's':
                cursor_produtos.execute("UPDATE infos SET quantidade = '" + str(nova_quantidade) + "' WHERE nome = '" + nome_produto + "'")
                banco_produtos.commit()
            else:
                print('Alteração cancelada!')

        if escolha == 6:
            print('Deslogando...')
            time.sleep(1)
            break

def menu_cliente(usuario_logado):

    nome_logado = usuario_logado[0]
    email_logado = usuario_logado[1]

    def realizar_compra():
        carrinho = []
        preco_total = 0

        while True:
            lin()
            print('Efetuar compra')
            print(f'Preço do carrinho: R${preco_total:.2f}')
            lin()
            print('[1] Adicionar produto no carrinho')
            print('[2] Remover produto do carrinho')
            print('[3] Ver meu carrinho')
            print('[4] Limpar carrinho')
            print('[5] Ver produtos disponíveis')
            print('[6] Cancelar compra')
            print('[7] Finalizar compra')

            while True:
                try:
                    escolha_compra = int(input('>>>>>>>>>>>>>>>>'))
                    while escolha_compra not in range(1, 8):
                        print('Opção inválida!')
                        escolha_compra = int(input('>>>>>>>>>>>>>>>>'))
                    break
                except ValueError:
                    print('Digite um valor válido!')

            if escolha_compra == 1:

                cursor_produtos.execute('SELECT * FROM infos')
                produtos = [produto for produto in cursor_produtos.fetchall()]

                while True:
                    while True:
                        try:
                            id_compra = int(input('Id do item:'))
                            while id_compra not in range(1, len(produtos) + 1):
                                print('Id inválido!!')
                                id_compra = int(input('Id do item:'))
                            break
                        except ValueError:
                            print('Digite o número de id do produto!')

                    quantidade_compra = int(input('Quantidade:'))

                    for cont, produto in enumerate(produtos):
                        while cont + 1 == id_compra and quantidade_compra > produto[2]:
                            print(f'Produto "{produto[0]}" só tem apenas "{produto[2]}" unidades disponíveis')
                            quantidade_compra = int(input('Quantidade:'))
                        if cont + 1 == id_compra:
                            nome_produto = produto[0]
                            total = quantidade_compra * produto[1]

                    print(f'Colocar "{quantidade_compra}" unidades do produto "{nome_produto}" no carrinho.')
                    print(f'Total = R${total:.2f}')

                    confirm = input('Confirma? [s/n]:').lower()

                    while confirm not in ('s', 'n'):
                        print('Opção inválida!')
                        confirm = input('Confirma? [s/n]:').lower()

                    if confirm == 's':

                        for produto in produtos:
                            if produto[0] == nome_produto:
                                quantidade_disponivel = produto[2] - quantidade_compra

                        cursor_produtos.execute("UPDATE infos SET quantidade = '" + str(quantidade_disponivel) + "' WHERE nome = '" + nome_produto + "'")
                        banco_produtos.commit()

                        produtos_carrinho = [produto[0] for produto in carrinho]

                        if nome_produto not in produtos_carrinho:
                            carrinho.append([nome_produto, quantidade_compra])
                        else:
                            for produto in carrinho:
                                if produto[0] == nome_produto:
                                    produto[1] += quantidade_compra

                        preco_total += total
                        print('Produto(s) adicionado(s) ao carrinho')

                        cont = str(input('Continuar? [s/n]:')).lower()

                        while cont not in ('s', 'n'):
                            print('Opção inválida!')
                            cont = str(input('Continuar? [s/n]:')).lower()

                        if cont == 'n':
                            break

                    elif confirm == 'n':
                        print('Produtos devolvidos')
                        break

            if escolha_compra == 2:

                if len(carrinho) == 0:
                    print('Seu carrinho está vazio!')
                else:
                    while True:
                        try:
                            id_remover = int(input('Id do item que desejas remover do carrinho:'))
                            while id_remover not in range(1, len(carrinho) + 1):
                                print('Id inválido!')
                                id_remover = int(input('Id do item que desejas remover do carrinho:'))
                            break
                        except ValueError:
                            print('Digite um Id válido!')

                    for cont, produto in enumerate(carrinho):
                        if cont + 1 == id_remover:
                            quantidade_carrinho = produto[1]

                    while True:
                        try:
                            quantidade_remover = int(input('Remover quantas unidades:'))
                            while quantidade_remover > quantidade_carrinho:
                                print('Não há esta quantidade no seu carrinho!')
                                quantidade_remover = int(input('Remover quantas unidades:'))
                            break
                        except ValueError:
                            print('Digite uma quantidade válida!')

                    for cont, produto in enumerate(carrinho):
                        if cont + 1 == id_remover:

                            nome_remover = produto[0]

                            produto[1] -= quantidade_remover

                            if produto[1] == 0:
                                carrinho.remove(produto)

                    cursor_produtos.execute("SELECT * FROM infos")
                    for produto in cursor_produtos.fetchall():
                        if produto[0] == nome_remover:
                            disponivel = produto[2]
                            quantidade = disponivel + quantidade_remover
                            preco_total -= (quantidade_remover * produto[1])

                    cursor_produtos.execute("UPDATE infos SET quantidade = '" + str(quantidade) + "' WHERE nome = '" + nome_remover + "'")
                    banco_produtos.commit()

            if escolha_compra == 3:
                lin()
                print('Carrinho:')
                lin()
                for produto in carrinho:
                    print(f"{produto[0]} - {produto[1]} Unidades ")

            if escolha_compra == 4:

                if len(carrinho) == 0:
                    print('Seu carrinho já está vazio!')
                else:
                    cursor_produtos.execute("SELECT * FROM infos")
                    for produto in cursor_produtos.fetchall():
                        for produto_carrinho in carrinho:
                            if produto[0] == produto_carrinho[0]:
                                novo_disponivel = produto[2] + produto_carrinho[1]

                    cursor_produtos.execute("UPDATE infos SET quantidade = '"+ str(novo_disponivel) +"' WHERE nome = '"+ produto_carrinho[0] +"'")
                    banco_produtos.commit()

                    print('Carrinho limpado!')
                    preco_total = 0
                    carrinho = []

            if escolha_compra == 5:

                ver_produtos()

            if escolha_compra == 6:

                print('Compra cancelada!')
                break

            if escolha_compra == 7:

                if len(carrinho) == 0:
                    print('Seu carrinho está vazio!')
                else:

                    data_hora = dt.datetime.now()

                    carrinho_str = ''
                    for produto in carrinho:
                        carrinho_str += f'|{produto[0]} - {str(produto[1])} Unidade(s)| '

                    cursor_vendas.execute("INSERT INTO infos VALUES('" + nome_logado + "', '" + email_logado + "', '" + carrinho_str + "', '" + str(preco_total) + "', '" + str(data_hora) + "')")
                    banco_vendas.commit()

                    lin()
                    print('Compra finalizada com sucesso!')
                    lin()

                    carrinho = []

                    break

    def ver_produtos():
        lin()
        print('Produtos disponíveis')
        lin()

        cursor_produtos.execute("SELECT * FROM infos")
        produtos = cursor_produtos.fetchall()

        for cont, produto in enumerate(produtos):
            time.sleep(0.3)
            print(f'{cont + 1}º Produto')
            print('-' * 24)
            print(f'- {produto[0]}')
            print(f'Preço:R${produto[1]:,.2f}')
            print(f'Quantidade disponível: {produto[2]}')
            lin()

    def minhas_compras():
        cursor_vendas.execute('SELECT * FROM infos')
        for venda in cursor_vendas.fetchall():
            if venda[0] == nome_logado:
                lin()
                print('Sua compra:')
                print(f'Carrinho - {venda[2]}')
                print(f'Valor total - R${venda[3]:.2f}')
                print(f'Data e hora - {venda[4]}')

    lin()
    print(f'Olá, {usuario_logado[0]}')
    while True:
        lin()
        print('Menu do cliente')
        lin()
        print('[1] Ver produtos')
        print('[2] Realizar compra')
        print('[3] Minhas compras')
        print('[4] Sair')

        while True:
            try:
                escolha = int(input('>>>>>>>>>>>>>'))
                while escolha not in range(1, 5):
                    print('Opção inválida!')
                    escolha = int(input('>>>>>>>>>>>>>'))
                break
            except ValueError:
                print('Digite um número')

        if escolha == 1:

            ver_produtos()

        if escolha == 2:

            realizar_compra()

        if escolha == 3:

            minhas_compras()

        if escolha == 4:

            print('Deslogando...')
            time.sleep(1)
            break


def menu_principal():

    def acessar_loja():
        lin()
        print('Para acessar, faça o login')
        lin()

        login = str(input('Login:'))
        senha = str(input('Senha:'))

        cursor_clientes.execute("SELECT * FROM infos")

        acesso = None
        for usuario in cursor_clientes.fetchall():
            if login == usuario[2] and senha == usuario[3]:
                acesso = True
                print('Logado com sucesso!')
                break
            else:
                acesso = False

        if acesso == True:
            usuario_logado = usuario
            menu_cliente(usuario_logado)
        elif acesso == False:
            print('Login ou senha inválidos!')

    def registrar():
        lin()
        print('Registro')
        lin()

        nome = str(input('Seu nome:')).title()
        email = str(input('Seu email:'))
        login = str(input('Login:'))

        cursor_clientes.execute("SELECT * FROM infos")

        logins = []
        for usuario in cursor_clientes.fetchall():
            logins.append(usuario[2])
        while login in logins:
            print('Login já utilizado')
            login = str(input('Login:'))

        senha = str(input('Senha:'))
        confirma_senha = str(input('Confirmar senha:'))

        while senha != confirma_senha or senha == '':
            print('Senhas não batem!')
            senha = str(input('Senha:'))
            confirma_senha = str(input('Confirmar senha:'))

        cursor_clientes.execute("INSERT INTO infos VALUES ('" + nome + "','" + email + "','" + login + "','" + senha + "')")
        banco_clientes.commit()

    def entrar_adm():

        senha_adm = 'Az1310750412'
        senha = str(input('Senha:'))

        if senha != senha_adm:
            print('Senha inválida!')
        else:
            print('Logado com sucesso!')
            menu_adm()

    lin()
    print('Menu principal')
    lin()
    print('[1] Acessar loja')
    print('[2] Registrar')
    print('[3] Entrar como ADM')
    print('[4] Sair')
    lin()

    while True:
        try:
            escolha = int(input('>>>>>>>>>>>>>>>>'))
            while escolha not in range(1, 5):
                print('Opção inválida!')
                escolha = int(input('>>>>>>>>>>>>>>>>'))
            break
        except ValueError:
            print('Digite um número!')

    if escolha == 1:
        acessar_loja()

    if escolha == 2:
        registrar()

    if escolha == 3:
        entrar_adm()

    if escolha == 4:
        input('Programa finalizado!')
        quit()

while True:
    menu_principal()