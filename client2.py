from client2_abenc import CPabe_BSW07

from charm.toolbox.pairinggroup import PairingGroup

from client2_getkey import getkey 

from client2_getEnc import getEnc

import numpy as np

from client2_DecImg import dec_img

import cv2

from pywt import idwt2

import os

from charm.core.engine.util import bytesToObject



#-----获取密钥和密文-----

print("获取密钥和密文......")



mark = input('请输入数据标记(3字节)：')

mark = mark.encode()



(pk, sk) = getkey(mark)

#返回密钥密文及小波系数密文

(ct, e_cA3, e_cH3, e_cV3, e_cD3, e_cH2, e_cV2, e_cD2, e_cH1, e_cV1, e_cD1) = getEnc(mark)



#-----解密图像-----

groupObj = PairingGroup('SS512')

cpabe = CPabe_BSW07(groupObj)



decsavePath = input('请输入解密的图像保存位置(/home/feng/桌面/图像访问者)--(bmp文件)：')

decsavePath = '/home/feng/桌面/图像访问者/' + decsavePath

'''

flag = {'lay1':0, 'lay2':0, 'lay3':0, 'lay4':0}

try:

    rec_msg1 = cpabe.decrypt(pk, sk, ct['ct1'])

    str_key1 = str(rec_msg1)

    k1_1 = ord(str_key1[1])

    k1_2 = ord(str_key1[2])

    flag['lay1'] = 1

except Exception as e:

    print(e)



finally:

    try:

        rec_msg2 = cpabe.decrypt(pk, sk, ct['ct2'])

        str_key2 = str(rec_msg2)

        k2_1 = ord(str_key2[1])

        k2_2 = ord(str_key2[2])

        flag['lay2'] = 1

    except Exception as e:

        print(e)



    finally:

        try:

            rec_msg3 = cpabe.decrypt(pk, sk, ct['ct3'])

            str_key3 = str(rec_msg3)

            k3_1 = ord(str_key3[1])

            k3_2 = ord(str_key3[2])

            flag['lay3'] = 1

            print('flag3:',flag['lay3'])

        except Exception as e:

            print(e)

        

        finally:

            try:

                rec_msg4 = cpabe.decrypt(pk, sk, ct['ct4'])

                str_key4 = str(rec_msg4)

                k4_1 = ord(str_key4[1])

                k4_2 = ord(str_key4[2])

                flag['lay4'] = 1

            except Exception as e:

                print(e)



            finally:

                print('flag:',flag['lay1'],flag['lay2'],flag['lay3'],flag['lay4'])

                if flag['lay1'] == 0 and flag['lay2'] == 0 and flag['lay3'] == 0 and flag['lay4'] == 0:

                    print('您没有权限解密图像！')

                    os._exit()



                if flag['lay1'] == 1:

                    dec_cA3 = dec_img(e_cA3, k1_1, k1_2)

                else:

                    dec_cA3 = None

                

                if flag['lay2'] == 1:

                    dec_cH3 = dec_img(e_cH3, k2_1, k2_2)

                    dec_cV3 = dec_img(e_cV3, k2_1, k2_2)

                    dec_cD3 = dec_img(e_cD3, k2_1, k2_2)

                else:

                    dec_cH3 = None

                    dec_cV3 = None

                    dec_cD3 = None



                if flag['lay3'] == 1:

                    dec_cH2 = dec_img(e_cH2, k3_1, k3_2)

                    dec_cV2 = dec_img(e_cV2, k3_1, k3_2)

                    dec_cD2 = dec_img(e_cD2, k3_1, k3_2)

                else:

                    dec_cH2 = None

                    dec_cV2 = None

                    dec_cD2 = None



                if flag['lay4'] == 1:

                    dec_cH1 = dec_img(e_cH1, k4_1, k4_2)

                    dec_cV1 = dec_img(e_cV1, k4_1, k4_2)

                    dec_cD1 = dec_img(e_cD1, k4_1, k4_2)

                else:

                    dec_cH1 = None

                    dec_cV1 = None

                    dec_cD1 = None



                #对图像进行重构



                CA2 = idwt2((dec_cA3,(dec_cH3, dec_cV3, dec_cD3)), 'haar')

                CA1 = idwt2((CA2,(dec_cH2, dec_cV2, dec_cD2)), 'haar')

                rimg = idwt2((CA1,(dec_cH1, dec_cV1, dec_cD1)), 'haar')



                cv2.imwrite(decsavePath, np.uint8(rimg))

                print('访问图像已保存至',decsavePath)

                cv2.imshow('rimg',np.uint8(rimg))

                cv2.waitKey()

'''

