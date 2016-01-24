import utils
import time
import random
import numpy as np
from Percolation import Percolation

class Simulation():
    def __init__(self, n_passenger, n_infected, Nods, Conns):
        self.n_passenger = n_passenger
        self.n_infected = n_infected
        self.clock = 0
        self.sec = 0.5
        self.Connectors = Conns
        self.Nodes = Nods
        
 
              
    def simulate_percolation(self, v):
        #size, distance, nPassenger, nInfected, duration, latency):
        n = v[2][1]
        Node = self.Nodes[n]
        N = self.N[n]
        B = Percolation(v[6], 1, v[3][0], v[3][1], int(self.clock-v[0]), 5)
        v[3] = B.percolation()
        C = Percolation(Node[1], 1, N[0][0], N[0][1], int(self.clock - N[1]), 5)
        self.N[v[2][1]][0] = C.percolation()
        return v

               
    def simulate_vehicles(self, Veh, N):
        self.N = N
        for v in Veh:
            if int(v[7]) == 0:
                coor_n_act = self.Nodes[v[2][0]][2]
                coor_n_next = self.Nodes[v[2][1]][2]
                a_t = self.clock
                f_t = utils.dist(coor_n_act, coor_n_next) / self.Connectors[v[1]][3]
                over = (a_t - v[0]) / (f_t)
                v[5] = over
                if over >= 1:
                    v = self.simulate_percolation(v)
                    (v[3], self.N[v[2][1]][0]) = self.transvase(v)
                    self.N[v[2][1]][1] = 18
                    self.N[v[2][1]][1] = self.clock
                    v[0] = self.clock
                    if v[2][1] == self.Connectors[v[1]][1][-1]:
                        v[4] = False
                    elif v[2][1] == self.Connectors[v[1]][1][0]:
                        v[4] = True
                        
                    if v[4]:
                        v[2][0] = v[2][1]
                        v[2][1] = utils.next_node(self.Connectors[v[1]], v[2][0])
                    elif not v[4]:
                        v[2][0] = v[2][1]
                        v[2][1] = utils.previous_node(self.Connectors[v[1]], v[2][0])
            else:
                v[7] -= self.sec
                v[0] = self.clock
        self.clock += self.sec
        time.sleep(0.03)        
        return [self.N, Veh]
    
    def room_left(self, size, n_occupied_cell):
        return size[0]*size[1] - n_occupied_cell
    
    def transvase(self, vehicle):
        Nv = np.asarray(vehicle[3])
        Nn = np.asarray(self.N[vehicle[2][1]][0])
        R = self.room_left(self.Nodes[vehicle[2][1]][1], Nn[0])
        Nt = np.asarray([0]*2)
        while True:
            Nt[0] = random.randint(0, Nv[0])
            if Nt[0] <= R:
                while True:
                    Nt[1] = random.randint(0, Nv[1])
                    if Nt[1] <= Nt[0]:
                        if  Nv[0] - Nt[0] >= Nv[1] - Nt[1]:
                            Nv -= Nt
                            Nn += Nt
                            break
                break
                
        R = self.room_left(vehicle[6], Nv[0])
        Nt = np.asarray([0]*2)
        while True:
            Nt[0] = random.randint(0, Nn[0])
            if Nt[0] <= R:
                while True:
                    Nt[1] = random.randint(0, Nn[1])
                    if Nt[1] <= Nt[0]:
                        if Nn[0] - Nt[0] >= Nn[1] - Nt[1]:
                            Nn -= Nt
                            Nv += Nt
                            break
                break
        return list(Nv), list(Nn)        
        