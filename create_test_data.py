import numpy as np
from random import *
from math import *


class create_data:
    gaussian_random = 0.0
    check = False
    speeds = [20,30,40,50,60,70]
    max_range = 1.

    def __init__(self,complexity,average_price,std_price):
        self.complexity = complexity
        self.average_price = average_price
        self.std_price = std_price

    def box_muller(self,mean,std):
        if(create_data.check == False):
            u1 = random()
            u2 = random()
            create_data.gaussian_random = (sqrt(-2.0*log(u1))*sin(2.0*pi*u2)*std) + mean
            create_data.check = not create_data.check
            return (sqrt(-2.0*log(u1))*cos(2.0*pi*u2)*std) + mean
        elif(create_data.check == True):
            create_data.check = not create_data.check
            return create_data.gaussian_random

    def expand_2D_array(array):
        size = np.shape(array)
        new = np.zeros((2*size[0],size[1]))
        for i in range(size[0]):
            new[i,:] = array[i,:]
        return new

    def cut_2D_array(array,length):
        size = np.shape(array)
        new = np.zeros((length,size[1]))
        for i in range(length):
            new[i,:] = array[i,:]
        return new

    def create_route(self,distance):
        num_nodes = 10
        #data format is: distance from previous node, speed of next section
        dist_vel_data = np.zeros((num_nodes,2))

        displacement = 0
        count = 0

        while(displacement <= distance):
            if(count == num_nodes):
                dist_vel_data = create_data.expand_2D_array(dist_vel_data)
                num_nodes *= 2

            vel = create_data.speeds[int(6 * random())]
            dist = random() * distance / self.complexity

            dist_vel_data[count,0] = dist
            dist_vel_data[count,1] = vel
            if(count == 0):
                dist_vel_data[count,0] = 0
            displacement += dist
            count += 1
        dist_vel_data = create_data.cut_2D_array(dist_vel_data,count)
        return dist_vel_data

    def create_stations(self,dist_vel_data):
        num_nodes = np.shape(dist_vel_data)[0]
        print("num of nodes = {}".format(num_nodes))
        num_stations = num_nodes
        #data format is: node number, distance from node, price
        petrol_stations = np.zeros((num_stations,3))

        count = 0
        check = True
        while(check):
            print("Adding stations")
            for i in range(num_nodes):
                n = int(create_data.box_muller(self,1,1))
                for j in range(n):

                    if(count == num_stations):
                        petrol_stations = create_data.expand_2D_array(petrol_stations)
                        num_stations *= 2

                    petrol_stations[count,0] = i
                    petrol_stations[count,1] = random() * create_data.max_range
                    petrol_stations[count,2] = create_data.box_muller(self,self.average_price,self.std_price)
                    count += 1
            if(count >= 2):
                check = not check
        petrol_stations = create_data.cut_2D_array(petrol_stations,count)
        return petrol_stations

seed()
x = create_data(1,1.35,0.05)
route = x.create_route(10)
stations = x.create_stations(route)
