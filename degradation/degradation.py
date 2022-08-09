import numpy as np
import imutils
import cv2


class degrade:

    def blur(self, img, radius=5):
        # radius has to be odd
        radius += 1 if radius%2 == 0 else 0
        return cv2.GaussianBlur(img, (radius, radius), cv2.BORDER_DEFAULT)




    def watermark(self, img, watermark, alpha=1, beta=0.1, gamma=0, scale_percent=100, rotate_angle=0):
        # add alpha channel to img if watermark has alpha
        if watermark.shape[2] == 4: img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)

        # size of image and watermark
        h_watermark, w_watermark, _ = watermark.shape
        h_img, w_img, _ = img.shape

        # making img and watermark dtype same
        watermark = watermark.astype(img.dtype)

        # down-scaling watermark if larger than img
        if w_watermark > w_img:
            watermark = self.scale(watermark, w_img/w_watermark*100)
        if h_watermark > h_img:
            watermark = self.scale(watermark, h_img/h_watermark*100)

        # apply transformations
        watermark = self.scale(watermark, scale_percent)
        watermark = self.rotate(watermark, rotate_angle)

        # size of down-scaled watermark
        h_watermark, w_watermark, _ = watermark.shape

        # calcuting center of image, where watermark's center will fall
        center_y = int(h_img/2)
        center_x = int(w_img/2)
        
        # calcuting coordinates in image where watermark's corners will fall
        top_y = center_y - int(h_watermark/2)
        left_x = center_x - int(w_watermark/2)
        bottom_y = top_y + h_watermark
        right_x = left_x + w_watermark

        # overlaying watermark only on specific part of image
        img_part = img[top_y:bottom_y, left_x:right_x]
        img_part = cv2.addWeighted(img_part, alpha, watermark, beta, gamma)
        img[top_y:bottom_y, left_x:right_x] = img_part

        return img




    def stamp(self, img, stamp, scale_percent=100, rotate_angle=0):
        # add alpha channel to img if stamp has alpha
        if stamp.shape[2] == 4: img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)

        # size of image and stamp
        h_stamp, w_stamp, _ = stamp.shape
        h_img, w_img, _ = img.shape

        # making img and stamp dtype same
        stamp = stamp.astype(img.dtype)

        # down-scaling stamp if larger than img
        if w_stamp > w_img:
            stamp = self.scale(stamp, w_img/w_stamp*100)
        if h_stamp > h_img:
            stamp = self.scale(stamp, h_img/h_stamp*100)

        # apply transformations
        stamp = self.scale(stamp, scale_percent)
        stamp = self.rotate(stamp, rotate_angle)

        # size of down-scaled stamp
        h_stamp, w_stamp, _ = stamp.shape

        # calcuting center of image, where stamp's center will fall
        center_y = int(h_img/2)
        center_x = int(w_img/2)
        
        # calcuting coordinates in image where stamp's corners will fall
        top_y = center_y - int(h_stamp/2)
        left_x = center_x - int(w_stamp/2)
        bottom_y = top_y + h_stamp
        right_x = left_x + w_stamp

        # overlaying stamp only on specific part of image
        img_part = img[top_y:bottom_y, left_x:right_x]
        img_part = cv2.add(img_part, stamp)
        img[top_y:bottom_y, left_x:right_x] = img_part

        return img




    def bleed_through(self, img, alpha=0.8, gamma=0, offset_x=0, offset_y=5):
        # creating bleed through background from image itself
        background = img.copy()
        background = cv2.flip(background, 1) 

        # offsetting the background
        rows, cols, _ = background.shape
        trans_matrix = np.float32([[1, 0, offset_x], [0, 1, offset_y]])
        background = cv2.warpAffine(img, trans_matrix, (cols, rows), borderValue=255)

        # blending the image and background
        beta = 1 - alpha

        return self.watermark(img, background, alpha, beta, gamma)




    def pepper(self, img, amount=0.05):
        img = img.copy()
        noise = np.random.random(img.shape)
        img[noise < amount] = 0
        return img




    def salt(self, img, amount=0.3):
        img = img.copy()
        noise = np.random.random(img.shape)
        img[noise < amount] = 255
        return img




    def open(self, img, kernel=np.ones((5, 5), np.uint8)):
        return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)




    def close(self, img, kernel=np.ones((5, 5), np.uint8)):
        return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)




    def erode(self, img, kernel=np.ones((3, 3), np.uint8)):
        return cv2.erode(img, kernel)




    def dilate(self, img, kernel=np.ones((3, 3), np.uint8)):
        return cv2.dilate(img, kernel)




    def read(self, img):
        return cv2.imread(img, -1)




    def save(self, name, img):
        return cv2.imwrite(name, img)




    def scale(self, img, percent=100):
        new_width = int(img.shape[1] * percent/100)
        new_height = int(img.shape[0] * percent/100)
        new_dim = (new_width, new_height)

        return cv2.resize(img, new_dim, interpolation=cv2.INTER_AREA)




    def rotate(self, img, angle=45):
        return imutils.rotate(img, angle)
            