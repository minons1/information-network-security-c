<<<<<<< HEAD
import socket
import select
import sys
import os
import time

# define server address, create socket, bind, and listen
# server_address = ('192.168.100.186', 5000)
server_address = ('192.168.43.225', 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]

try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])

        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)
            
            else:
                # menerima nama file dari client dan memparsing nya untuk mendapatkan nama file
                recv_data = sock.recv(1024)
                data = recv_data.split(' '.encode(),1)
            
                if (data[0].decode('utf-8') != 'unduh'):
                    sock.send(bytes('Error', 'utf-8'))
                

                if recv_data and data[0].decode('utf-8') == 'unduh':
                    # mengambil nama file
                    filename = data[1].decode('utf-8').rstrip("\n")
                    print(sock.getpeername(), 'request', filename)
                    # membuka dan mengirim file
                    try:
                        with open("dataset/"+filename, 'rb') as file:
                            # mengirimkan message header ke client
                            filesize = str(os.path.getsize("dataset/"+filename))
                            message_header = "file-name: "+filename+",\nfile-size: "+filesize+",\n\n\n"
                            sock.send(bytes(message_header,'utf-8'))
                            # membaca dan mengirimkan isi file ke client
                            readfile = True
                            while (readfile):
                                readfile = file.read(1024)
                                sock.send(readfile)
                                # Sleep agar tidak ada loss package yang dikirim
                                # Tanpa sleep terlalu cepat(mungkin masalah hardware, bisa dicoba di device lain)
                                time.sleep(0.5)
                            
                            # file sudah berhasil dikirim
                            print ('File telah dikirim ke', sock.getpeername())

                    # menangkap error ketika membuka file atau yang lainnya
                    except OSError:
                        print ("Could not open/read file: ", filename)
                        sock.send(bytes('Error', 'utf-8'))
                        continue

                else:
                    sock.close()
                    input_socket.remove(sock)

                    
except KeyboardInterrupt:
    server_socket.close()
=======
import socket
import select
import sys
import os
import time
from message import Message as msg
import pickle
import pbkdf2
import secrets
import pyaes

# define server address, create socket, bind, and listen
# server_address = ('192.168.100.186', 5000)
server_address = ('127.0.0.1', 5000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]

password = "n3wPa55"
passwordSalt = os.urandom(16)
key = pbkdf2.PBKDF2(password, passwordSalt).read(32)
iv = secrets.randbits(256)
encryptor = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))

try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])

        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)
            
            else:
                # menerima nama file dari client dan memparsing nya untuk mendapatkan nama file
                recv_data = sock.recv(2048)
                data = recv_data.split(' '.encode(),1)
            
                if (data[0].decode('utf-8') != 'unduh'):
                    sock.send(bytes('Error', 'utf-8'))
                

                if recv_data and data[0].decode('utf-8') == 'unduh':
                    # mengambil nama file
                    filename = data[1].decode('utf-8').rstrip("\n")
                    print(sock.getpeername(), 'request', filename)
                    # membuka dan mengirim file
                    try:
                        with open("dataset"+filename, 'rb') as file:
                            # mengirimkan message header ke client
                            filesize = str(os.path.getsize("dataset/"+filename))
                            readfile = file.read()
                            messageToSent = msg(text='file',filename=filename, 
                                                filesize=filesize, key=key, iv=iv, doc=file)
                            sock.send(pickle.dump(messageToSent))
                            print ('File telah dikirim ke', sock.getpeername())

                    # menangkap error ketika membuka file atau yang lainnya
                    except OSError:
                        print ("Could not open/read file: ", filename)
                        sock.send(bytes('Error', 'utf-8'))
                        continue

                else:
                    sock.close()
                    input_socket.remove(sock)

                    
except KeyboardInterrupt:
    server_socket.close()
>>>>>>> 7b595a8fc83c7cad39680af001fe1f617273f497
    sys.exit(0)