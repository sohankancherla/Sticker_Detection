import cv2

class ShapeDetector:
    def __init__(self):
        pass

    def detect(self,c):
        shape = "unidentified"
        peri = cv2.arcLength(c, True);
        approx = cv2.approxPolyDP(c,0.04 * peri, True)

        if len(approx) == 4:

            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = "square sticker" if ar >= 0.95 and ar <= 1.05 else "rect sticker"
            if ar >= 0.95 and ar <= 1.05:
                shape = "square sticker"
            elif ar >= 0.90 and ar <= 1.05:
                shape = "rect sticker"
        else:
            shape = "none"

        return shape


