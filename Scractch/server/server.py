import socket
import select
import sys
import os
from message import Message as msg
import pickle
from aes import CTR
import os

# define server address, create socket, bind, and listen
server_address = ('127.0.0.1', 5000)
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
                # Encryptor Set-up
                key = os.urandom(16)
                iv = os.urandom(16)
                encryptor = CTR(key)

                # Receive & load request message from client
                recv_data = sock.recv(2048)
                data = pickle.loads(recv_data)

                # Decryptor setup
                key_c = data.key
                iv_c = data.iv
                decryptor = CTR(key_c)

                # decrypt filename requested from client
                data.filename = decryptor.decrypt_ctr(data.filename, data.iv)

                if (data.message != 'unduh'):
                    messageToSent = msg('Command not found',filename=None)
                    sock.sendall(pickle.dumps(messageToSent))
                

                if data and data.message == 'unduh':
                    # get filename
                    filename = (data.filename).decode('utf-8')
                    print(sock.getpeername(), 'request', filename)
                    # open and send file as requested
                    try:
                        with open("dataset/"+filename, 'rb') as file:
                            filesize = str(os.path.getsize("dataset/"+filename))
                            readfile = file.read()

                            readfile = encryptor.encrypt_ctr(readfile, iv)
                            messageToSent = msg('file',filename=filename, 
                                                filesize=filesize, key=key, iv=iv, doc=readfile)
                            sock.sendall(pickle.dumps(messageToSent))
                            print ('File telah dikirim ke', sock.getpeername())

                    # handle file error
                    except OSError:
                        print ("Could not open/read file: ", filename)
                        messageToSent = msg('File not found',filename=None)
                        sock.sendall(pickle.dumps(messageToSent))
                        continue

                else:
                    sock.close()
                    input_socket.remove(sock)

                    
except KeyboardInterrupt:
    server_socket.close()
    sys.exit(0)