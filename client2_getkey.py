import socket
from charm.core.engine.util import bytesToObject
from charm.toolbox.pairinggroup import PairingGroup
from recv_txt import recv_b
import json

HOST = '127.0.0.1'
PORT = 8088

cli = socket.socket()

def getkey(mark):
    cli.connect((HOST,PORT))
    cli.send('2'.encode())
    cli.send(mark)
  
    #发送属性给授权中心
    attrs = input("请输入属性(以空格分隔)：").split()
    attrs = list(attrs)
    json_attr1 = json.dumps(attrs)
    cli.send(json_attr1.encode())

    savepath = '/home/feng/桌面/图像访问者/' + mark.decode('utf-8') + 'Bytes_content.txt'
    recv_b(cli, savepath)
    with open(savepath, 'rb') as f:
        content = f.read()
    
    group = PairingGroup("SS512")
    bytes_content = bytesToObject(content, group)
    sk = bytes_content['sk']
    pk = bytes_content['pk']

    cli.close()

    return (pk,sk)