import struct
import os

def send_b(filepath, cli):
    #****************
    fhead = struct.pack(b'128sq', bytes(os.path.basename(filepath), encoding='utf-8'), os.stat(filepath).st_size)  #将图片以128sq的格式打包
    cli.send(fhead)
    fp = open(filepath, 'rb')
    while True:
        data = fp.read(1024)
        if not data:
            print('{0} send over...'.format(filepath))
            break
        cli.send(data)
    fp.close()
    #****************

    '''
    file = open(filepath,"rb")
    cli.sendall(file.read())
    file.close()
    '''