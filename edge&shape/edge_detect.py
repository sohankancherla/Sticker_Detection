#Team member: ZengKeat, Valeriia, Luke, Sohan
import cv2
import imutils
import layoutparser as lp
import argparse
import numpy
from cv2 import bilateralFilter
import shapeDetector
import text_detection
import numpy as np
from PIL import Image
import glob

from PIL import Image
import os, os.path

#loop all the images path to an array
imgs = []
path = "../image/"
valid_images = [".jpg",".jpeg",".png"]
for f in os.listdir(path):
    ext = os.path.splitext(f)[1]
    if ext.lower() not in valid_images:
        continue
    imgs.append(os.path.join(path,f))

#loop over all images
for images in imgs:

    # read the image
    image = cv2.imread(images)
    image_file_path = images

    # image = cv2.imread("../image/image16.jpeg")
    # image_file_path = "../image/image16.jpeg"

    # convert the image to grayscale format
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # to equalize the range of contrast in the image
    img_gray = cv2.equalizeHist(img_gray)

    # THIS IS DILATE, WE SHOULD KEEP IT
    dilatation_size = 2
    dilation_shape = cv2.MORPH_RECT
    element = cv2.getStructuringElement(dilation_shape, (2 * dilatation_size + 1, 2 * dilatation_size + 1),
                                        (dilatation_size, dilatation_size))
    dilatation_dst = cv2.dilate(image, element)

    # This blur keep the edge but reduce the noise
    dilatation_dst = bilateralFilter(dilatation_dst, 6, 75, 75)
    #cv2.imshow("blur after dilate IMAGE", dilatation_dst)

    # This is canny edge detection, play with the value and see what work best
    edged = cv2.Canny(dilatation_dst, 10,90, 7, L2gradient=True)
    cv2.imshow('canny edge', edged)

    # close the gap between contour line and make it thicker
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    edged = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel, iterations=2)
    # cv2.imshow('morp gap after canny edge', edged)

    # detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
    contours = cv2.findContours(image=edged.copy(), mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    image_copy = image.copy()

    # draw contour on the original image
    cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=1,
                     lineType=cv2.LINE_AA)

    # create the shapeDectertor reference
    sd = shapeDetector.ShapeDetector()

    # create the textdetector reference
    td = text_detection.textDetector()

    # this will return the x and y coordinates, width and height of text bounding box
    text_box = td.text_detect(image_file_path)

    height, width, _ = image.shape
    image_area = width * height

    # set the contour size
    threshold_max = image_area * 0.2# 20%
    threshold_min = image_area * 0.05 #5%

    print("TOTAL AREA: ", image_area)
    print("MAX: ", threshold_max)
    print("MIN:", threshold_min)

    # loop over the contours
    for c in contours:

        area = cv2.contourArea(c)

        #if the area of current contour is smaller than max but bigger than min
        if threshold_max > area > threshold_min:

            print(area)
            # compute the center of the contour, then detect the name of the
            # shape using only the contour
            M = cv2.moments(c)
            if M['m00'] != 0.0:
                cX = int(M['m10'] / M['m00'])
                cY = int(M['m01'] / M['m00'])

            shape = sd.detect(c)

            # if the shape is none then dont display
            if shape != "none":

                # get all the coordinates (x,y,width,height) of current contour
                x, y, w, h = cv2.boundingRect(c)
                # the 4 point of current contour
                boundb = {'x': x, 'y': y, 'width': w, 'height': h}

                #go through each textarea bounding box
                for (startX, startY, endX, endY) in text_box:

                    #4 corrdinates point of the text area bounding box
                    innerb = {'x': startX, 'y': startY, 'width': endX, 'height': endY}

                    # formula to determined if one box is inside another box:
                    # a <= x0 < a+c and b <= y0 < b + d
                    # if one of the text area is inside that box then we can say that it is a sticker
                    if boundb['x'] <= innerb['x'] < (boundb['x'] + boundb['width']) and \
                            boundb['y'] <= innerb['y'] < (boundb['y'] + boundb['height']):

                        print('The entire box is inside the bounding box.')
                        c = c.astype("float")
                        c = c.astype("int")
                        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
                        cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                        # show the output image
                        cv2.imshow("Image", image)
                        cv2.waitKey(0)
                        break

                    else:
                        print('there are no text inside that sticker, so it is not sticker')

            # multiply the contour (x, y)-coordinates by the resize ratio,
            # then draw the contours and the name of the shape on the image
            # none_shape = "none"
            # c = c.astype("float")
            # c = c.astype("int")
            # cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            # cv2.putText(image, none_shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            #
            # # show the output image
            # cv2.imshow("Image", image)
            # cv2.waitKey(0)


    # problem1: some shape is still recognize as sticker because it look like a square or it have 4 point corner
    # solution1: we can detect the text area and make sure the detected sticker have text area inside it
    # problem2: if the contour of the sticker couldnt be capture, then having text detection is pointless.
    # solution2: tune the contour detection to be better

