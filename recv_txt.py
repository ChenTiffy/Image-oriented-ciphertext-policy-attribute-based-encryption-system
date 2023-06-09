import struct
import os

def recv_b(cli, savepath):
    #********************
    fileinfo_size = struct.calcsize('128sq')
    buf = cli.recv(fileinfo_size)   #接收图片名
    if buf:
        filename, file_size = struct.unpack('128sq', buf)
        filename = filename.decode().strip('\x00')
        #print("接收文件大小：", file_size)
        print(filename,'has been received...')
        f = open(savepath, 'wb')
        recvd_size = 0
        while not recvd_size == file_size:
            if file_size - recvd_size > 1024:
                data = cli.recv(1024)
                recvd_size += len(data)
            else:
                data = cli.recv(file_size - recvd_size)
                recvd_size = file_size
            f.write(data)  #写入图片数据
        f.close()
        #print('实际接收大小：', recvd_size)
    #********************

    '''
    print("start......")
    total_data = b''
    num = 0
    data = cli.recv(1024)
    total_data += data
    num =len(data)
    # 如果没有数据了，读出来的data长度为0，len(data)==0
    while len(data)>0:
        data = cli.recv(1024)
        num +=len(data)
        total_data += data       
    with open(savepath,"wb") as f:
        f.write(total_data)
    print('end......')
    '''