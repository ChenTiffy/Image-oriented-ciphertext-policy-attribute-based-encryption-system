import socket
from send_txt import send_b
from send_img import sendimg

HOST = '127.0.0.1'
PORT = 6666

cli = socket.socket()

def send_ct(mark):
    try:
        cli.connect((HOST, PORT))
        cli.send('3'.encode())
        cli.send(mark)
        send_b(mark.decode('utf-8') + 'byte_ct.txt', cli) 
            
    finally:
        cli.close()