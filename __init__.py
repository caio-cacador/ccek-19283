# /usr/bin/python3
import optparse, os
from servidor import Servidor
from usuario import Usuario


def encerra_aplicacao(mensagem):
    print(mensagem)
    os.abort()


def le_input(input_txt):
    linhas = []
    try:
        with open(input_txt, "r") as file:
            linha = file.read().replace('\n', '')
            for texto in linha:
                if len(texto) > 1:
                    encerra_aplicacao("[-] Arquivo invalido, deve haver um caracter por linha!")

                linhas.append(int(texto))

    except ValueError:
        encerra_aplicacao("[-] No arquivo deve contas apenas numeros.")
    except FileNotFoundError as ex:
        encerra_aplicacao("[-] Arquivo input não encontrado.")

    if len(linhas) <= 2:
        encerra_aplicacao('[-] Arquivo invalido, não contêm o número de novos usuários para cada tick')

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
                      help="Caminho do arquivo input (arquivo com os dados a serem lidos), ex: /home/caio/input.txt")
    parser.add_option("-o", "--output", dest="output", default="output.txt",
                      help="Caminho do arquivo output (arquivo onde será salvo os resultados), ex: /home/caio/output.txt")

    (options, arguments) = parser.parse_args()
    return options


def removeServidoresVazio(__servidores):
    return [servidor for servidor in __servidores if not servidor.is_empty()]


def getServidor(__servidores):
    melhor_servidor = None
    for servidor in __servidores:
        if not servidor.is_full():
            if not melhor_servidor:
                melhor_servidor = servidor
            elif servidor.getTotalTtask() > melhor_servidor.getTotalTtask():
                melhor_servidor = servidor

    if melhor_servidor:
        return melhor_servidor

    new_servidor = Servidor(umax)
    __servidores.append(new_servidor)
    return new_servidor


def atualizaServidores(__servidores):
    status = ''
    for servidor in __servidores:
        servidor.usuarios = [_user for _user in servidor.usuarios if not _user.finished()]
        servidor.update()
        if len(servidor.usuarios) > 0:
            if status != '':
                status += ','
            status += str(len(servidor.usuarios))

    print(status)


if __name__ == '__main__':
    argumento = get_argumentos()
    input_txt = argumento.input
    output_txt = argumento.output
    ttask, umax, inputs = le_input(input_txt)

    servidores = []
    custo_total = 0
    output = []

    for number in inputs:
        for i in range(int(number)):
            getServidor(servidores).usuarios.append(Usuario(ttask))


        atualizaServidores(servidores)
        servidores = removeServidoresVazio(servidores)
        custo_total += len(servidores)

    while len(servidores) > 0:
        atualizaServidores(servidores)
        servidores = removeServidoresVazio(servidores)
        custo_total += len(servidores)

    output.append(str(custo_total))
    with open(output_txt, 'w') as file:
        for i in output:
            file.writelines(i)
    print('[-] Custo Total: ', custo_total)