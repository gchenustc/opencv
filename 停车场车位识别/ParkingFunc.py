import matplotlib.pyplot as plt
import cv2
import numpy as np

class Parking(object):

    def img_show(self, images, cmap=None):
        cols = 2
        rows = (len(images)+1) // cols

        for index, image in enumerate(images):
            plt.subplot(rows, cols, index+1)
            plt.imshow(image, cmap="gray" if cmap is None else cmap)
            plt.xticks([])
            plt.yticks([])
        
        plt.tight_layout()
        plt.show()
    
    def cv_show(self, img, name="image"):
        cv2.imshow(name, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    def select_useful(self, img):
        #过滤掉背景
        lower = np.uint8([120, 120, 120])
        upper = np.uint8([255, 255, 255])
        
        # lower_red和高于upper_red的部分分别变成0，lower_red～upper_red之间的值变成255,相当于过滤背景
        mask = cv2.inRange(img, lower, upper)
        img = cv2.bitwise_and(img, img, mask=mask)
        return img
    
    def to_gray(self, img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    def get_edge(self, img, low_thres=100, high_thres=500):
        return cv2.Canny(img, low_thres, high_thres)
    
    def filter_region(self, img, points):
        """传入的图像需要时灰度图"""
        # 增加一个维度是为了fillPoly函数调用需要
        points = np.array([points])
        
        mask = np.zeros_like(img)
        cv2.fillPoly(mask, points, 255) # 如果不是灰度图，255要换成(255,255,255)
        # Parking().cv_show(mask)
        return cv2.bitwise_and(img, mask)

    def select_region(self,img):
        """
        手动选择区域
        """
        # first, define the polygon by vertices
        rows, cols = img.shape[:2]
        pt_1  = [cols*0.05, rows*0.90]
        pt_2 = [cols*0.05, rows*0.70]
        pt_3 = [cols*0.30, rows*0.55]
        pt_4 = [cols*0.6, rows*0.15]
        pt_5 = [cols*0.90, rows*0.15] 
        pt_6 = [cols*0.90, rows*0.90]

        points = np.array([pt_1, pt_2, pt_3, pt_4, pt_5, pt_6], dtype=np.int32)

        img_point = cv2.cvtColor(img.copy(), cv2.COLOR_GRAY2RGB)

        # 展示定位点，debug用
        for point in points:
            cv2.circle(img_point, (point[0], point[1]), 10, (0,0,255), 4)
            # Parking().cv_show(img_point)
        
        return self.filter_region(img, points)