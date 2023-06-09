import numpy as np

def arnold(img, a, b):

    r, c = img.shape

    p = np.zeros((r, c))

    for i in range(r):

        for j in range(c):

            x = (i + b * j) % r

            y = (a * i + (a * b + 1) * j) % c

            p[x, y] = img[i, j]

    return p



def enc_img(img, key1, key2):

    for i in range(8):

        img = arnold(img, key1, key2)

    return img