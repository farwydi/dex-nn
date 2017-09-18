import cv2
import time
import numpy as np
import pyscreenshot as ImageGrab
import pyautogui


def main():
    screenshot = ImageGrab.grab(bbox=(0, 30, 1024, 768))
    im = screenshot.convert('RGB')
    imcv = np.array(screenshot)
    cv_img = imcv.astype(np.uint8)

    img_grey = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('temp.png', cv_img)

    # cv2.imshow("image", img)
    cv2.waitKey()

# def find_patt(image, patt, thres):
#   img_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#   (patt_H, patt_W) = patt.shape[:2]
#   res = cv2.matchTemplate(img_grey, patt, cv2.TM_CCOEFF_NORMED)
#   loc = np.where(res>thres)
#   return patt_H, patt_W, zip(*loc[::-1])


# if __name__ == '__main__':
#   screenshot = ImageGrab.grab()
#   img = np.array(screenshot.getdata(), dtype='uint8').reshape((screenshot.size[1],screenshot.size[0],3))

#   patt = cv2.imread('coin.png', 0)
#   h,w,points = find_patt(img, patt, 0.60)
#   if len(points)!=0:
#     pyautogui.moveTo(points[0][0]+w/2, points[0][1]+h/2)
#     # pyautogui.click()

if __name__ == '__main__':
    main()
