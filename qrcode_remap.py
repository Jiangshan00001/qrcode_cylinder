import math
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

if __name__ == '__main__':
    #####################################

    # 原始二维码的输入图片:需要是xy像素数相等的，rgb三颜色图片
    file_name = 'pic/qrcode_for_gh_d6a716faac45_1280.jpg'
    #二维码尺寸：单位mm。是变换后的二维码的尺寸
    img_size = 10.0
    # 输出二维码图像的像素数（xy像素数相等）
    img_out_pixels = 1280  # 像素数
    # 要贴到的圆柱形物体的直径。单位mm
    circle_d = 14.0

    #####################################



    img = cv2.imread(file_name)
    cv2.imshow('img_org', img)
    img_in_pixels = img.shape[0]

    dpi = img_out_pixels / img_size * 25.4
    print('dpi', dpi)

    circle_r = circle_d / 2.0
    # 弧长=半径 * 弧度
    # 弧度=弧长/半径
    alpha1 = img_size / circle_r

    after_remap = circle_r * math.sin(alpha1 / 2.0) * 2
    print('after_remap', after_remap)

    # in:1280x1280
    # out:1280x1280

    img_out = np.zeros([img_out_pixels, img_out_pixels, 3], dtype=np.uint8)

    x_list = []
    y_list = []
    for i in range(img_out_pixels):
        # 每个像素做映射
        # 弧长
        len_mm = (img_out_pixels / 2 - i) / img_out_pixels * img_size
        # 弧度
        alphaA = len_mm / circle_r
        # 弦长
        x_mm = circle_r * math.sin(alphaA)
        # 弦上的像素
        pos_x_pixel = (after_remap / 2.0 - x_mm) * img_in_pixels / after_remap
        x_list.append(i)
        y_list.append(pos_x_pixel)
        for j in range(img_out_pixels):
            pos_y_pixel = j * img_in_pixels / img_out_pixels
            pos_y_pixel = int(pos_y_pixel)
            pos_x_pixel = int(pos_x_pixel)
            img_out[j, i] = img[pos_y_pixel, pos_x_pixel]

    cv2.imshow('img_out', img_out)

    img_diff = img_out - img
    cv2.imwrite('pic/diff.png', img_diff)

    img_out = cv2.cvtColor(img_out, cv2.COLOR_BGR2RGB)

    PILimage = Image.fromarray(img_out)
    PILimage.save('pic/result.png', dpi=(dpi, dpi))

    plt.plot(x_list, [y_list[i] - x_list[i] for i in range(len(y_list))])
    plt.savefig('pic/shift_pixel.png')


    #plt.show()
