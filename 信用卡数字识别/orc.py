import numpy as np
import cv2
import argparse
from imutils import contours # ? 
import os
cur_dir = os.path.dirname(__file__)

#
def sort_contours(cnts, method="left-to-right"):
    boundingBoxes = [cv2.boundingRect(c) for c in cnts] #用一个最小的矩形，把找到的形状包起来x,y,h,w
    # print(boundingBoxes)
    temp1 = zip(cnts, boundingBoxes)
    # print(np.array(list(temp1)).shape) # (10,2)
    # print(np.array(list(temp1))[0][0].shape) # (32,1,2)
    # print(np.array(list(temp1))[0][1]) # (730, 20, 54, 85)
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][0], reverse=False))
    return cnts, boundingBoxes

# 绘图展示
def cv_show(img):
    cv2.imshow("image",img)
    cv2.waitKey()
    cv2.destroyAllWindows()

# 设置参数
ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,help="path for input image")
ap.add_argument("-t","--template",required=True,help="path for template image")
args = vars(ap.parse_args("-i images/credit_card_01.png,\
                          -t images/ocr_a_reference.png".split()))
# 模板图像
img_tem = cv2.imread(args["template"])
# cv_show(img_tem)
# 模板灰度图像
img_tem_gray = cv2.cvtColor(img_tem, cv2.COLOR_BGR2GRAY)
# 模板二值图像
img_tem_thresh = cv2.threshold(img_tem_gray, 20, 255, cv2.THRESH_BINARY_INV)[1]
# cv_show(img_tem_thresh)
# 寻找和绘制轮廓
ref_contours = cv2.findContours(img_tem_thresh, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)[1]
cv2.drawContours(img_tem, ref_contours, -1, (0,0,255), 3)
# print(np.array(ref_contours).shape) # (10,)
# print(np.array(ref_contours)[0].squeeze().shape) # (32,2)

ref_contours = sort_contours(ref_contours)[0]



