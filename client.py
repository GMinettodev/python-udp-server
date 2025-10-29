import socket
import os
import sys

def enviar_arquivo(arquivo, servidor, porta, tamanho_pacote):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    tamanho_arquivo = os.path.getsize(arquivo)
    num_pacotes = (tamanho_arquivo + tamanho_pacote - 1) // tamanho_pacote

    print(f"Enviando '{arquivo}' para {servidor}:{porta}")
    print(f"Tamanho do arquivo: {tamanho_arquivo} bytes")
    print(f"Tamanho do pacote: {tamanho_pacote} bytes")
    print(f"Número de pacotes: {num_pacotes}\n")

    with open(arquivo, 'rb') as f:
        pacote_id = 1
        while True:
            dados = f.read(tamanho_pacote)
            if not dados:
                break

            sock.sendto(dados, (servidor, porta))
            print(f"Enviado pacote {pacote_id}/{num_pacotes} ({len(dados)} bytes)")
            pacote_id += 1

    # Envia marcador de fim
    sock.sendto(b'FIM', (servidor, porta))
    sock.close()
    print("\nArquivo enviado com sucesso!")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Uso: python3 client.py <arquivo> <servidor> <porta> <tamanho_pacote>")
        sys.exit(1)

    arquivo = sys.argv[1]
    servidor = sys.argv[2]
    porta = int(sys.argv[3])
    tamanho_pacote = int(sys.argv[4])

    enviar_arquivo(arquivo, servidor, porta, tamanho_pacote)
