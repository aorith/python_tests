from math import sqrt, pi
from cv2 import imshow, waitKey, destroyAllWindows, rectangle, putText, FONT_HERSHEY_SIMPLEX
from numpy import zeros, uint8
from random import randint
from time import time
from argparse import ArgumentParser

ap = ArgumentParser()
ap.add_argument("-s", "--size", required=False, type=int, default=800,
                help="size of the square")
ap.add_argument("-l", "--loops", required=False, type=int, default=1000,
                help="number of loops per second")
args = vars(ap.parse_args())

SIZE = args["size"]
R = int(SIZE / 2)
CENTER = R
STARTTIME = time()
NUM_LOOPS = args["loops"]

img = zeros((SIZE, SIZE, 3), dtype=uint8)
info = zeros((150, 600), dtype=uint8)


# Gives de distance from the edge of the cirle
def dist(x, y):
    d = sqrt((x - CENTER)**2 + (y - CENTER)**2) - R
    return int(abs(d))


# Gives distance from the center of the circle
def dist_center(x, y):
    d = sqrt((x - CENTER)**2 + (y - CENTER)**2)
    return int(abs(d))


def diff_mypi(mypi):
    return abs(float(mypi - pi))


# Draw the circle
for x in range(SIZE):
    for y in range(SIZE):
        if dist_center(x, y) == R:
            img[x][y] = (255, 255, 255)

in_circle = 0
total = 0
record_mypi = 3.1

while True:
    loop_time = time()
    for i in range(NUM_LOOPS):
        total += 1
        x = randint(0, SIZE - 1)
        y = randint(0, SIZE - 1)
        if dist_center(x, y) < R:
            img[x][y] = (50, randint(180,255), 50)
            in_circle += 1
        else:
            img[x][y] = (randint(185,255), 50, 50)

    imshow('Aproximate PI - Press <ESC> to quit.', img)
    imshow('Current and record of PI.', info)
    k = waitKey(10)
    if k == 27:
        break
    mypi = float(4 * float(float(in_circle) / float(total)))

    info.fill(255)
    putText(info, 'Current: ' + str(mypi), (50,50), FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)

    if diff_mypi(mypi) <= diff_mypi(record_mypi):
        record_mypi = mypi
    putText(info, 'Record: ' + str(record_mypi), (50,120), FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)

    endtime = time() - STARTTIME
    hour = int(endtime // 3600)
    endtime %= 3600
    minutes = int(endtime // 60)
    endtime %= 60
    seconds = int(endtime)
    time_str = str(hour) + ":" + str(minutes) + ":" + str(seconds)
    loop_time = time() - loop_time
    speed = int(NUM_LOOPS / loop_time)
    print(f"{hour}:{minutes}:{seconds}: Current: {mypi}\t Best: {record_mypi}\t Speed: {speed} loops/s")

destroyAllWindows()
