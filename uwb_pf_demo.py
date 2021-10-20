import random
import numpy as np
import helpers
import read_data
import time
from helpers import draw_particles, resize_and_plot, draw_robot
from robot import robot

## parameters
#data_file = '0926test3.data'
data_file = '10-14-21-test1.data'
world_size = 500
RESIZE = 500
scale = 100.0
D = 34 * 25.4/ scale  # mm to px distance between UWBs on a drone
circle_size = 2 # for plot

## hyperparameters
N = 2000  # num of particles
noise = 3  # px

## extract data
experimental_data = read_data.Preprocessing(filename=data_file, scale=scale)
measurements = experimental_data.get_all_measurements()

## initialize robot (Drone 1)
myrobot = robot(world_size, noise, scale=scale)
myrobot.set(new_a2x=world_size / 2 + D / 2, new_a2y=world_size / 2, new_orientation=np.pi / 2)
Z = myrobot.sense(experimental_data.get_measurement())
# print(Z)
T = 2164

## initialize N particles
p = []
for i in range(N):
    r = robot(world_size, noise, scale)
    r.set_noise(noise, noise, noise)
    p.append(r)
canvas = np.ones((world_size, world_size, 3), np.uint8) * 255
draw_particles(p, canvas, circle_size, color=(255, 0, 0))
draw_robot(myrobot, canvas, circle_size
           )
resize_and_plot(canvas, RESIZE)

# iterate through each time step (pressing a key is required)

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
    # print(max(w), w)
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
    draw_robot(myrobot, canvas, circle_size)
    draw_particles(p, canvas, circle_size, color=(255, 0, 0))
    resize_and_plot(canvas, RESIZE)
    # print('error: ', myrobot.x, myrobot.y, helpers.eval(myrobot, p, world_size))
