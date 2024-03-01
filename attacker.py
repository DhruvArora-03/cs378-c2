# import socket
# import subprocess

# HOST = '0.0.0.0'  # Listen on all network interfaces
# PORT = 12345  # Choose a port number
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((HOST, PORT))
# s.listen(1)
# print(f"Listening on {HOST}:{PORT}")
# conn, addr = s.accept()
# print(f"Connection from {addr}")

# while True:
#     command = input("Enter command to execute or 'exit' to quit: ")
#     if command.lower() == 'exit':
#         conn.send(b'exit')
#         conn.close()
#         break
#     conn.send(command.encode())
#     output = conn.recv(1024)
#     print(output.decode(), end="")
# s.close()

# from cryptography.hazmat.primitives import serialization
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.asymmetric import padding

# import socket
# import subprocess

# def load_private_key():
#     with open("private_key.pem", "rb") as key_file:
#         private_key = serialization.load_pem_private_key(
#             key_file.read(),
#             password=None,
#             backend=default_backend()
#         )
#     return private_key

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

# HOST = '10.0.2.6' # Listen on all network interfaces
# PORT = 12345  # Choose a port number
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((HOST, PORT))
# s.listen(1)
# print(f"Listening on {HOST}:{PORT}")
# conn, addr = s.accept()
# print(f"Connection from {addr}")

# private_key = load_private_key()

# while True:
#     command = input("Enter command to execute or 'exit' to quit: ")
#     if command.lower() == 'exit':
#         conn.send(b'exit')
#         conn.close()
#         break
#     conn.send(command.encode())
#     encrypted_output = conn.recv(1024)
#     output = decrypt_message(encrypted_output, private_key)
#     print(output, end="")
# s.close()


from cryptidy import asymmetric_encryption
import socket
import subprocess

HOST = '10.0.2.4' # Listen on all network interfaces
PORT = 12345  # Choose a port number
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
print(f"Listening on {HOST}:{PORT}")
conn, addr = s.accept()
print(f"Connection from {addr}")

priv_key, pub_key = asymmetric_encryption.generate_keys(2048)  # 2048 bits RSA key

while True:
    command = input("Enter command to execute or 'exit' to quit: ")
    if command.lower() == 'exit':
        conn.send(b'exit')
        conn.close()
        break
    conn.send(command.encode())
    encrypted_output = conn.recv(1024)
    output = asymmetric_encryption.decrypt_message(encrypted_output, priv_key)
    print(output, end="")
s.close()
