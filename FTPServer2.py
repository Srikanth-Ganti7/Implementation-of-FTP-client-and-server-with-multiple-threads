import socket
import os
import threading
import sys

CHUNK_SIZE = 1024
FILE_END_MARKER = b'ENDED'

def send_file(connection, file_path):
    with open(file_path, 'rb') as file:
        data_chunk = file.read(CHUNK_SIZE)
        while data_chunk:
            connection.send(data_chunk)
            data_chunk = file.read(CHUNK_SIZE)
    connection.send(FILE_END_MARKER)

def receive_file(connection, file_path):
    with open(file_path, 'wb') as file:
        while True:
            data_chunk = connection.recv(CHUNK_SIZE)
            if data_chunk.endswith(FILE_END_MARKER):
                data_chunk = data_chunk[:-len(FILE_END_MARKER)]
                file.write(data_chunk)
                break
            file.write(data_chunk)

def handle_get(connection, command):
    file_path = command.split()[1]
    if os.path.exists(file_path):
        connection.send(b'BEGIN')
        send_file(connection, file_path)
    else:
        connection.send(b'ERROR: File does not exist.')

def handle_upload(connection, command):
    file_path = "new" + command.split()[1]
    connection.send(b'READY')
    receive_file(connection, file_path)
    print(f'File {file_path} uploaded successfully.')

def handle_unknown(connection, _):
    connection.send(b'ERROR: Unknown command.')

def client_session(connection, address):
    print(f"Connected to {address}")
    command_handlers = {
        'get': handle_get,
        'upload': handle_upload,
    }

    try:
        while True:
            client_command = connection.recv(CHUNK_SIZE).decode()
            if not client_command:
                print(f"Client {address} disconnected, closing connection.")
                break

            action = client_command.split()[0].lower()
            if action == "quit":
                print(f"Quit command received from {address}, closing client connection.")
                break

            handler = command_handlers.get(action, handle_unknown)
            handler(connection, client_command)
    finally:
        connection.close()

def run_server():
    if len(sys.argv) < 2:
        print("Usage: python server.py <port>")
        sys.exit()

    port = int(sys.argv[1])
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind(('', port))
    except socket.error as e:
        print(f"Error binding to port {port}: {e}")
        return

    server_socket.listen(5)
    print(f'Server is running on port {port}')

    try:
        while True:
            client_connection, client_address = server_socket.accept()
            client_thread = threading.Thread(target=client_session, args=(client_connection, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        print("Server shutdown initiated...")
    finally:
        server_socket.close()
        print("Server has been shut down.")

if __name__ == '__main__':
    run_server()
