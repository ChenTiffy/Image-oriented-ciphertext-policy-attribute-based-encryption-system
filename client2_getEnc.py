import socket
from charm.core.engine.util import bytesToObject
from charm.toolbox.pairinggroup import PairingGroup
from client2_recv_img import recv_img
from recv_txt import recv_b
import cv2
from pywt import dwt2

HOST = '127.0.0.1'
PORT = 6666

cli = socket.socket()

def getEnc(mark):
    cli.connect((HOST, PORT))
    cli.send('2'.encode())
    cli.send(mark)

    #接收密文图像，并对图像做小波分解
    filename = recv_img(cli)
    enc_img = cv2.imread(filename, 0)
    e_cA1,(e_cH1, e_cV1, e_cD1) = dwt2(enc_img, 'haar')
    e_cA2,(e_cH2, e_cV2, e_cD2) = dwt2(e_cA1, 'haar')
    e_cA3,(e_cH3, e_cV3, e_cD3) = dwt2(e_cA2, 'haar')

    #***********************
    recv_b(cli, '/home/feng/桌面/图像访问者/' + mark.decode('utf-8') + 'byte_ct.txt')

    with open('/home/feng/桌面/图像访问者/' + mark.decode('utf-8') + 'byte_ct.txt', 'rb') as f:
        byte_ct = f.read()
    groupObj = PairingGroup("SS512")
    ct = bytesToObject(byte_ct, groupObj)
    #***********************
  
    cli.close()
    return (ct, e_cA3, e_cH3, e_cV3, e_cD3, e_cH2, e_cV2, e_cD2, e_cH1, e_cV1, e_cD1)