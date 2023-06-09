import socket

import json

from send_txt import send_b

from recv_txt import recv_b

from client2_abenc import CPabe_BSW07

from charm.toolbox.pairinggroup import PairingGroup

from charm.core.engine.util import bytesToObject, objectToBytes



HOST = '127.0.0.1'

PORT = 8088

sk1 = socket.socket()

sk1.bind((HOST, PORT))

sk1.listen()

print("Wait for Connection.....................")

dict1 = {}

try:

    while True:

        cli, addr = sk1.accept()

        print(addr)

        flag = cli.recv(1)

        

        if flag.decode('utf-8') == '1': #接收用户上传的pk，mk

            while True: #接收用户上传的数据标记，判断标记是否已使用

                mark = cli.recv(3).decode('utf-8')

                if mark in dict1:

                    cli.send(b'0')

                else:

                    cli.send(b'1')

                    dict1[mark] = mark

                    break

            #print('-------------mark:',mark)

            savepath = '/home/feng/桌面/授权中心/' + mark+'Bytes_content.txt'

            #print("-------------savepath:",savepath)

            recv_b(cli, savepath)





        elif flag.decode('utf-8') == '2': #发送sk,pk

            mark = cli.recv(3).decode('utf-8')

            filepath = '/home/feng/桌面/授权中心/' + mark+'Bytes_content.txt'

            with open(filepath, 'rb') as f:

                content = f.read()

            group = PairingGroup("SS512")

            bytes_content = bytesToObject(content, group)

            pk = bytes_content['pk']

            mk = bytes_content['mk']

            

            groupObj = PairingGroup('SS512')

            cpabe = CPabe_BSW07(groupObj)



            json_attrs = cli.recv(1024).decode('utf-8')

            attrs = json.loads(json_attrs)

            sk = cpabe.keygen(pk, mk, attrs)



            send_content = {'pk':pk, 'sk':sk}

            Bytes_send_content = objectToBytes(send_content, groupObj)

            filepath = '/home/feng/桌面/授权中心/' + mark+'Bytes_send_content.txt'

            with open(filepath, 'wb') as f:

                f.write(Bytes_send_content)

            send_b(filepath, cli)



        cli.close()



except Exception as e:

    print(e)



finally:

    sk1.close()