from math import *

import cv2


def resize_and_plot(canvas, resize):
    resized = cv2.resize(canvas, (resize, resize), interpolation=cv2.INTER_AREA)
    cv2.imshow('resized', resized)
    cv2.waitKey(1000)

def draw_particles(particles, canvas, circle_size, color=(0, 255, 0)):
    for p in particles:
        x = int(round((p.a2x + p.b2x)/2))
        y = int(round((p.a2y + p.b2y)/2))
        # print(x, y)
        cv2.circle(canvas, (x, y), circle_size, color, -1)


def eval(r, p, world_size):
    sum = 0.0
    for i in range(len(p)):  # calculate mean error
        # dx = (p[i].get_x() - r.x + (world_size / 2.0)) % world_size - (world_size / 2.0)
        dx = (p[i].get_x() - r.x)
        # dy = (p[i].get_y() - r.y + (world_size / 2.0)) % world_size - (world_size / 2.0)
        dy = (p[i].get_y() - r.y)
        err = sqrt(dx * dx + dy * dy)
        sum += err
    return sum / float(len(p)), (r.x, r.y)

def draw_robot(myrobot, canvas, circle_size):
    cv2.circle(canvas, (int(round(myrobot.x)), int(round(myrobot.y))), circle_size, (0, 0, 0), -1)
