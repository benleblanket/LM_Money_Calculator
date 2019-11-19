import pytesseract
import cv2
import math

# import ScreenCapture

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def crop_to_right(frame):
    half_cols = math.trunc(frame.shape[1]/2)
    cropped_img = frame[:frame.shape[0], half_cols:]
    return cropped_img

def mask_frame(frame):
    frame = cv2.GaussianBlur(frame, (3,3), 0)
    for r in range(frame.shape[0]):
        for c in range(frame.shape[1]):
            bgr = frame[r, c]
            if (bgr[0] * 7) < bgr[1] and (bgr[0] * 7) < bgr[2]:
                frame[r, c] = [0, 0, 255]
    cv2.imshow("mask", frame)
    cv2.waitKey()
    cv2.destroyAllWindows()
    return frame

def inc_mon(frame, mon_cnt):
    gframe = frame
    # gframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gframe = crop_to_right(gframe)

    cropframe = cv2.fastNlMeansDenoising(src=gframe, h=3)
    masked_frame = mask_frame(cropframe)
    window_height = math.trunc(cropframe.shape[0]/3)
    coinframe = cropframe[:window_height, 0:]
    billframe = cropframe[window_height:(window_height*2), 0:]
    barframe = cropframe[(window_height*2):, 0:]
    cv2.imshow("coin", coinframe)
    cv2.imshow("bill", billframe)
    cv2.imshow("bar", barframe)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    coins = pytesseract.image_to_string(coinframe, config="outputbase digits")
    bills = pytesseract.image_to_string(billframe, config="outputbase digits")
    bars = pytesseract.image_to_string(barframe, config="outputbase digits")

    text = pytesseract.image_to_string(cropframe, config="outputbase digits")
    print("Coins: " + str(coins))
    print("Bills: " + str(bills))
    print("Bars: " + str(bars))
    print(text)



    return