"""

try:

    rec_msg1 = cpabe.decrypt(pk, sk, ct['ct1'])

    str_key1 = str(rec_msg1)

    k1_1 = ord(str_key1[1])

    k1_2 = ord(str_key1[2])

    dec_cA3 = dec_img(e_cA3, k1_1, k1_2)

    print('here1')

except Exception as e:

    print(e)

    dec_cA3 = None

    print('here2')

finally:

    try:

        rec_msg2 = cpabe.decrypt(pk, sk, ct['ct2'])

        str_key2 = str(rec_msg2)

        k2_1 = ord(str_key2[1])

        k2_2 = ord(str_key2[2])

        dec_cH3 = dec_img(e_cH3, k2_1, k2_2)

        dec_cV3 = dec_img(e_cV3, k2_1, k2_2)

        dec_cD3 = dec_img(e_cD3, k2_1, k2_2)

        print('here3')

    except Exception as e:

        print(e)

        dec_cH3 = None

        dec_cV3 = None

        dec_cD3 = None

        print('here4')

    finally:

        try:

            rec_msg3 = cpabe.decrypt(pk, sk, ct['ct3'])

            str_key3 = str(rec_msg3)

            k3_1 = ord(str_key3[1])

            k3_2 = ord(str_key3[2])

            dec_cH2 = dec_img(e_cH2, k3_1, k3_2)

            dec_cV2 = dec_img(e_cV2, k3_1, k3_2)

            dec_cD2 = dec_img(e_cD2, k3_1, k3_2)       

        except Exception as e:

            print(e)

            dec_cH2 = None

            dec_cV2 = None

            dec_cD2 = None

        

        finally:

            try:

                rec_msg4 = cpabe.decrypt(pk, sk, ct['ct4'])

                str_key4 = str(rec_msg4)

                k4_1 = ord(str_key4[1])

                k4_2 = ord(str_key4[2])

                dec_cH1 = dec_img(e_cH1, k4_1, k4_2)

                dec_cV1 = dec_img(e_cV1, k4_1, k4_2)

                dec_cD1 = dec_img(e_cD1, k4_1, k4_2)

            except Exception as e:

                print(e)

                dec_cH1 = None

                dec_cV1 = None

                dec_cD1 = None



            finally:

                #对图像进行重构



                CA2 = idwt2((dec_cA3,(dec_cH3, dec_cV3, dec_cD3)), 'haar')

                CA1 = idwt2((CA2,(dec_cH2, dec_cV2, dec_cD2)), 'haar')

                rimg = idwt2((CA1,(dec_cH1, dec_cV1, dec_cD1)), 'haar')



                cv2.imwrite(decsavePath, np.uint8(rimg))

                print('访问图像已保存至',decsavePath)

                cv2.imshow('rimg',np.uint8(rimg))

                cv2.waitKey()

"""





rec_msg1 = cpabe.decrypt(pk, sk, ct['ct1'])

str_key1 = str(rec_msg1)

k1_1 = ord(str_key1[1])

k1_2 = ord(str_key1[2])

dec_cA3 = dec_img(e_cA3, k1_1, k1_2)



rec_msg2 = cpabe.decrypt(pk, sk, ct['ct2'])

str_key2 = str(rec_msg2)

k2_1 = ord(str_key2[1])

k2_2 = ord(str_key2[2])

dec_cH3 = dec_img(e_cH3, k2_1, k2_2)

dec_cV3 = dec_img(e_cV3, k2_1, k2_2)

dec_cD3 = dec_img(e_cD3, k2_1, k2_2)



rec_msg3 = cpabe.decrypt(pk, sk, ct['ct3'])

str_key3 = str(rec_msg3)

k3_1 = ord(str_key3[1])

k3_2 = ord(str_key3[2])

dec_cH2 = dec_img(e_cH2, k3_1, k3_2)

dec_cV2 = dec_img(e_cV2, k3_1, k3_2)

dec_cD2 = dec_img(e_cD2, k3_1, k3_2)       

   

rec_msg4 = cpabe.decrypt(pk, sk, ct['ct4'])

str_key4 = str(rec_msg4)

k4_1 = ord(str_key4[1])

k4_2 = ord(str_key4[2])

dec_cH1 = dec_img(e_cH1, k4_1, k4_2)

dec_cV1 = dec_img(e_cV1, k4_1, k4_2)

dec_cD1 = dec_img(e_cD1, k4_1, k4_2)

           

#对图像进行重构



CA2 = idwt2((dec_cA3,(dec_cH3, dec_cV3, dec_cD3)), 'haar')

CA1 = idwt2((CA2,(dec_cH2, dec_cV2, dec_cD2)), 'haar')

rimg = idwt2((CA1,(dec_cH1, dec_cV1, dec_cD1)), 'haar')



cv2.imwrite(decsavePath, np.uint8(rimg))

print('访问图像已保存至',decsavePath)

cv2.imshow('rimg',np.uint8(rimg))

cv2.waitKey()