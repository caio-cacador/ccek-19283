# /usr/bin/python3
import optparse, sys
from servidor import Servidor
from usuario import Usuario


def encerra_aplicacao(mensagem):
    print(mensagem)
    sys.exit(0)


def le_input(input_txt):
    linhas = []
    try:
        with open(input_txt, "r") as file:
            linha = file.read().replace('\n', '')
            for texto in linha:
                if len(texto) > 1:
                    encerra_aplicacao("[-] Arquivo inválido, deve haver um caracter por linha.")

                linhas.append(int(texto))

    except ValueError:
        encerra_aplicacao("[-] No arquivo deve conter apenas números inteiros.")
    except FileNotFoundError:
        encerra_aplicacao("[-] Arquivo input não encontrado, verifique se o caminho esta correto.")
    except IsADirectoryError:
        encerra_aplicacao("[-] Arquivo input não encontrado, verifique se o caminho esta correto.")

    if len(linhas) <= 2:
        encerra_aplicacao('[-] Arquivo inválido, não contêm o número de novos usuários para cada tick')

    # primeira linha: valor de ttask  |  1 ≤ ttask ≤ 10
    if not 1 <= linhas[0] <= 10:
        encerra_aplicacao('[-] O valor de ttask precisa ser maior que ZERO e menor que 11 (1 ~ 10)')
    # segunda linha: valor de umax    |  1 ≤ umax ≤ 10
    if not 1 <= linhas[1] <= 10:
        encerra_aplicacao('[-] O valor de umax precisa ser maior que ZERO e menor que 11 (1 ~ 10)')

    # demais linhas contêm o número de novos usuários para cada tick
    return linhas[0], linhas[1], linhas[2:]


def get_argumentos():
    parser = optparse.OptionParser(description="Calcula backend servidor.")
    parser.add_option("-i", "--input", dest="input", default="input.txt",
                      help="Caminho do arquivo input (arquivo com os dados a serem lidos), ex: /home/user/input.txt")
    parser.add_option("-o", "--output", dest="output", default="output.txt",
                      help="Caminho do arquivo output (arquivo onde será salvo os resultados), ex: /home/user/output.txt")

    (options, arguments) = parser.parse_args()
    return options


# atualiza a lista de servidores removendo os vazios
def removeServidorVazio(__servidores):
    return [__servidor for __servidor in __servidores if not __servidor.is_empty()]


# escolhe o melhor servidor para colocar o usuário
def getServidor(__servidores):
    melhor_servidor = None
    for __servidor in __servidores:
        if not __servidor.is_full():
            """
            escolhe o servidor mais cheio para que os demais possam ser
            encerrados o quanto antes
            """
            if not melhor_servidor:
                melhor_servidor = __servidor
            elif __servidor.getTotalTtask() > melhor_servidor.getTotalTtask():
                melhor_servidor = __servidor

    if melhor_servidor:
        return melhor_servidor

    # cria um servidor novo se não houver nenhum disponível
    new_servidor = Servidor(umax)
    __servidores.append(new_servidor)
    return new_servidor


# atualiza todos os servidores
def atualizaServidores(__servidores, __output):
    qtd_usuarios = ''
    for __servidor in __servidores:
        # atualiza a lista de usuarios removendo os que já encerraram o numero de ttask
        __servidor.usuarios = [_user for _user in __servidor.usuarios if not _user.finished()]

        # atualiza o servidor (atualiza o custo do servidor e a ttask do usuario)
        __servidor.update()

        # pega a quantidade de usuarios no servidor para gravar no output.txt
        if len(__servidor.usuarios) > 0:
            if qtd_usuarios != '':
                qtd_usuarios += ','
            qtd_usuarios += str(len(__servidor.usuarios))

    # adiciona a quantidade de usuário de cada servidor no output.txt
    if qtd_usuarios != '':
        __output.append(qtd_usuarios)


def start():
    print('[+] Iniciando.')

    servidores = []
    custo_total = 0
    output = []

    # percorre as linhas que contem o número de novos usuários
    for numero in inputs:
        for i in range(int(numero)):
            # cria usuário por usuário e o coloca no melhor servidor
            getServidor(servidores).usuarios.append(Usuario(ttask))

        atualizaServidores(servidores, output)
        servidores = removeServidorVazio(servidores)
        custo_total += len(servidores)

    # continua até que todos os servidores sejam finalizados.
    while len(servidores) > 0:
        atualizaServidores(servidores, output)
        servidores = removeServidorVazio(servidores)
        custo_total += len(servidores)

    # acrescenta o ultimo 0, pois não há mais servidores
    output.append(str(len(servidores)))

    # grava o custo total
    output.append(str(custo_total))

    # escreve o output.txt
    try:
        with open(output_txt_path, 'w') as file:
            for i in output:
                file.write(i + '\n')
    except FileNotFoundError:
        encerra_aplicacao("[-] Arquivo output não encontrado, verifique se o caminho esta correto.")
    except IsADirectoryError:
        encerra_aplicacao("[-] Arquivo output não encontrado, verifique se o caminho esta correto.")

    print('[-] Custo Total: ', custo_total)
    print('[-] Salvo Em: ', output_txt_path)


if __name__ == '__main__':
    """
    recebe os argumentos
    se não for passado nenhum argumento é pego o 'default'
    """
    argumentos = get_argumentos()
    input_txt_path = argumentos.input
    output_txt_path = argumentos.output

    # recebe os valores do input.txt
    ttask, umax, inputs = le_input(input_txt_path)

    start()
