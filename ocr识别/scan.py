import numpy as np
import argparse
import cv2
import os

# 绘图展示
def cv_show(img):
    cv2.imshow("image",img)
    cv2.waitKey()
    cv2.destroyAllWindows()

def order_points(pts):
    """对坐标按照左上，右上，右下，左下进行排序"""
    
    ret = np.zeros((4,2), dtype="float32")
    # 左上，右下
    sum_ = pts.sum(axis=1).flatten()
    ret[0] = pts[np.argmin(sum_)] 
    ret[2] = pts[np.argmax(sum_)]

    # 右上，坐下
    diff_ = np.diff(pts, axis=1).flatten()
    ret[1] = pts[np.argmin(diff_)]
    ret[3] = pts[np.argmax(diff_)]

    return ret
    
    
def perspectiveTrans(img, pts): # pts:坐标
    pts = order_points(pts) # numpy 格式
    tl, tr, br, bl = pts
    
    # 计算输入的w和h值
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    
	# 变换后对应坐标位置
    dest = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")
    
    # ! 计算变换矩阵
    M = cv2.getPerspectiveTransform(pts, dest)
    return cv2.warpPerspective(img, M, (maxWidth, maxHeight))
    
    

# argparse
ap = argparse.ArgumentParser()
group = ap.add_mutually_exclusive_group(required=True)
group.add_argument("-f", "--imagefolder", default=0, help="Path to store images") 
group.add_argument("-i","--image", help="Path to image to scan")
args = ap.parse_args(f"-i .\\images\\page.jpg".split())
# args = ap.parse_args(f"-f .\images".split())

image_paths = []
if not args.imagefolder:
    image_paths.append(args.image)
else:
    image_name = os.listdir(args.imagefolder)
    image_paths = list(map(lambda x: os.path.join(args.imagefolder, x), image_name))

# print(images_path)

# 拿出一张图像进行识别
image_path = image_paths[0]

image = cv2.imread(image_path)
ori = image.copy()
# cv_show(image)

# 将image进行resize,新的图片的高度统一为500，resize是为了获得文本轮廓区域，仍然按照原尺寸输出
ratio = image.shape[0] / 500
new_width =  image.shape[1] / ratio
image = cv2.resize(image, (int(new_width), 500),interpolation=cv2.INTER_AREA) # 变换成统一尺寸后的图像

# 预处理
# 灰度处理 - GaussianBlur - Canny，其实Canny中就包含GaussianBlur，中间步骤是为了得到Blur后的图像
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (3,3), 0)
edged = cv2.Canny(gray, 50, 200)
# 展示预处理效果 
# cv_show(edged)

# 轮廓检测
cnts = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[1]
# 按照轮廓面积从大到小排序，获取前三个个可能是文本界面的轮廓，但是还要继续筛选
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:3]
# 展示轮廓
image_cnts = cv2.drawContours(image.copy(), cnts, -1, (0,0,255), 1)
# cv_show(image_cnts)

cnts_ocr = []
# 筛选轮廓
for cnt in cnts:
    c = cv2.arcLength(cnt, closed=True)
    cnt_approx = cv2.approxPolyDP(cnt, 0.02*c, closed=True)
    # print(len(cnt_approx))
    # 如果轮廓由四个点组成，则是文本轮廓
    if len(cnt_approx) == 4:
        cnts_ocr.append(cnt_approx.squeeze()) #  squeeze() 去除多余的维度
# image_cnts_ocr = cv2.drawContours(image.copy(), cnts_ocr, -1, (0,0,255), 1)
# cv_show(image_cnts_ocr)

# 选取最大的文本轮廓
cnt_ocr = cnts_ocr[0]
# print(cnt_ocr.shape) # (4,2)

# 透视变换
image_ocr = perspectiveTrans(ori, cnt_ocr*ratio) 
# cv_show(image_ocr)

# 后处理
image_ocr = cv2.cvtColor(image_ocr, cv2.COLOR_BGR2GRAY)
image_ocr = cv2.threshold(image_ocr, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# 保存
cv2.imwrite("scan.png", image_ocr)

# cv_show(image_ocr)
