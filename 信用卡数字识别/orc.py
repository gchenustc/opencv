import numpy as np
import cv2
import argparse
from imutils import contours # ? 
import os
cur_dir = os.path.dirname(__file__)

#
def sort_contours(cnts, method="left-to-right"):
    reverse = False
    i = 0 # i=0：把contours的方框按照从x轴排列，i=1则按照y轴排列
    boundingBoxes = [cv2.boundingRect(c) for c in cnts] #用一个最小的矩形，把找到的形状包起来x,y,h,w
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1
    # print(boundingBoxes)
    # temp1 = zip(cnts, boundingBoxes)
    # print(np.array(list(temp1)).shape) # (10,2)
    # print(np.array(list(temp1))[0][0].shape) # (32,1,2)
    # print(np.array(list(temp1))[0][1]) # (730, 20, 54, 85)
    # print(list(zip(*temp2))[0])
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))
    return cnts, boundingBoxes

# 按照比例扩大和缩小 
def resize(img, width=None, height=None):
    size = None
    h,w = img.shape[:2] # 原高和宽
    if not (width or height):
        return img
    if width:
        ratio = width / float(w)
        h_new = ratio * h
        size = (width, int(h_new))
    else:
        ratio = height / float(h)
        w_new = ratio * w
        size = (int(w_new), height)
    return cv2.resize(img, size, interpolation=cv2.INTER_AREA)
        
    
# 绘图展示
def cv_show(img):
    cv2.imshow("image",img)
    cv2.waitKey()
    cv2.destroyAllWindows()

# 设置参数
ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",required=True,help="path for input image")
ap.add_argument("-t","--template",required=True,help="path for template image")
args = vars(ap.parse_args("-i images/credit_card_01.png\
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

ref_contours, ref_rect = sort_contours(ref_contours)

digits = {}
for index, (x,y,w,h) in enumerate(ref_rect):
    roi = img_tem_thresh[y:y+h, x:x+w]
    roi = cv2.resize(roi, (57,88))
    # cv_show(roi)
    digits[index] = roi
    
# 读取输入图像，预处理
img = cv2.imread("images/credit_card_01.png")
img = resize(img, width=300)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)



