import socket
import os
import sys
import pickle
from message import Message as msg
from aes import CTR
import os
import pyaes
import pbkdf2
import secrets

# create socket and connect to server
server_address = ('127.0.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

try:
    while True:
        # Client Encryptor Setup
        key_c = os.urandom(16)
        iv_c = os.urandom(16)
        encryptor = CTR(key_c)

        # Input
        message = input()
        # melakukan parsing untuk mendapatkan nama file
        message_split = message.split(' ',1)
        filename = message_split[1].rstrip("\n")

        # mengirimkan request filename ke server
        filename = encryptor.encrypt_ctr(bytes(filename, 'utf-8'), iv_c)
        cmd = msg(text='unduh', filename=filename, key=key_c, iv=iv_c)
        client_socket.sendall(pickle.dumps(cmd))
        
        # Receive and load message
        res = b''
        while True:
            recv_data = client_socket.recv(2048)
            res += recv_data
            if len(recv_data) < 2048 - 1:
                break
        data = pickle.loads(res)
        
        if(data.message != 'file'):
            print(data.message)
            continue

        else:
            # Decryptor setup
            key = data.key
            iv = data.iv
            decryptor = CTR(key)

            # create and insert file data
            with open(data.filename, 'wb') as file:
                print ('File dibuat')
                # Decrypt the file and write to the file
                file.write(decryptor.decrypt_ctr(data.file, iv))

            # file accepted
            print("File telah diterima\n")

except KeyboardInterrupt:
    client_socket.close()
    sys.exit(0)