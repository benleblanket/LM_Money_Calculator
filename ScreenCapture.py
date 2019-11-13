import cv2
import numpy as np
import pyscreenshot as pscrn
from PIL import ImageGrab
import time
import keyboard


# Return the current frame of the selected area of the screen
def image_cap(x, y, w, h):
    time.sleep(1)
    img = ImageGrab.grab(bbox=(x, y, w, h))
    img_np = np.array(img)
    # frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    frame = img_np
    cv2.imshow("test", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return frame


# Increment Bl, Gr, Re, Di, GD, RD
def inc_gem(frame, gem_cnt):
    return gem_cnt

# Increment Sm, Me, La
def inc_prl(frame, prl_cnt):
    return prl_cnt

# Increment Co, Bi, GB
def inc_mon(frame, mon_cnt):
    return mon_cnt


# Calculate and print the total
def calc_total(mon_cnt, prl_cnt, gem_cnt):
    total = 0
    total += mon_cnt[0] * 5000 + mon_cnt[1] * 20000 + mon_cnt[2] * 100000
    total += prl_cnt[0] * 50000 + prl_cnt[1] * 100000 + prl_cnt[2] * 1000000
    total += gem_cnt[0] * 500000 + gem_cnt[1] * 800000 + gem_cnt[2] * 1000000 + \
        gem_cnt[3] * 5000000 + gem_cnt[4] * 2000000 + gem_cnt[5] * 5000

    print(str(total) + 'G')


# Order of Operations
def main(x, y, w, h, calc_key):
    # Co Bi GB Bl Gr Re Di GD RD Sm Me La
    mon_cnt = [0] * 3
    gem_cnt = [0] * 6
    prl_cnt = [0] * 3

    while True:
        frame = image_cap(x, y, w, h)

        # if hidden ------- None

        # elif blue --------- P ------- 3-height space
        if True:
            prl_cnt = inc_prl(frame, prl_cnt)

        # elif red ---------- G ------- mid-height space
        if False:
            gem_cnt = inc_gem(frame, gem_cnt)

        # elif green -------- Check --- 3-heights space
        if False:
            mon_cnt = inc_mon(frame, mon_cnt)

        # UNFINISHED - If a calc_key is set, only calc_total on key press. If not set, auto-update
        if calc_key == '*':
            if keyboard.is_pressed(calc_key):
                calc_total(mon_cnt, prl_cnt, gem_cnt)
        else:
            calc_total(mon_cnt, prl_cnt, gem_cnt)

    return


if "__main__" == __name__:
    x = 100
    y = 10
    w = 400
    h = 780
    calc_key = ''
    main(x, y, w, h, calc_key)
