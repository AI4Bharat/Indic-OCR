# DocSynth.Degradation

Degradation is a package which provides functions for performing degradations on an image. 

The functions are:



1. blur
2. watermark
3. stamp
4. bleed_through
5. pepper
6. salt
7. open
8. close
9. erode
10. dilate
11. read
12. save
13. scale
14. rotate
15. shake
16. remove_bg
17. degrade_stamp

		


# Example:


```
from degradation import degrade

degrade = degrade()
img = degrade.read("docimg.jpg")
stamp = degrade.read("stamp.png")

newimg = degrade.stamp(img, stamp, rotate_angle=45, scale_percent=10, pos=[800, 1300])
newimg = degrade.salt(newimg)

degrade.save(newimg, "newdocimg.jpg")
```


**before:** [docimg.jpg](https://drive.google.com/file/d/16p7bSt1syjnUnfsgz-0EjDl0Ti1i4cXK/view?usp=sharing)

**after:** [newdocimg.jpg](https://drive.google.com/file/d/1jgx1cvk1Ac3KMLyfkk2oT9v57AHELzkz/view?usp=sharing)



# Function Description:
## blur

* Applying blur effect on an image
* Parameters:
* img: 
    * type: image file
* radius: 
    * determines hardness of blur
    * type: integer
    * range: (0, inf)


## watermark

* Pasting image to background watermark
* Parameters: 
    * img:
        * type: image file
    * watermark: 
        * type: image file 
        * .png recommended
    * alpha, beta, gamma:
        * type: integer
        * range: [0, 1]
        * default: 1, 0.1, 0
    * scale_percent:
        * type: integer
        * range: (0, inf)
        * default: 100
        * less than 100 reduces scale, more than 100 increases scale
    * rotate_angle: 
        * type: integer
        * range: [0, 360)
        * default: 0


## stamp

* Pasting image as stamp
* Parameters:
    * img: 
        * type: image file
    * stamp:
        * type: image file
    * scale_percent: 
        * type: integer
        * range: (0, inf)
        * default: 100
        * less than 100 reduces scale, more than 100 increases scale
    * rotate_angle: 
        * type: integer
        * range: [0, 360)
    * pos:
        * position where stamp is pasted on image
        * type: [integer, integer]
        * range: [0, image dimensions]
        * default: [ ]


## bleed_through

* Adding back page bleeding effect to image
* Parameters: 
    * img: 
        * type: image file
    * alpha, gamma:
        * type: integer
        * range: [0, 1]
        * default: 0.8, 0


## pepper

* adding black pixels noise to image
* Parameters:
    * img: 
        * type: image file
    * amount:
        * type: integer
        * range: [0, 1]
        * default: 0.05


## salt

* adding white pixels noise to image
* Parameters:
    * img:
        * type: image file
    * amount:
        * type: integer
        * range: [0, 1]
        * default: 0.05


## open

* Applying [open morphology](https://en.wikipedia.org/wiki/Opening_(morphology)#:~:text=Opening%20removes%20small%20objects%20from,specific%20shapes%20in%20an%20image.) effect to image
* Parameters:
    * img: 
        * type: image file
    * kernel:
        * structuring element
        * type: numpy 2d binary array
        * default: np.ones((5, 5), np.uint8)


## close

* Applying [close morphology](https://en.wikipedia.org/wiki/Closing_(morphology)) effect to image
* Parameters:
    * img: 
        * type: image file
    * kernel:
        * structuring element
        * type: numpy 2d binary array
        * default: np.ones((5, 5), np.uint8)


## erode

* Applying [erosion morphology](https://en.wikipedia.org/wiki/Erosion_(morphology)) effect to image
* Parameters;
    * img:
        * type: image file
    * kernel:
        * structuring element
        * type: numpy 2d binary array
        * default: np.ones((3, 3), np.uint8)


## dilate

* Applying [dilation morphology](https://en.wikipedia.org/wiki/Dilation_(morphology)) effect to image
* Parameters;
    * img:
        * type: image file
    * kernel:
        * structuring element
        * type: numpy 2d binary array
        * default: np.ones((3, 3), np.uint8)


## read

* Function for reading image file
* Parameters:
    * img:
        * type: image file location


## save

* Function for saving image file
* Parameters:
    * img:
        * type: image file location
    * name:
        * type: new image file location


## scale

* Scaling size of image
* Parameters:
    * img:
        * type: image file
    * percent:
        * type: integer
        * range: (0, inf)


## rotate

* Rotating an image
* Parameters;
    * img: 
        * type: image file
    * angle:
        * type: integer
        * range: [0, 260)


## shake

* Applying shaking image to image
* Parameters:
    * img:
        * type: image file
    * alpha, gamma:
        * type: integer
        * default: 0.5, 0
    * offset_x, offset_y: 
        * amount of shake in x and y direction
        * type: integer
        * default: 0, 5


## remove_bg

* Removing background of an image
* Adds alpha channel to image
* Parameters:
    * img:
        * type: image file


## degrade_stamp

* Applies degradation effect on stamp image
* Appears like a real world stamp
* Parameters:
    * img:
        * type: image file
    * kernel:
        * structuring element
        * type: numpy 2d binary array
        * default: np.ones((3, 3), np.uint8)
    * iterations:
        * measure of degradation effect
        * default: 5