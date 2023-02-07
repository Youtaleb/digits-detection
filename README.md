# digits-detection
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
