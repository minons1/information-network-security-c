import socket
import sys
import pickle
from message import Message as msg

success_msg = (bytes('File sent successfully', 'utf-8'))
failed_msg = (bytes('File not found', 'utf-8'))

# create socket and connect to server
# server_address = ('192.168.100.186', 5000)
server_address = ('127.0.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

try:
    while True:
        message = sys.stdin.readline()
        # melakukan parsing untuk mendapatkan nama file
        message_split = message.split(' ',1)
        filename = message_split[1].rstrip("\n")

        # mengirimkan request filename ke server
        cmd = msg(text='unduh', filename=filename)
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
        print(type(data.key))
        print("Received message: " + data.message 
        + "\nfile name : " + data.filename 
        + "\nfilesize: " + data.filesize
        + "\niv:  " + str(data.iv))
        # membuat file dan mengisi data kedalam file
        # with open(filename, 'wb') as file:
        #     # Panjang pesan untuk membatasi loop recv sesuai ukuran file
        #     msg_len = message_header[1].decode('utf-8').split(" ")
        #     file_len = (int(msg_len[1][:-1])//1024) + 1
        #     print ('File dibuat')

        #     # mengirimkan file yang masuk ke recv_data (untuk memenuhi slot 1024 bytes sebelum
        #     # masuk ke variabel selanjutnya (data))
        #     file.write(message_header[4])
            
        #     while file_len:
        #         print('Menerima data...')
        #         data = client_socket.recv(1024)
        #         file.write(data)
        #         file_len-=1

        ## INTERRUPT DENGAN KEYBOARD UNTUK MENGHENTIKAN PROSES

        # file telah diterima
        print("File telah diterima\n")

except KeyboardInterrupt:
    client_socket.close()
    sys.exit(0)