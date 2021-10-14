import random
import numpy as np

import helpers
import read_data
from helpers import draw_particles, resize_and_plot, draw_robot
from robot import robot

world_size = 1000
RESIZE = 500
scale = 100.0
THREE_FEET = 914.4 / scale #mm to px
N = 1000
noise = 5 # px


experimental_data = read_data.Preprocessing(scale=scale)

myrobot = robot(world_size, noise, scale=scale)
myrobot.set(new_a2x=world_size / 2 + THREE_FEET / 2, new_b2x= world_size / 2 - THREE_FEET/2, new_a2y=world_size / 2, new_b2y=world_size / 2, new_orientation=0)

Z = myrobot.sense(experimental_data.get_measurement())
# print(Z)
T = 30

p = []
for i in range(N):
    r = robot(world_size, noise, scale)
    r.set_noise(noise, noise, noise)
    p.append(r)
canvas = np.ones((world_size, world_size, 3), np.uint8) * 255
draw_particles(p, canvas)
draw_robot(myrobot, canvas)
resize_and_plot(canvas, RESIZE)


def print_particles(p):
    for particle in p:
        print(particle.a2x, particle.a2y, particle.b2x, particle.b2y)


for t in range(T):
    canvas = np.ones((world_size, world_size, 3), np.uint8) * 255
    # myrobot = myrobot.move(0.0, 0.0)
    Z = myrobot.sense(experimental_data.get_measurement())

    # move particles according to robot motion
    p2 = []
    for i in range(N):
        p2.append(p[i].move(0, 0))
    p = p2

    w = []
    for i in range(N):
        w.append(p[i].measurement_prob(Z))
    # print('weights')
    print(max(w), w)
    p3 = []
    index = int(random.random() * N)
    beta = 0.0
    mw = max(w)
    for i in range(N):
        beta += random.random() * 2.0 * mw
        while beta > w[index]:
            beta -= w[index]
            index = (index + 1) % N
        p3.append(p[index])
    p = p3
    # print_particles(p)
    draw_robot(myrobot, canvas)
    draw_particles(p, canvas)
    resize_and_plot(canvas, RESIZE)
    print('error: ', myrobot.x, myrobot.y, helpers.eval(myrobot, p, world_size))

