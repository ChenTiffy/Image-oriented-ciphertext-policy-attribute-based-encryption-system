from pywt import dwt2,idwt2

import cv2

from client1_Key import keyGen

from client1_EncImg import enc_img

from charm.core.engine.util import objectToBytes

from charm.toolbox.pairinggroup import PairingGroup

from client2_DecImg import dec_img

import numpy as np



def img_deal(mark, pk):

    img_path = input('请输入需要分层的图像（分三层）：')

    img = cv2.imread(img_path, 0)

    #图像大小需要能被2的3次方 即8整除

    img = cv2.resize(img,(320,320))

    cv2.imwrite("/home/feng/桌面/图像对比/new.bmp",img)

    #小波变换将图像分解为三层

    cA1, (cH1, cV1, cD1) = dwt2(img, 'haar')  

    cA2, (cH2, cV2, cD2) = dwt2(cA1, 'haar')  

    cA3, (cH3, cV3, cD3) = dwt2(cA2, 'haar')



    #产生四组密钥，使用密钥分别加密一个低频信号和九个高频信号

    #对密钥进行属性加密，密钥密文为ct

    access_policy1 = input('请输入低频系数的访问策略：')

    (k1_1, k1_2, ct1, rand_msg1) = keyGen(access_policy1, pk)

    enc_cA3 = enc_img(cA3, k1_1, k1_2)





    access_policy2 = input('请输入第三层高频系数的访问策略：')

    (k2_1, k2_2, ct2, rand_msg2) = keyGen(access_policy2, pk)

    enc_cH3 = enc_img(cH3, k2_1, k2_2)

    enc_cV3 = enc_img(cV3, k2_1, k2_2)

    enc_cD3 = enc_img(cD3, k2_1, k2_2)



    access_policy3 = input('请输入第二层高频系数的访问策略：')

    (k3_1, k3_2, ct3, rand_msg3) = keyGen(access_policy3, pk)

    enc_cH2 = enc_img(cH2, k3_1, k3_2)

    enc_cV2 = enc_img(cV2, k3_1, k3_2)

    enc_cD2 = enc_img(cD2, k3_1, k3_2)



    access_policy4 = input('请输入第一层高频系数的访问策略：')

    (k4_1, k4_2, ct4, rand_msg4) = keyGen(access_policy4, pk)

    enc_cH1 = enc_img(cH1, k4_1, k4_2)

    enc_cV1 = enc_img(cV1, k4_1, k4_2)

    enc_cD1 = enc_img(cD1, k4_1, k4_2)



    ct = {'ct1':ct1, 'ct2':ct2, 'ct3':ct3, 'ct4':ct4}

    groupObj = PairingGroup('SS512')

    byte_ct = objectToBytes(ct, groupObj)

    with open(mark + 'byte_ct.txt', 'wb') as f:

        f.write(byte_ct)

    print('密钥密文已保存至文件', mark + 'byte_ct.txt')



    #对加密后的信号进行重构

    enc_3 = idwt2((enc_cA3,(enc_cH3,enc_cV3,enc_cD3)),'haar')

    enc_2 = idwt2((enc_3,(enc_cH2,enc_cV2,enc_cD2)),'haar')

    enc_1 = idwt2((enc_2,(enc_cH1,enc_cV1,enc_cD1)),'haar')

    

    '''

    #test

    e_cA1,(e_cH1, e_cV1, e_cD1) = dwt2(enc_1, 'haar')

    e_cA2,(e_cH2, e_cV2, e_cD2) = dwt2(e_cA1, 'haar')

    e_cA3,(e_cH3, e_cV3, e_cD3) = dwt2(e_cA2, 'haar')

    dec_cA3 = dec_img(e_cA3, k1_1, k1_2)

    dec_cH3 = dec_img(e_cH3, k2_1, k2_2)

    dec_cV3 = dec_img(e_cV3, k2_1, k2_2)

    dec_cD3 = dec_img(e_cD3, k2_1, k2_2)

    dec_cH2 = dec_img(e_cH2, k3_1, k3_2)

    dec_cV2 = dec_img(e_cV2, k3_1, k3_2)

    dec_cD2 = dec_img(e_cD2, k3_1, k3_2)

    dec_cH1 = dec_img(e_cH1, k4_1, k4_2)

    dec_cV1 = dec_img(e_cV1, k4_1, k4_2)

    dec_cD1 = dec_img(e_cD1, k4_1, k4_2)

    #对图像进行重构

    CA2 = idwt2((dec_cA3,(dec_cH3, dec_cV3, dec_cD3)), 'haar')

    CA1 = idwt2((CA2,(dec_cH2, dec_cV2, dec_cD2)), 'haar')

    rimg = idwt2((CA1,(dec_cH1, dec_cV1, dec_cD1)), 'haar')

    cv2.imshow('rimg',np.uint8(rimg))

    cv2.waitKey()

    '''

    

    #保存图像密文

    cv2.imwrite(mark + 'enc.bmp', enc_1)

    print('图像密文已保存至文件', mark + 'enc.bmp')



    #保存pk, rand_msg

    GT_key = {'pk': pk, 'GT_key1': rand_msg1, 'GT_key2': rand_msg2, 'GT_key3': rand_msg3, 'GT_key4': rand_msg4}

    byte_GT_key = objectToBytes(GT_key, groupObj)

    with open(mark + 'byte_GT_key.txt', 'wb') as f:

        f.write(byte_GT_key)

    print('GT_key已保存至文件', mark + 'byte_GT_key.txt')