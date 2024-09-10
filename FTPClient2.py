import socket
import sys

CHUNK_SIZE = 1024
FILE_END_MARKER = b'ENDED'

def upload_file(client_socket, filename):
    try:
        client_socket.send(f'upload {filename}'.encode())
        response = client_socket.recv(CHUNK_SIZE)
        if response == b'READY':
            with open(filename, 'rb') as f:
                chunk = f.read(CHUNK_SIZE)
                while chunk:
                    client_socket.send(chunk)
                    chunk = f.read(CHUNK_SIZE)
            client_socket.send(FILE_END_MARKER)
            print(f'File {filename} has been successfully uploaded.')
        else:
            print('Upload failed')
    except FileNotFoundError:
        print(f'File {filename} not found.')

def download_file(client_socket, filename):
    client_socket.send(f'get {filename}'.encode())
    response = client_socket.recv(CHUNK_SIZE)
    if response == b'BEGIN':
        with open(f'new{filename}', 'wb') as f:
            while True:
                chunk = client_socket.recv(CHUNK_SIZE)
                if chunk.endswith(FILE_END_MARKER):
                    chunk = chunk[:-len(FILE_END_MARKER)]
                    f.write(chunk)
                    break
                f.write(chunk)
        print(f'File {filename} has been successfully downloaded as new{filename}.')
    elif response.startswith(b'ERROR'):
        print(f'Error: {response.decode()[6:]}')

def main():
    if len(sys.argv) < 2:
        print("Usage: python ftpclient.py <port>")
        return

    port = int(sys.argv[1])
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(('localhost', port))
    except ConnectionRefusedError:
        print("Failed to connect to the server.")
        return

    while True:
        command = input("Enter command (upload <filename> / get <filename> / quit): ")
        if command.startswith("upload"):
            _, filename = command.split()
            upload_file(client_socket, filename)
        elif command.startswith("get"):
            _, filename = command.split()
            download_file(client_socket, filename)
        elif command == "quit":
            client_socket.send(command.encode())
            break
        else:
            print("Invalid command. Please use 'upload <filename>', 'get <filename>', or 'quit'.")

    client_socket.close()

if __name__ == '__main__':
    main()
