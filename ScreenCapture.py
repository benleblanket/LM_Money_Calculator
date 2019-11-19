import cv2
import numpy as np
import pyscreenshot as pscrn
from PIL import ImageGrab
import time
import keyboard
import math
import DetectCount


# Return the current frame of the selected area of the screen
def image_cap(x, y, w, h):
    time.sleep(1)
    img = ImageGrab.grab(bbox=(x, y, w, h))
    img_np = np.array(img)
    # frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    frame = img_np
    cv2.imshow("test", frame)
    # cv2.waitKey(0)
    cv2.destroyAllWindows()

    return frame


# For testing purposes
# Using a single image that has been imported in for testing detection integrity
def single_image_import(image_file):
    try:
        img = cv2.imread(image_file, 1)
        frame = np.array(img)
        cv2.imshow('test', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return frame
    except:
        print('error')
        return -1


# Increment Bl, Gr, Re, Di, GD, RD
def inc_gem(frame, gem_cnt):
    return gem_cnt

# Increment Sm, Me, La
def inc_prl(frame, prl_cnt):
    return prl_cnt

# Increment Co, Bi, GB
def inc_mon(frame, mon_cnt):
    return mon_cnt


def find_scrn_col(frame):
    color = -1
    bgr_total = [0] * 3
    # height
    rows = frame.shape[0]
    krnl_r_size = int(math.ceil(rows/5))
    # width
    cols = frame.shape[1]
    krnl_c_size = int(math.ceil(cols/5))
    # channels (should be BGR)
    chnl = frame.shape[2]
    if chnl != 3:
        return -1
    # Average BGR elements
    for c in range(krnl_c_size):
        for r in range(krnl_r_size):
            bgr = frame[c, r]
            bgr_total[0] += bgr[0]
            bgr_total[1] += bgr[1]
            bgr_total[2] += bgr[2]

    total_cells = krnl_c_size * krnl_r_size
    for i in range(len(bgr_total)):
        bgr_total[i] = bgr_total[i] / total_cells

    max_val = np.amax(bgr_total)
    max_ind = bgr_total.index(max_val)
    print(bgr_total)
    for i in range(len(bgr_total)):
        if i != max_ind:
            if (max_val - bgr_total[i]) < 20:
                return color
    # GREEN
    if max_ind == 1:
        color = 1
    # BLUE
    elif max_ind == 0:
        color = 0
    # RED
    elif max_ind == 2:
        color = 2
    return color


# Calculate and print the total
def calc_total(mon_cnt, prl_cnt, gem_cnt):
    total = 0
    total += mon_cnt[0] * 5000 + mon_cnt[1] * 20000 + mon_cnt[2] * 100000
    total += prl_cnt[0] * 50000 + prl_cnt[1] * 100000 + prl_cnt[2] * 1000000
    total += gem_cnt[0] * 500000 + gem_cnt[1] * 800000 + gem_cnt[2] * 1000000 + \
        gem_cnt[3] * 5000000 + gem_cnt[4] * 2000000 + gem_cnt[5] * 5000

    print(str(total) + 'G')


# Order of collectibles
def main(x, y, w, h, calc_key, test, image_file):
    # Co Bi GB Bl Gr Re Di GD RD Sm Me La
    mon_cnt = [0] * 3
    gem_cnt = [0] * 6
    prl_cnt = [0] * 3

    video_loop = True
    while video_loop:
        if test:
            frame = single_image_import(image_file)
            video_loop = False
        else:
            frame = image_cap(x, y, w, h)
        scrn_color = find_scrn_col(frame)
        print(scrn_color)

        # elif green -------- Check --- 3-heights space
        if scrn_color == 1:
            mon_cnt = DetectCount.inc_mon(frame, mon_cnt)

        # elif blue --------- P ------- 3-height space
        if scrn_color == 0:
            prl_cnt = inc_prl(frame, prl_cnt)

        # elif red ---------- G ------- mid-height space
        if scrn_color == 2:
            gem_cnt = inc_gem(frame, gem_cnt)

        # if hidden ------- None
        if scrn_color == -1:
            continue

        # UNFINISHED - If a calc_key is set, only calc_total on key press. If not set, auto-update
        if calc_key == '*':
            if keyboard.is_pressed(calc_key):
                calc_total(mon_cnt, prl_cnt, gem_cnt)
        else:
            calc_total(mon_cnt, prl_cnt, gem_cnt)

    return


if "__main__" == __name__:

    test = True

    x = 100
    y = 10
    w = 400
    h = 780
    calc_key = ''
    # 107 x 78
    image_file = r"C:\Users\\bleblanc\Downloads\PersonalProjects\lm_gbh_images\stnd_vark.png"
    main(x, y, w, h, calc_key, test, image_file)
