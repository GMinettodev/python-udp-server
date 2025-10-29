import socket

# Configurações
HOST = '0.0.0.0'   # escuta em todas as interfaces
PORT = 5000
OUTPUT_FILE = 'recebido.bin'

# Cria socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

print(f"Servidor escutando em {HOST}:{PORT}")
print("Aguardando dados...\n")

with open(OUTPUT_FILE, 'wb') as f:
    while True:
        data, addr = sock.recvfrom(4096)
        
        # Se o cliente enviar a palavra 'FIM', termina a recepção
        if data == b'FIM':
            print(f"\nTransferência concluída de {addr}")
            break

        f.write(data)
        print(f"Recebido pacote de {len(data)} bytes de {addr}")

sock.close()
print(f"Arquivo salvo como {OUTPUT_FILE}")
