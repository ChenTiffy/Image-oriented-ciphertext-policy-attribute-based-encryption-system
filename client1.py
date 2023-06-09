from client1_abenc import CPabe_BSW07
from charm.core.engine.util import objectToBytes, bytesToObject
from client1_server1 import send_content
from client1_server2 import send_enc
from charm.toolbox.pairinggroup import PairingGroup
from client1_send_ct import send_ct

print('1、上传图像密文、密钥密文、公钥、主密钥\n2、更新访问策略\n')
choice = input('请选择：')

if choice == '1':
    mark = input('请输入数据标记(3字节)：')
    #-----上传公钥PK，主密钥MK至授权中心-----
    mark = send_content(mark)

    #-----上传图像密文enc.bmp至云服务器-----
    send_enc(mark.decode('utf-8'))
    

elif choice == '2':
    mark = input('请输入数据标记(3字节)：')
    choice = input('请输入需要修改第几层图像的访问策略（1-4）：')
    
    access_policy = input('请输入访问策略：')
    groupObj = PairingGroup('SS512')
    cpabe = CPabe_BSW07(groupObj)
    with open(mark + 'byte_GT_key.txt', 'rb') as f:
        byte_msg = f.read()
    msg = bytesToObject(byte_msg, groupObj)
    pk = msg['pk']
    GT_key1 = msg['GT_key1']
    GT_key2 = msg['GT_key2']
    GT_key3 = msg['GT_key3']
    GT_key4 = msg['GT_key4']

    with open(mark + 'byte_ct.txt', 'rb') as f:
        byte_ct = f.read()
    ct = bytesToObject(byte_ct,groupObj)
    ct1 = ct['ct1']
    ct2 = ct['ct2']
    ct3 = ct['ct3']   
    ct4 = ct['ct4']   
    
    if choice == '1':
        ct1 = cpabe.encrypt(pk, GT_key1, access_policy)
    elif choice == '2':
        ct2 = cpabe.encrypt(pk, GT_key2, access_policy)
    elif choice == '3':
        ct3 = cpabe.encrypt(pk, GT_key3, access_policy)
    elif choice == '4':
        ct4 = cpabe.encrypt(pk, GT_key4, access_policy)
    
    ct = {'ct1':ct1, 'ct2':ct2, 'ct3':ct3, 'ct4':ct4}
    byte_ct = objectToBytes(ct, groupObj)
    with open(mark + 'byte_ct.txt','wb') as f:
        f.write(byte_ct)

    #-----上传cpabe加密的密钥至服务器-----
    send_ct(mark.encode('utf-8'))
        

