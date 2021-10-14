# Please only modify the indicated area below!

from math import *
import random
import cv2
import read_data
import numpy as np


class robot:
    def __init__(self, world_size, noise, scale):
        self.orientation = random.random() * 2.0 * pi
        self.THREE_FEET = 914.4 / scale
        self.a2x = random.random() * world_size
        self.a2y = random.random() * world_size
        self.b2x = self.a2x + np.cos(self.orientation + np.pi/2) * self.THREE_FEET
        self.b2y = self.a2y + np.sin(self.orientation + np.pi/2) * self.THREE_FEET
        self.x = (self.a2x + self.b2x) / 2
        self.y = (self.a2y + self.b2y) / 2
        self.forward_noise = noise * 2
        self.turn_noise = noise
        self.sense_noise = noise
        self.world_size = world_size
        self.scale = scale

    def set(self, new_a2x, new_a2y, new_orientation):
        # if new_x < 0 or new_x >= self.world_size:
        #     raise (ValueError, 'X coordinate out of bound')
        # if new_y < 0 or new_y >= self.world_size:
        #     raise (ValueError, 'Y coordinate out of bound')
        # if new_orientation < 0 or new_orientation >= 2 * pi:
        #     raise (ValueError, 'Orientation must be in [0..2pi]')
        self.a2x = float(new_a2x)
        self.a2y = float(new_a2y)
        self.b2x = self.a2x + self.THREE_FEET * cos(new_orientation + np.pi/2)
        self.b2y = self.a2y + self.THREE_FEET * sin(new_orientation + np.pi/2)
        self.x = (self.a2x + self.b2x) / 2
        self.y = (self.a2y + self.b2y) / 2
        self.orientation = float(new_orientation)

    def set_noise(self, new_f_noise, new_t_noise, new_s_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.forward_noise = float(new_f_noise)
        self.turn_noise = float(new_t_noise)
        self.sense_noise = float(new_s_noise)

    def sense(self, measurements):
        return measurements
        # Z = []
        # for i in range(len(landmarks)):
        #     dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
        #     dist += random.gauss(0.0, self.sense_noise)
        #     Z.append(dist)
        # return Z

    def move(self, turn, forward):
        if forward < 0:
            raise (ValueError, 'Robot cant move backwards')

        # turn, and add randomness to the turning command
        orientation = self.orientation + float(turn) + random.gauss(0.0, self.turn_noise)
        orientation %= 2 * pi

        # move, and add randomness to the motion command
        dist = float(forward) + random.gauss(0.0, self.forward_noise)
        # self.x = (self.a2x + self.b2x) / 2
        # self.y = (self.a2y + self.b2y) / 2
        new_a2x = self.a2x + (cos(orientation) * dist)
        new_a2y = self.a2y + (sin(orientation) * dist)

        new_b2x = self.b2x + (cos(orientation) * dist)
        new_b2y = self.b2y + (sin(orientation) * dist)
        # x %= self.world_size  # cyclic truncate
        # y %= self.world_size

        # set particle
        res = robot(self.world_size, self.sense_noise, self.scale)
        res.set(new_a2x=new_a2x, new_a2y=new_a2y, new_orientation=orientation)
        res.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
        return res

    def Gaussian(self, mu, sigma, x):
        # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
        return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))

    def measurement_prob(self, measurement):
        # calculates how likely a measurement should be
        # x = self.x
        # y = self.y
        a1a2, a1b2, b1a2, b1b2 = measurement
        r_a1a2 = sqrt(
            (self.a2x - self.world_size / 2 - self.THREE_FEET / 2) ** 2 + (
                        self.a2y - self.world_size / 2) ** 2)  # dist to b1
        r_a1b2 = sqrt(
            (self.b2x - self.world_size / 2 - self.THREE_FEET / 2) ** 2 + (
                        self.b2y - self.world_size / 2) ** 2)  # dist to a1

        r_b1a2 = sqrt(
            (self.a2x - self.world_size / 2 + self.THREE_FEET / 2) ** 2 + (
                        self.a2y - self.world_size / 2) ** 2)  # dist to b1
        r_b1b2 = sqrt(
            (self.b2x - self.world_size / 2 + self.THREE_FEET / 2) ** 2 + (
                        self.b2y - self.world_size / 2) ** 2)  # dist to b1

        r_a2b2 = sqrt((self.a2x - self.b2x) ** 2 + (self.a2y - self.b2y) ** 2) - self.THREE_FEET

        diff = (abs(r_a2b2) + abs(r_a1a2 - a1a2) + abs(r_a1b2 - a1b2) + abs(
            r_b1a2 - b1a2 ) + abs(r_b1b2 - b1b2))

        print('diff', diff, abs(r_a2b2), abs(r_a1a2 - a1a2), abs(r_a1b2 - a1b2),
              abs(r_b1a2 - b1a2), abs(r_b1b2 - b1b2))
        # for i in range(len(measurement)):
        #     dist = measurement[i]

        prob = self.Gaussian(mu=0, sigma=self.sense_noise, x=diff)
        # print('prob',prob)
        return prob

    def get_x(self):
        return (self.a2x + self.b2x) / 2

    def get_y(self):
        return (self.a2y + self.b2y) / 2

    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))
