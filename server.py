import socket
import os

# Endereço e porta do servidor
HOST = '0.0.0.0'  # Escuta em todas as interfaces de rede
PORT = 5000       # Porta de comunicação
SAVE_DIR = 'uploads'  # Pasta onde os arquivos recebidos serão salvos

# Cria a pasta 'uploads' caso não exista
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def main():
    # Cria o socket TCP/IP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Associa o socket ao endereço e porta
        s.bind((HOST, PORT))
        # Coloca o servidor em modo de escuta (aguarda conexões)
        s.listen()
        print(f"Servidor escutando em {HOST}:{PORT}...")

        # Aguarda conexão de um cliente
        conn, addr = s.accept()
        with conn:
            print(f"Conectado por {addr}")

            # Recebe o nome do arquivo (primeira mensagem)
            filename = conn.recv(1024).decode()
            if not filename:
                print("Erro: nome do arquivo não recebido.")
                return

            # Define o caminho completo onde o arquivo será salvo
            filepath = os.path.join(SAVE_DIR, filename)
            with open(filepath, 'wb') as f:
                print(f"Recebendo arquivo: {filename}")

                total_bytes = 0  # Contador de bytes recebidos
                while True:
                    # Recebe dados em pacotes (máx. 4096 bytes por vez)
                    data = conn.recv(4096)
                    if not data:
                        # Se não houver mais dados, encerra o loop
                        break
                    # Escreve os dados recebidos no arquivo
                    f.write(data)
                    total_bytes += len(data)

                # Exibe estatísticas do arquivo recebido
                print(f"Arquivo '{filename}' recebido com sucesso!")
                print(f"Tamanho total: {total_bytes} bytes")

# Executa a função principal
if __name__ == "__main__":
    main()
