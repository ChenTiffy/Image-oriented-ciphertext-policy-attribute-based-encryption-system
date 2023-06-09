import struct

import os

from send_txt import send_b



def sendimg(cli, filepath):

    #-----发送密文图片-----

    #filepath = input('请输入需要上传至服务器的图片：')   #输入当前目录下的图片名 

    fhead = struct.pack(b'128sq', bytes(os.path.basename(filepath), encoding='utf-8'), os.stat(filepath).st_size)  #将图片以128sq的格式打包

    cli.send(fhead)



    fp = open(filepath, 'rb')  #打开要传输的图片

    while True:

        data = fp.read(1024) #读入图片数据

        if not data:

            print('{0} send over...'.format(filepath))

            break

        cli.send(data)  #以二进制格式发送图片数据

    fp.close()



    """

    #-----发送密钥密文-----

    #****************

    send_b(mark.decode('utf-8') + 'byte_ct.txt', cli) 

    #*****************

    """