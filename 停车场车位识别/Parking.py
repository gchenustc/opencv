import os
from ParkingFunc import Parking
import glob
import matplotlib.pyplot as plt
import numpy as np
import cv2

cur_dir = os.getcwd()
path_test_images = f"data\\test_images\\"
video_name = 'parking_video.mp4'
test_images = [plt.imread(path) for path in glob.glob(path_test_images+"\\*.jpg")]
# plt.imshow(test_images[0])
park = Parking()

def imgProcess(images, park):
    # 筛选图像中需要的部分
    imgs_1 = list(map(park.select_useful, images))
    park.cv_show(imgs_1[0])
    # 灰度图
    imgs_2 = list(map(park.to_gray, imgs_1))
    park.cv_show(imgs_2[0])
    # Canny边缘检测
    imgs_3 = list(map(park.get_edge, imgs_2))
    park.cv_show(imgs_3[0])
    imgs_4 = list(map(park.select_region, imgs_3))
    park.cv_show(imgs_4[0])

imgProcess(test_images, park)