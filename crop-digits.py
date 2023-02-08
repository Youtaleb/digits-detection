import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import os
import matplotlib.pyplot as plt
%matplotlib inline
import pandas as pd

def reshape_image(image_path,output_loc):
    img = Image.open(image_path)

    # If the image is not a PNG, we convert it to a PNG.
    if img.format.lower() != "png":
        filename = image_path.split(".")

        png_img =str()
        for el in filename[:-1]:
            png_img += el

        png_img = png_img+".png"
        img.save("."+png_img)
        image_path = "."+png_img
        print("The input image has the extension :"+img.format+". It has been converted to a PNG. The new image is stored with a different file extension : "+image_path)

    #img = Image.open(image_path)

    # If the input image is too large, we reduce its dimensions.
    # max_height = 250
    # For now, we give all the images the same height
    height = 220
    img = Image.open(image_path).convert("RGBA")
    w_img, h_img = img.size

    if h_img != height:
        newsize = (int(height*w_img/min(w_img,h_img)), int(height*h_img/min(w_img,h_img)))
        img = img.resize(newsize)
        img.save(image_path)

    return image_path

def crop_digits(image_path, output_loc):
    # image_path is a string : it indicates the path to where the image is stored.
    # output_loc is a string : it indicates the path to where the cropped digits should be stored.
    """
    This function takes an image containing a number and outputs a set of images
    containing each digit included in the image inputed.
    If the input image is of the following form :
    ---------------
    | 2  3  9  5  |
    ---------------
    then the output would be 4 images containing each a digit :

       -----         -----         -----         -----
       | 2 |         | 3 |         | 9 |         | 5 |
       -----         -----         -----         -----
    digit_1.png   digit_2.png   digit_3.png   digit_4.png

    Before using the script, the module cv2 needs to be imported : import cv2
    """

    # We check if the input image is not too large and if the image is a PNG.
    # If not, we resize the image, and convert it to a PNG.
    image_path = reshape_image(image_path,output_loc)

    im = cv2.imread(image_path)
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    digitCnts = [] # contours of digits will be stored here.
    digits = dict() # Keys of this dictionnary will contain the a abscissa of the images
                    # Values contain the digit's image
                    # digits[x] = image
    final = thresh.copy()
    #print("Size : "+str(im.shape))
    w_img, h_img, channels = im.shape

    for c in contours:
        (x, y, w, h) = cv2.boundingRect(c)
        x1 = x+w
        y1 = y+h
        cv2.rectangle(final,(x,y),(x1,y1),(0, 255, 0), 1)
        # Contours large enough are supposed to contain digits.
        if w >= 13 and w <= 230 and h >= 90:
            #print((x, y, w, h))

            digitCnts.append([x,x1,y,y1])
            #print(len(digitCnts))
            # Drawing the selected contour on the original image
            #cv2.rectangle(final,(x,y),(x1,y1),(0, 255, 0), 1)

            p=1 # p is a padding : setting p to 1 avoids slicing parts of the digits
            crop_img = final[y-p:y1+p, x-p:x1+p].copy() #we set a padding p
            digits[x]=crop_img

    keys = list(digits.keys())
    keys.sort()
    #del keys[0] #we delete the first element, as the first element corresponds to the whole number
    #print(keys)

    i=1
    digits_filenames = dict()
    for k in keys:
        #cv2.imshow("cropped", crop_img)
        cv2.imwrite(output_loc+"/digit_"+str(i)+".png", digits[k])
        print(output_loc+"/digit_"+str(i)+".png")
        digits_filenames[i] = "digit_"+str(i)+".png"
        cv2.waitKey(0)
        i+=1
