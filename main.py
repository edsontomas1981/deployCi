from funcoes_pega_coleta import webscrap_coletas


# Execução principal
if __name__ == "__main__":

    pedidos = []

    while True:
        numero_pedido = input("Digite o número do pedido (ou 'sair' para encerrar): ")

        if numero_pedido.lower() == 'sair':
            break

        try:
            numero_pedido = int(numero_pedido)
            pedidos.append(numero_pedido)
            print(f"Número do pedido {numero_pedido} adicionado à lista.")
        except ValueError:
            print("Por favor, digite um número válido.")


    USUARIO = "edson@nor"
    SENHA = "analu1710"

    webscrap_coletas(USUARIO, SENHA,pedidos)

    print(f"lista de pedidos finalizada")

