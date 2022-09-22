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
args = vars(ap.parse_args("-i images/credit_card_04.png\
                          -t images/ocr_a_reference.png".split())) # 改成字典的形式 {"images": path, "template": path}
# 模板图像
img_tem = cv2.imread(args["template"])
# cv_show(img_tem)
# 模板灰度图像
img_tem_gray = cv2.cvtColor(img_tem, cv2.COLOR_BGR2GRAY)
# 模板二值图像
img_tem_thresh = cv2.threshold(img_tem_gray, 20, 255, cv2.THRESH_BINARY_INV)[1]
# cv_show(img_tem_thresh)
# 寻找和绘制轮廓 - mode=cv2.RETR_EXTERNAL 只取外部轮廓
ref_contours = cv2.findContours(img_tem_thresh, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)[1]
cv2.drawContours(img_tem, ref_contours, -1, (0,0,255), 3)
# print(np.array(ref_contours).shape) # (10,)
# print(np.array(ref_contours)[0].squeeze().shape) # (32,2)

ref_contours, ref_rect = sort_contours(ref_contours)

digits = {} # digits 的key为数字，value为数字对应的图片
for index, (x,y,w,h) in enumerate(ref_rect):
    roi = img_tem_thresh[y:y+h, x:x+w]
    roi = cv2.resize(roi, (57,88))
    # cv_show(roi)
    digits[index] = roi
    
# 卷积核
kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (9,3))
kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
# print(kernel1, kernel1.dtype, type(kernel1)) # np.ones((9,3)), np.unit8, <class 'numpy.ndarray'>

# 读取输入图像，预处理
img = cv2.imread(args["image"])
# cv_show(img)
img = resize(img, width=300)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv_show(img_gray)

# 礼帽操作 - 原始-开运算（先腐蚀再膨胀）
# 礼貌操作 - 突出明亮区域
img_gray_tophat = cv2.morphologyEx(img_gray, cv2.MORPH_TOPHAT, kernel=kernel1)
# cv_show(img_gray_tophat)

# Sobel求梯度
img_gradx = cv2.Sobel(img_gray_tophat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1) # ksize=-1 相当于 3*3
img_gradx = np.absolute(img_gradx)
img_grady = cv2.Sobel(img_gray_tophat, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1) # ksize=-1 相当于 3*3
img_grady = np.absolute(img_grady)
img_grad = cv2.addWeighted(img_gradx, 0.5, img_grady, 0.5, 0)
# cv_show(img_grad)

# 求完梯度后数值归一化
minval, maxval = np.min(img_grad),np.max(img_grad)
# print(minval, maxval)
img_grad = 255* ((img_gradx-minval)/ (maxval-minval))
img_grad = img_grad.astype("uint8") # 这一步必不可少
# cv_show(img_grad)

#通过闭操作（先膨胀，再腐蚀）将数字连在一起
img_grad_close = cv2.morphologyEx(img_grad, cv2.MORPH_CLOSE, kernel1)
# cv_show(img_grad_close)

# thresh=0，自动划分阈值
img_thresh = cv2.threshold(img_grad_close, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
# cv_show(img_thresh)

# 闭操作，先膨胀再腐蚀，使得相连的区域连接
img_thresh = cv2.morphologyEx(img_thresh, cv2.MORPH_CLOSE, kernel2)
# cv_show(img_thresh)

# 计算轮廓
contours = cv2.findContours(img_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
img_exhib = cv2.drawContours(img.copy(), contours, -1, (0,0,255), 1)
# cv_show(img_exhib)

locs_lst = []
# 筛选需要的轮廓
for index, cnt in enumerate(contours):
    (x,y,w,h) = cv2.boundingRect(cnt)
    ar = w / float(h)
    if ar > 2.5 and ar < 4:
        if (w>30 and w<55) and (h>10 and h<20):
            locs_lst.append((x,y,w,h))

# 对轮廓排序 - 按照x轴排序
locs = sorted(locs_lst, key=lambda x:x[0])
digit_out = [] # 银行卡号对应的所有数字
for i,(x,y,w,h) in enumerate(locs):
    real_digits = [] # 第一组数字的匹配值
    group = img_gray[y-5:y+h+5, x-5:x+w+5]
    # cv_show(group)
    # 二值处理
    group = cv2.threshold(group, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # cv_show(group)
    # find contours
    digit_contours = cv2.findContours(group, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)[1]
    # draw_contour = cv2.drawContours(group.copy(), digit_contours, -1, (0,255,255),0)
    # cv_show(draw_contour)
    digit_contours, digit_contours_rects = sort_contours(digit_contours)
    
    # ! 不要和上一级循环的变量名相同，所以这里为x1, y1, w1, h1
    for x1,y1,w1,h1 in digit_contours_rects:
        roi = group[y1:y1+h1, x1:x1+w1]
        roi = cv2.resize(roi, (57,88))
        # cv_show(roi)

        # 计算匹配得分
        scores = [] # 索引对应匹配的数字，一共10个值，对应0-9的得分
        
        for digit,digit_roi in digits.items():
            result = cv2.matchTemplate(roi, digit_roi, method=cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            scores.append(max_val)
        
        # 取最高的得分
        real_digits.append(str(np.argmax(scores)))

    digit_out.extend(real_digits)
    
    # 展示
    cv2.rectangle(img, (x-5,y-5), (x+w+5, y+h+5), (0,0,255), 1)
    cv2.putText(img, "".join(real_digits), (x, y-15), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

# 打印结果
FIRST_NUMBER = {
	"3": "American Express",
	"4": "Visa",
	"5": "MasterCard",
	"6": "Discover Card"
}
print("Credit Card Type: {}".format(FIRST_NUMBER[digit_out[0]]))
print("Credit Card #: {}".format(" ".join(digit_out)))        

cv_show(img)