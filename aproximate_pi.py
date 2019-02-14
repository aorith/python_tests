import math
import cv2
import numpy as np
import random
import time

SIZE = 800
R = int(SIZE / 2)
CENTER = (R, R)
STARTTIME = time.time()

img = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)


# Gives de distance from the edge of the cirle
def dist(x, y):
    d = math.sqrt((x - CENTER[0])**2 + (y - CENTER[1])**2) - R
    return int(abs(d))


# Gives distance from the center of the circle
def dist_center(x, y):
    d = math.sqrt((x - CENTER[0])**2 + (y - CENTER[0])**2)
    return int(abs(d))


def diff_pi(pi):
    return abs(float((pi - math.pi)))


# Draw the circle
for x in range(SIZE):
    for y in range(SIZE):
        if dist_center(x, y) == R:
            img[x][y] = (255, 255, 255)

in_circle = 0
total = 0
record_pi = 3.1

while True:
    for i in range(500):
        total += 1
        x = random.randint(0, SIZE - 1)
        y = random.randint(0, SIZE - 1)
        if dist_center(x, y) < R:
            img[x][y] = (75, 255, 75)
            in_circle += 1
        else:
            img[x][y] = (255, 75, 75)

    cv2.imshow('Aproximate PI', img)
    k = cv2.waitKey(10)
    if k == 27:
        break
    pi = float(4 * float(float(in_circle) / float(total)))
    if diff_pi(pi) <= diff_pi(record_pi):
        record_pi = pi
        cv2.rectangle(img, (int(SIZE / 4.2), int(SIZE / 2.2)),
                      (int(SIZE / 1.4), int(SIZE / 1.9)), (0, 0, 0), -1)
        cv2.putText(img, str(record_pi), (int(SIZE / 4), int(SIZE / 2)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2)

    cv2.rectangle(img, (int(SIZE / 4.2), int(SIZE / 4.9)),
                  (int(SIZE / 1.4), int(SIZE / 3.6)), (0, 0, 0), -1)
    cv2.putText(img, str(pi), (int(SIZE / 4), int(SIZE / 4)),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2)

    endtime = time.time() - STARTTIME
    hour = int(endtime // 3600)
    endtime %= 3600
    minutes = int(endtime // 60)
    endtime %= 60
    seconds = int(endtime)
    time_str = str(hour) + ":" + str(minutes) + ":" + str(seconds)
    print(f"{hour}:{minutes}:{seconds}: Current: {pi}\t Best: {record_pi}")


cv2.destroyAllWindows()
