import numpy as np



def dearnold(img, a, b):

    r, c = img.shape

    p = np.zeros((r, c))

    for i in range(r):

        for j in range(c):

            x = ((a * b + 1) * i - b * j) % r

            y = (-a * i + j) % c

            p[x, y] = img[i, j]

    return p



def dec_img(img, key1, key2):

    for i in range(8):

        img = dearnold(img, key1, key2)

    return img