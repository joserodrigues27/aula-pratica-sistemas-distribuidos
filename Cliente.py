import socket
import threading

# Configuração do cliente
SERVER = '127.0.0.1' # Endereço IP do servidor
PORT = 65432 # Porta de comunicação


# Função para receber mensagens do servidor
def receive_messages(client):
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            if msg:
                print(msg)
        except:
            print("Erro ao receber mensagem")
            client.close()
            break


# Função para enviar mensagens ao servidor
def send_messages(client, username):
    while True:
        msg = input()
        full_msg = f"{username}: {msg}"
        client.send(full_msg.encode('utf-8'))


# Conectar ao servidor
def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))

    # Solicitar nome de usuário
    username = input("Digite seu nome de usuário: ")

    # Iniciar threads para enviar e receber mensagens
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(client, username))
    send_thread.start()


# Iniciar o cliente
if __name__ == "__main__":
    start_client()