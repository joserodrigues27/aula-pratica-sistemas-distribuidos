# Aula Prática - Sistemas Distribuídos
# Professor: Jefferson Silva Lopes
# Aluno: José Rodrigues Costa Júnior

import socket
import threading

# Configuração do servidor
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 65432  # Porta de comunicação

# Lista para armazenar clientes conectados
clients = []


# Função para gerenciar conexões de clientes
def handle_client(conn, addr):
    print(f"Nova conexão: {addr}")
    connected = True
    while connected:
        try:
            # Recebe a mensagem do cliente
            msg = conn.recv(1024).decode('utf-8')
            if msg:
                print(f"{addr}: {msg}")
                broadcast(msg, conn)
            else:
                connected = False
        except:
            connected = False

    # Remove o cliente da lista e fecha a conexão
    clients.remove(conn)
    conn.close()
    print(f"Conexão encerrada: {addr}")


# Função para enviar mensagens a todos os clientes
def broadcast(message, connection):
    for client in clients:
        if client != connection:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                clients.remove(client)


# Inicialização do servidor
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Servidor iniciado em {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


# Iniciar o servidor
if __name__ == "__main__":
    start_server()