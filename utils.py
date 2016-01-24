import gtk
import pygame
from pygame.locals import *
import math
import numpy as np
import random

import time


class Map():
    def __init__(self, Nod, Conn):
        self.Nod = Nod
        self.Conn = Conn
        self.hitbox = 15
        self.radius = 15
        self.connector_width = 5
        self.Open = False
        
        
        return None
    
    #Utils
    def get_pos(self):
        b = True
        while b is True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close_window()
                    return -1
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    b = False
        return pos    
    def count_infections(self, Veh, N):
        Np = 0
        Ni = 0
        for v in Veh:
            Np += v[3][0]
            Ni += v[3][1]
        for n in N:
            Np += n[0][0]
            Ni += n[0][1]
        return Np, Ni
            
        
    def disp_simulation(self):
        self.disp_map()
        #pygame.display.update()

    def disp_vehicles(self, Veh, N):
        self.blit_map()
        
        basicfont = pygame.font.SysFont(None, 20)
        text = basicfont.render('', True, (255, 0, 0), (255, 255, 255))
        textrect = text.get_rect()
        textrect.centerx = self.screen.get_rect().centerx
        textrect.centery = self.screen.get_rect().centery
         
        self.screen.blit(text, textrect)
        for i in range(0, len(self.Nod)):

            text = basicfont.render("Np:" + str(N[i][0][0])+", Ni:"+str(N[i][0][1]), True, (0, 0, 0), (255, 255, 255))
            textrect.centerx = self.Nod[i][2][0]+20
            textrect.centery = self.Nod[i][2][1]
            self.screen.blit(text, textrect)  
        [Np, Ni] = self.count_infections(Veh, N)
        text = basicfont.render('Np:' + str(Np), True, (0, 255, 0), (255, 255, 255))
        textrect.centerx = 20
        textrect.centery = 20
        self.screen.blit(text, textrect) 
            
        text = basicfont.render('Ni:' + str(Ni), True, (255, 0, 0), (255, 255, 255))
        textrect.centerx = 20
        textrect.centery = 40
        self.screen.blit(text, textrect)  
            
        for v in Veh:
            if int(v[7]) == 0:
                coor_n_act = self.Nod[v[2][0]][2]
                coor_n_next = self.Nod[v[2][1]][2]
                over = v[5]
                x = over * (coor_n_next[0] - coor_n_act[0]) + coor_n_act[0]
                y = over * (coor_n_next[1] - coor_n_act[1]) + coor_n_act[1]
                pygame.draw.circle(self.screen, self.Conn[v[1]][0], [int(x), int(y)], 7, 0)
                pygame.display.update()
            

        
        #pygame.display.flip()

            
    def disp_connectors(self):
        sim = []
        pair = []
        index_con = []
        for c in self.Conn:
            for i in range(0, len(c[1])):
                if i > 0:
                    self.Nod = count_connectors_per_node(self.Nod, self.Conn) 
                    n_prev = c[1][i-1]
                    n_actual = c[1][i]
                    """dif = list(set(n_prev) - set(n_actual))
                    for d in dif:
                        n_prev.remove(d)"""
                    pair.append([c[1][i-1], c[1][i]])
                    index_con.append(self.Conn.index(c))
                    pair[-1].sort()
        while len(pair) > 0:
            p = pair[0]            
            sim.append([pair[0], [index_con[0]]])
            pair.pop(0)
            index_con.pop(0)
            
            pos = []
            for i in range(0, len(pair)):
                if pair[i] == p:
                    pos.append(i)
            for j in range(0, len(pos)):
                sim[-1][1].append(index_con[pos[j] - j])
                pair.pop(pos[j] - j)
                index_con.pop(pos[j] - j)
         
        for s in sim:
            coor1 = np.asarray(self.Nod[s[0][0]][2])
            coor2 = np.asarray(self.Nod[s[0][1]][2])
            delta = coor2 - coor1
            n = len(s[1])
            d = -n/2.0 + 0.5
            
            distance = dist(coor1, coor2)
            if distance != 0:
                for i in range(0, len(s[1])):
                    Xa = coor1[0] - (d + i) * self.connector_width * delta[1] / distance
                    Ya = coor1[1] + (d + i) * self.connector_width * delta[0] / distance
                    Xb = coor2[0] - (d + i) * self.connector_width * delta[1] / distance
                    Yb = coor2[1] + (d + i) * self.connector_width * delta[0] / distance
                    pygame.draw.line(self.screen, self.Conn[s[1][i]][0], [Xa, Ya], [Xb, Yb], self.connector_width)    

    def disp_nodes(self):
        for node in self.Nod:
            pygame.draw.circle(self.screen, (0,   0,   0), node[2], self.radius, 0)

    def blit_map(self):
        self.screen.fill((250, 250, 250))
        self.disp_connectors()
        self.disp_nodes() 
        pygame.display.update()
        
    def disp_map(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1024, 800))
        pygame.display.set_caption('Network')
        # Fill background
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        background.fill((250, 250, 250))
        self.screen.blit(background, (0, 0))
        self.background = background
            
        """trajectory = []
        for connector in self.Conn:
            for id in connector[1]:
                trajectory.append(self.Nod[id][2])
                self.Nod[id][3] += 1
            pygame.draw.lines(self.screen, connector[0], False, trajectory, self.connector_width)    
        """
        self.disp_connectors()
        self.disp_nodes()

        # Blit everything to the screen
        pygame.display.flip()
        pygame.display.update()
        self.Open = True

    
    def close_window(self):
        pygame.display.quit()
        self.Open = False       
        
def dist(a, b):
     return math.sqrt(math.pow(b[0] - a[0], 2) + math.pow(b[1] - a[1], 2))
 
def count_connectors_per_node(Nod, Conn):
    for n in Nod:
        n[3] = []
    for connector in Conn:
        for id in connector[1]:
            Nod[id][3].append(Conn.index(connector))
    return Nod

def previous_node(c, i):
    id = c[1].index(i) - 1
    return c[1][id]

def next_node(c, i):
    id = c[1].index(i) + 1

    return c[1][id]

def update_vehicles(Veh):
    return 0
    
def generate_vehicles(Conn):
    V = []
    for i in range(0, len(Conn)):
        for j in range(0, Conn[i][2]):
            V.append([0, i, [Conn[i][1][0], Conn[i][1][1]], [random.randint(10, 40), random.randint(0, 3)], True, 0, [10, 10], j*10])
    
    return V