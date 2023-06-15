'''
import glob
import math

import numpy as np
from skimage import io

#road1 = glob.glob("lena.bmp")  # 获取标准图像的文件路径
#standard = io.imread(road1[0])  # 读取标准图像文件
standard = io.imread("lena.bmp")  # 读取标准图像文件
standard = standard.astype(np.int32)  # 将 uint8类型的数据转换为int32类型便于后面运算
road2 = glob.glob("/home/feng/桌面/图像/*.bmp")  # 获取待评价图像的文件路径
m = len(road2)  # 获取待评价图像的数量
gray = 255  # 定义灰度范围值，方便后续计算
#strname = 'ans.txt'  # 定义一个文档名称，用于保存结果


# 定义函数calMSE，计算标准图像std与目标图像aim之间的均方误差(MSE)评价指标
def calMSE(std, aim):
    # 利用循环计算两幅影像间相同位置像素的灰度值的差的平方和
    num = 0
    for i in range(std.shape[0]):
        for j in range(std.shape[1]):
            num += math.pow(std[i, j] - aim[i, j], 2)
    mse = num / (std.shape[0] * std.shape[1])
    return mse


# 定义函数calPSNR，计算标准图像std与目标图像aim之间的峰值信噪比(PSNR)评价指标
def calPSNR(std, aim):
    num = 0
    for i in range(std.shape[0]):
        for j in range(std.shape[1]):
            num += (std[i, j] - aim[i, j]) * (std[i, j] - aim[i, j])
    mse = num / (std.shape[0] * std.shape[1])
    psnr = 10 * math.log(gray * gray / mse, 10)
    return psnr


#f = open(strname, "w")  # 打开文件
for i in range(m):
    img = io.imread(road2[i])  # 读取一张待评价的图片
    img = img.astype(np.int32)
    mse = calMSE(standard, img)  # 计算MSE指标
    psnr = calPSNR(standard, img)  # 计算PSNR指标
    name = '图像名称： ' + road2[i] + ',  MSE指标： ' + str(mse) + ',  PSNR指标： ' + str(psnr)
    print(str(name))  # 将结果字符串写入文件
    print('\n')  # 换行使文件中结果更加清楚
#f.close()  # 关闭文件
'''
from skimage.measure import compare_ssim, compare_psnr, compare_mse
import cv2

'''
img = cv2.imread('lena.bmp', 0)
#图像大小需要能被2的3次方 即8整除
img = cv2.resize(img,(320,320))
cv2.imwrite('/home/feng/桌面/图像/new.bmp',img)
'''

list1=["000enc.bmp","dec_5.bmp","dec_4.bmp","dec_3.bmp","dec_2.bmp","dec_1.bmp"]

for i in range(6):
    print(list1[i])
    img1 = cv2.imread("/home/feng/桌面/图像对比/"+list1[i])
    img2 = cv2.imread("/home/feng/桌面/图像对比/new.bmp")


    psnr = compare_psnr(img1, img2)
    ssim = compare_ssim(img1, img2, multichannel=True)  # 对于多通道图像(RGB、HSV等)关键词multichannel要设置为True
    mse = compare_mse(img1, img2)

    print('PSNR：{}，SSIM：{}，MSE：{}'.format(psnr, ssim, mse))
