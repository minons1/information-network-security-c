import socket
import os
import sys
import pickle
from message import Message as msg
import pyaes
import pbkdf2
import secrets
import time

# create socket and connect to server
server_address = ('127.0.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

try:
    while True:
        # Client Encryptor Setup
        password = "n3wPa55Cl13nt"
        passwordSalt = os.urandom(16)
        key_c = pbkdf2.PBKDF2(password, passwordSalt).read(32)
        iv_c = secrets.randbits(256)
        encryptor = pyaes.AESModeOfOperationCTR(key_c, pyaes.Counter(iv_c))

        # Input
        message = input()
        # melakukan parsing untuk mendapatkan nama file
        message_split = message.split(' ',1)
        filename = message_split[1].rstrip("\n")

        # mengirimkan request filename ke server
        filename = encryptor.encrypt(filename)
        cmd = msg(text='unduh', filename=filename, key=key_c, iv=iv_c)
<<<<<<< HEAD
=======
        
>>>>>>> 15df38435cb05b814ce70a6a94de3abd3fb72665
        client_socket.sendall(pickle.dumps(cmd))
        
        # Receive and load message
        res = b''
        while True:
            recv_data = client_socket.recv(2048)
            res += recv_data
            if len(recv_data) < 2048 - 1:
                break
        data = pickle.loads(res)
<<<<<<< HEAD
        
        if(data.message != 'file'):
            print(data.message)
            continue

        else:
            # Decryptor setup
            key = data.key
            iv = data.iv
            decryptor = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))

            # create and insert file data
            with open(data.filename, 'wb') as file:
                print ('File dibuat')
                # Decrypt the file and write to the file
                file.write(decryptor.decrypt(data.file))
=======
        key = data.key
        iv = data.iv
        decryptor = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))
        print(data.filename)
        print(data.filesize)
        time_start = time.time()
        print("CLIENT TIME START => ", time_start)
        # membuat file dan mengisi data kedalam file
        with open(data.filename, 'wb') as file:
            print ('File dibuat')
            # mengirimkan file yang masuk ke recv_data (untuk memenuhi slot 1024 bytes sebelum
            # masuk ke variabel selanjutnya (data))
            file.write(decryptor.decrypt(data.file))
        time_end = time.time()
        print("CLIENT TIME END => ", time_end)
        print("CLUENT EXECUTE TIME CONSUMED => ", time_end - time_start)
        ## INTERRUPT DENGAN KEYBOARD UNTUK MENGHENTIKAN PROSES
>>>>>>> 15df38435cb05b814ce70a6a94de3abd3fb72665

            # file accepted
            print("File telah diterima\n")

except KeyboardInterrupt:
    client_socket.close()
    sys.exit(0)