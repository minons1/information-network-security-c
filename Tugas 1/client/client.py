import socket
import os
import sys
import pickle
from message import Message as msg
import pyaes
import pbkdf2
import secrets

success_msg = (bytes('File sent successfully', 'utf-8'))
failed_msg = (bytes('File not found', 'utf-8'))

# create socket and connect to server
# server_address = ('192.168.100.186', 5000)
server_address = ('127.0.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

password = "n3wPa55Cl13nt"
passwordSalt = os.urandom(16)
key_c = pbkdf2.PBKDF2(password, passwordSalt).read(32)
iv_c = secrets.randbits(256)
encryptor = pyaes.AESModeOfOperationCTR(key_c, pyaes.Counter(iv_c))

key         = None
iv          = None
decryptor   = None

try:
    while True:
        message = sys.stdin.readline()
        # melakukan parsing untuk mendapatkan nama file
        message_split = message.split(' ',1)
        filename = message_split[1].rstrip("\n")

        # mengirimkan request filename ke server
        filename = encryptor.encrypt(filename)
        cmd = msg(text='unduh', filename=filename, key=key_c, iv=iv_c)
        

        client_socket.sendall(pickle.dumps(cmd))
        
        res = b''
        while True:
            recv_data = client_socket.recv(2048)
            res += recv_data
            print(":sekali")
            if len(recv_data) < 2048 - 1:
                print("break")
                break
        
        data = pickle.loads(res)
        key = data.key
        iv = data.iv
        decryptor = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))
        print(data.filename)
        print(data.filesize)

        # membuat file dan mengisi data kedalam file
        with open(data.filename, 'wb') as file:
            print ('File dibuat')
            # mengirimkan file yang masuk ke recv_data (untuk memenuhi slot 1024 bytes sebelum
            # masuk ke variabel selanjutnya (data))
            file.write(decryptor.decrypt(data.file))

        ## INTERRUPT DENGAN KEYBOARD UNTUK MENGHENTIKAN PROSES

        # file telah diterima
        print("File telah diterima\n")

except KeyboardInterrupt:
    client_socket.close()
    sys.exit(0)