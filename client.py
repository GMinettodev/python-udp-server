import socket
import os
import math

# Endereço do servidor (alterar se o servidor estiver em outro PC)
SERVER_HOST = '127.0.0.1'  # localhost
SERVER_PORT = 5000         # Porta deve ser a mesma do servidor

def enviar_arquivo(caminho_arquivo, tamanho_pacote=1024, max_pacotes=None):
    """
    Função que envia um arquivo para o servidor, em pacotes configuráveis.
    - caminho_arquivo: caminho completo do arquivo a ser enviado
    - tamanho_pacote: tamanho de cada pacote em bytes
    - max_pacotes: limite máximo de pacotes a enviar (opcional)
    """

    # Verifica se o arquivo existe
    if not os.path.exists(caminho_arquivo):
        print("Arquivo não encontrado!")
        return

    # Obtém o tamanho total do arquivo em bytes
    tamanho_total = os.path.getsize(caminho_arquivo)

    # Calcula o número total de pacotes necessários
    num_pacotes = math.ceil(tamanho_total / tamanho_pacote)

    # Se o usuário quiser limitar o envio, ajusta o número de pacotes
    if max_pacotes is not None:
        num_pacotes = min(num_pacotes, max_pacotes)

    # Exibe informações iniciais
    print(f"Enviando arquivo: {caminho_arquivo}")
    print(f"Tamanho total: {tamanho_total} bytes")
    print(f"Tamanho do pacote: {tamanho_pacote} bytes")
    print(f"Número de pacotes a enviar: {num_pacotes}")

    # Cria o socket TCP/IP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Conecta ao servidor
        s.connect((SERVER_HOST, SERVER_PORT))

        # Envia o nome do arquivo ao servidor
        s.sendall(os.path.basename(caminho_arquivo).encode())

        # Abre o arquivo em modo leitura binária
        with open(caminho_arquivo, 'rb') as f:
            total_enviado = 0  # Contador de bytes enviados

            # Envia o arquivo em pedaços (pacotes)
            for i in range(num_pacotes):
                # Lê um pedaço do arquivo do tamanho configurado
                chunk = f.read(tamanho_pacote)
                if not chunk:
                    # Fim do arquivo
                    break

                # Envia o pacote ao servidor
                s.sendall(chunk)
                total_enviado += len(chunk)

                # Mostra o progresso do envio
                print(f"Pacote {i+1}/{num_pacotes} enviado ({len(chunk)} bytes)")

        # Exibe resumo final
        print(f"\nEnvio concluído! Total enviado: {total_enviado} bytes")

# Executa a função principal
if __name__ == "__main__":
    # Pede as configurações ao usuário
    caminho = input("Caminho do arquivo a enviar: ").strip()
    pacote = int(input("Tamanho do pacote (bytes): ").strip() or 1024)
    limite = input("Número máximo de pacotes (deixe vazio para enviar tudo): ").strip()
    limite = int(limite) if limite else None

    # Chama a função principal de envio
    enviar_arquivo(caminho, tamanho_pacote=pacote, max_pacotes=limite)
