import socket
import struct
import os
from recv_txt import recv_b
from send_txt import send_b
from server2_recv_img import recv_img

HOST = '127.0.0.1'
PORT = 6666

sk = socket.socket()
sk.bind((HOST, PORT))
sk.listen()
print("Wait for Connection.....................")
#filename = 'enc.bmp'
try:
    while True:
        cli,addr = sk.accept()
        print(addr)
        flag = cli.recv(1)
        #mark = cli.recv(3).decode('utf-8')
        if flag.decode('utf-8') == '1': #接收用户上传的图像密文，密钥密文
            mark = cli.recv(3).decode('utf-8')

            recv_img(cli, mark + 'enc.bmp')
            
            #************************
            recv_b(cli, '/home/feng/桌面/云服务器/' + mark+'byte_ct.txt')
            #************************


        elif flag.decode('utf-8') == '2': #发送用户需要的密文图像，密钥密文
            mark = cli.recv(3).decode('utf-8')

            filepath = '/home/feng/桌面/云服务器/' + mark + 'enc.bmp'
            fhead = struct.pack(b'128sq', bytes(os.path.basename(filepath),encoding = 'utf-8'),os.stat(filepath).st_size) #将图片以128sq的格式打包
            cli.send(fhead)

            fp = open(filepath, 'rb')
            while True:
                data = fp.read(1024)
                if not data:
                    print('{0} send over...'.format(filepath))
                    break
                cli.send(data)
            fp.close()

            #************************
            send_b('/home/feng/桌面/云服务器/' + mark+'byte_ct.txt', cli)
            #************************

        elif flag.decode('utf-8') == '3': 
            mark = cli.recv(3).decode('utf-8')
            recv_b(cli, '/home/feng/桌面/云服务器/' + mark+'byte_ct.txt')

        cli.close()

except Exception as e:
    print(e)
    
finally:
    sk.close()