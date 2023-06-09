import struct
import os
def recv_img(cli):
    fileinfo_size = struct.calcsize('128sq')
    buf = cli.recv(fileinfo_size)   #接收图片名
    if buf:
        filename, filesize = struct.unpack('128sq', buf)
        fn = filename.decode().strip('\x00')
        print(fn,'has been received...')
        new_filename = os.path.join('/home/feng/桌面/图像访问/', fn)  

        recvd_size = 0
        fp = open(new_filename, 'wb')

        while not recvd_size == filesize:
            if filesize - recvd_size > 1024:
                data = cli.recv(1024)
                recvd_size += len(data)
            else:
                data = cli.recv(filesize - recvd_size)
                recvd_size = filesize
            fp.write(data)  #写入图片数据
        fp.close()
    return new_filename