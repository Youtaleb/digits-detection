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
    im = cv2.imread(image_path)
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    digitCnts = [] # contours of digits will be stored here.
    digits = dict() # Keys of this dictionnary will contain the a abscissa of the images
                    # Values contain the digit's image
                    # digits[x] = image
    final = thresh.copy()

    for c in contours:
        (x, y, w, h) = cv2.boundingRect(c)
        # Contours large enough are supposed to contain digits.
        if w >= 13 and w <= 290 and h >= 20:
            #print((x, y, w, h))
            x1 = x+w
            y1 = y+h
            digitCnts.append([x,x1,y,y1])
            #print(len(digitCnts))
            # Drawing the selected contour on the original image
            #cv2.rectangle(final,(x,y),(x1,y1),(0, 255, 0), 1)

            p=1 # p is a padding : setting p to 1 avoids slicing parts of the digits
            crop_img = final[y-p:y1+p, x-p:x1+p].copy() #we set a padding p
            digits[x]=crop_img

    keys = list(digits.keys())
    keys.sort()
    del keys[0] #we delete the first element, as the first element corresponds to the whole number
    #print(keys)

    i=1
    digits_filenames = dict()
    for k in keys:
        #cv2.imshow("cropped", crop_img)
        cv2.imwrite(output_loc+"/digit_"+str(i)+".png", digits[k])
        digits_filenames[i] = "digit_"+str(i)+".png"
        cv2.waitKey(0)
        i+=1

    #cv2.imwrite("digits_cropped.png", final)
