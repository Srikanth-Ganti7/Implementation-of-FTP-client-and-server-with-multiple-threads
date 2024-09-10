
# CNT 5106 - Computer Networks - Project 2

## Implementation of FTP client and server with multiple threads

This project consists of a simple FTP server and multiple clients that can handle basic file transfer operations such as uploading and downloading files with multiple threads. 



## Authors

**Name**: Balasai Srikanth Ganti

**UFID** : 5251-6075



## Running the Server

To run the server, execute the following command in cmd prompt:
- `python FTPServer2.py <Server_port>`


## Running the Client

To run the Client, execute the following command in cmd promt :
- `python FTPClient2.py <Server_port>`

This can be done with multiple clients

Here the port number is mentioned as **same as mentioned for server in server cmd prompt**

### Commands

The server listens for client connections and handles each client session in a separate thread. It supports the following commands:

- `get <filename>`: Downloads a file from the server.
- `upload <filename>`: Uploads a file to the server.
- `quit`: Exits Server connection and terminates both Client and Server.

### Notes
- The server creates a new file with a new prefix for uploaded files to avoid overwriting existing files.
- The client creates a new file with a new prefix for downloaded files.
- Both the server and client use a chunk size of 1024 bytes for file transfer.






