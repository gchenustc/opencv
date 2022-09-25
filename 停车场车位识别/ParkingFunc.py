import matplotlib.pyplot as plt

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