import random

import numpy
import numpy as np
import helpers
import read_data
from helpers import draw_particles, resize_and_plot, draw_robot, draw_best_guess_particle
from robot import robot
import cv2

import math
from scipy.io import savemat


## parameters
data_file = '0926test3.data'
data_file = '10-14-21-tests/10-14-21-test1'
data_file = '10-14-21-tests/10-14-21-test4'
data_file = '11-23-21-tests/11-23-21_test1'
#data_file = '11-23-21-tests/11-23-21_test4'
data_file = '11-23-21-tests/11-23-21_test6'
world_size = 500
RESIZE = 500
scale = 30.0
D = 863.6 / scale  # mm to px (distance between modules on a drone)
circle_size = 2  # for plot

## hyperparameters
N = 2000  # num of particles
noise = 10  # px

# open file in read mode
with open(data_file, 'r') as fp:
    for num_meas, line in enumerate(fp):
        pass

## extract data
experimental_data = read_data.Preprocessing(filename=data_file, scale=scale)
measurements = experimental_data.get_all_measurements()
## initialize robot (Drone 1)
myrobot = robot(world_size, noise, D, scale=scale)
myrobot.set(new_a2x=world_size / 2 + D / 2, new_a2y=world_size / 2, new_orientation=np.pi / 2)
Z = myrobot.sense(experimental_data.get_measurement())
# print(Z)
T = len(measurements['time'])

## initialize N particles
p = []
for i in range(N):
    r = robot(world_size, noise, D, scale)
    r.set_noise(noise, noise, noise)
    p.append(r)
canvas = np.ones((world_size, world_size, 3), np.uint8) * 255
# draw_particles(p, canvas, circle_size, color=(255, 0, 0))
draw_robot(myrobot, canvas, circle_size)
resize_and_plot(canvas, RESIZE)

# iterate through each time step
data_set= {'a2x':[], 'a2y':[], 'b2x':[], 'b2y':[], 'time': []}
for t in range(T-1):

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
    # draw_particles(p, canvas, circle_size, color=(255, 0, 0))
    #for i in range(N):
    ## w = w/np.sum(w)
    a2x_values = []
    a2y_values = []
    b2x_values = []
    b2y_values = []

    for particle in p:
        a2x_values.append(particle.a2x)
        a2y_values.append(particle.a2y)
        b2x_values.append(particle.b2x)
        b2y_values.append(particle.b2y)
    w = np.array(w)
    w = w / np.sum(w)
    BestGuess_a2x = int(np.array(a2x_values) @ w.transpose())
    BestGuess_a2y = int(np.array(a2y_values) @ w.transpose())
    BestGuess_b2x = int(np.array(b2x_values) @ w.transpose())
    BestGuess_b2y = int(np.array(b2y_values) @ w.transpose())

    a2 = (BestGuess_a2x, BestGuess_a2y)
    b2 = (BestGuess_b2x, BestGuess_b2y)
    data_set['a2x'].append((BestGuess_a2x-world_size/2)*scale/1000)
    data_set['a2y'].append((BestGuess_a2y-world_size/2)*scale/1000)
    data_set['b2x'].append((BestGuess_b2x-world_size/2)*scale/1000)
    data_set['b2y'].append((BestGuess_b2y-world_size/2)*scale/1000)
    data_set['time'].append(Z[4])
    # for particles in p:
       # BestGuess_a2x += particles.a2x * w

    #draw_best_guess_particle(p, canvas, color=(255, 0, 0))
    cv2.line(canvas, a2, b2, (255, 0, 0), 1)
    cv2.circle(canvas, (int(BestGuess_b2x), int(BestGuess_b2y)), 2, (255, 0, 0), -1)

    resize_and_plot(canvas, RESIZE)
    # print('error: ', myrobot.x, myrobot.y, helpers.eval(myrobot, p, world_size))
    print(t)
savemat(data_file + '_pf_noise' + str(noise) + '.mat', data_set) # units are in meters