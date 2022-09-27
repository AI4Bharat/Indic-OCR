import numpy as np
import imutils
import random
import cv2


class degrade:

    def blur(self, img, radius=5):
        # radius has to be odd
        radius += 1 if radius%2 == 0 else 0
        return cv2.GaussianBlur(img, (radius, radius), cv2.BORDER_DEFAULT)


    def watermark(self, img, watermark, alpha=1, beta=0.1, gamma=0, scale_percent=100, rotate_angle=0):
        # add alpha channel to img if watermark has alpha
        if watermark.shape[2] == 4: img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)

        # making img and watermark dtype same
        watermark = watermark.astype(img.dtype)

        # apply transformations
        watermark = self.scale(watermark, scale_percent)
        watermark = self.rotate(watermark, rotate_angle)

        # size of image and watermark
        h_watermark, w_watermark, _ = watermark.shape
        h_img, w_img, _ = img.shape

        # down-scaling watermark if larger than img
        if w_watermark > w_img:
            watermark = self.scale(watermark, w_img/w_watermark*100)
        if h_watermark > h_img:
            watermark = self.scale(watermark, h_img/h_watermark*100)

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


    def stamp(self, img, stamp, scale_percent=100, rotate_angle=0, pos=[]):
        # making img and stamp dtype same
        stamp = stamp.astype(img.dtype)

        # apply transformations
        stamp = self.scale(stamp, scale_percent)
        stamp = self.rotate(stamp, rotate_angle)

        # size of image and stamp
        h_stamp, w_stamp, _ = stamp.shape
        h_img, w_img, _ = img.shape

        # down-scaling stamp if larger than img
        if w_stamp > w_img:
            stamp = self.scale(stamp, w_img/w_stamp*100)
        if h_stamp > h_img:
            stamp = self.scale(stamp, h_img/h_stamp*100)

        # recalculating sizes of image and stamp
        h_stamp, w_stamp, c_stamp = stamp.shape
        h_img, w_img, c_img = img.shape

        # calculating default stamp position
        if not pos:
            pos = [int(w_img/2)-int(w_stamp/2), int(h_img/2)-int(h_stamp/2)]

        # making stamp mask
        *_, mask = cv2.split(stamp)
        maskBGRA = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGRA)
        maskBGR = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        imgRGBA = cv2.bitwise_and(stamp, maskBGRA)
        imgRGB = cv2.cvtColor(imgRGBA, cv2.COLOR_BGRA2BGR)

        imgMaskFull = np.zeros((h_img, w_img, c_img), np.uint8)
        imgMaskFull[pos[1]:h_stamp + pos[1], pos[0]:w_stamp + pos[0], :] = imgRGB
        imgMaskFull2 = np.ones((h_img, w_img, c_img), np.uint8) * 255
        maskBGRInv = cv2.bitwise_not(maskBGR)
        imgMaskFull2[pos[1]:h_stamp + pos[1], pos[0]:w_stamp + pos[0], :] = maskBGRInv

        # pasting masks on image
        img = cv2.bitwise_and(img, imgMaskFull2)
        img = cv2.bitwise_or(img, imgMaskFull)

        return img


    def bleed_through(self, img, alpha=0.8, gamma=0):
        # creating bleed through background from image itself
        background = img.copy()
        background = cv2.flip(background, 1) 

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


    def save(self, img, name="img.jpg"):
        return cv2.imwrite(name, img)


    def scale(self, img, percent=100):
        new_width = int(img.shape[1] * percent/100)
        new_height = int(img.shape[0] * percent/100)
        new_dim = (new_width, new_height)

        return cv2.resize(img, new_dim, interpolation=cv2.INTER_AREA)


    def rotate(self, img, angle=45):
        return imutils.rotate(img, angle)


    def shake(self, img, alpha=0.5, gamma=0, offset_x=0, offset_y=5):
        # creating shaken image from image itself
        shakeimg = img.copy()
        shakeimg = cv2.flip(shakeimg, 1)

        # offsetting the shaken image
        rows, cols, _ = shakeimg.shape
        trans_matrix = np.float32([[1, 0, offset_x], [0, 1, offset_y]])
        shakeimg = cv2.warpAffine(img, trans_matrix, (cols, rows), borderValue=255)

        # blending the image and shaken image
        beta = 1 - alpha

        return self.watermark(img, shakeimg, alpha, beta, gamma)


    def remove_bg(self, img):
        # convert to gray
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # threshold input image as mask
        mask = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)[1]

        # negate mask
        mask = 255 - mask

        # apply morphology to remove isolated extraneous noise
        # use borderconstant of black since foreground touches the edges
        kernel = np.ones((3,3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # anti-alias the mask -- blur then stretch
        # blur alpha channel
        mask = cv2.GaussianBlur(mask, (0,0), sigmaX=2, sigmaY=2, borderType = cv2.BORDER_DEFAULT)

        # linear stretch so that 127.5 goes to 0, but 255 stays 255
        mask = (2*(mask.astype(np.float32))-255.0).clip(0,255).astype(np.uint8)

        # put mask into alpha channel
        result = img.copy()
        result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
        result[:, :, 3] = mask

        return result


    def degrade_stamp(img, kernel=np.ones((3, 3)), iterations=5):
        quadrant = random.choice([1, 2, 3, 4])
        img_h, img_w, _ = img.shape

        if quadrant == 1: h1, h2, w1, w2 = 0, img_h//2, img_w//2, img_w
        elif quadrant == 2: h1, h2, w1, w2 = 0, img_h//2, 0, img_w//2
        elif quadrant == 3: h1, h2, w1, w2 = img_h//2, img_h, 0, img_w//2
        else: h1, h2, w1, w2 = img_h//2, img_h, img_w//2, img_w

        imgpart = img[h1: h2, w1: w2]
        imgpart = cv2.erode(imgpart, kernel=kernel, iterations=iterations)
        img[h1: h2, w1: w2] = imgpart

        if quadrant == 1: h1, h2, w1, w2 = 0, img_h*2//3, img_w//3, img_w
        elif quadrant == 2: h1, h2, w1, w2 = 0, img_h*2//3, 0, img_w*2//3
        elif quadrant == 3: h1, h2, w1, w2 = img_h//3, img_h, 0, img_w*2//3
        else: h1, h2, w1, w2 = img_h//3, img_h, img_w//3, img_w

        imgpart = img[h1: h2, w1: w2]
        imgpart = cv2.erode(imgpart, kernel=kernel, iterations=iterations)
        img[h1: h2, w1: w2] = imgpart
        
        img = cv2.erode(img, kernel=kernel, iterations=iterations)
        return img