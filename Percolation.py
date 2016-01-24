import numpy as np
from random import randint
import pygame
from pygame.locals import *
from time import sleep


class Percolation():
    def __init__(self, size, distance, nPassenger, nInfected, duration, latency):
        self.size = size
        self.nPassenger = nPassenger
        self.nInfected = nInfected
        self.distance = distance
        
        self.iter = int(duration // latency)

        #self.duration = duration
        #self.latency = latency
        #Grid initialization
        grid = np.zeros(self.size)  
        for i in range(0, self.nPassenger):
            x = randint(0, self.size[0]-1)
            y = randint(0, self.size[1]-1)
            while grid[x][y] != 0:
                x = randint(0, self.size[0]-1)
                y = randint(0, self.size[1]-1)
            
            if i <= self.nInfected:
                grid[x][y] = 2
            else:
                grid[x][y] = 1
        self.grid = grid
        #pygame.init()
        #self.screen = pygame.display.set_mode(50*np.asarray(size))
            
    def checkAndChange(self, x, y, shiftX, shiftY, distanceLeft):
        tempMe = 3
        adverse = 1
        
        if x < self.size[0] and  x >= 0  and y < self.size[1] and y >= 0:#If it finds ones cell it returns true
            if self.grid[x][y] == adverse:
                self.grid[x][y] = tempMe
            if distanceLeft > 0:  # and x < 0 and x >= self.size[0] - 1 and y < 0 and y >= self.size[1]:
                self.checkAndChange(x + shiftX, y + shiftY, shiftX, shiftY, distanceLeft - 1)
    
    
    def allCheck(self, pos):
        x = pos[0];
        y = pos[1];
        #if x < self.size[0] and  x >= 0  and y < self.size[1] and y >= 0:#Check if cell is already occupied
        self.checkAndChange(x+1, y, 1, 0, self.distance-1)
        self.checkAndChange(x-1, y, -1, 0, self.distance-1)
        self.checkAndChange(x, y+1, 0, 1, self.distance-1)
        self.checkAndChange(x, y-1, 0, -1, self.distance-1)
        self.checkAndChange(x+1, y+1, 1, 1, self.distance-1)
        self.checkAndChange(x-1, y-1, -1, -1, self.distance-1)
        self.checkAndChange(x+1, y-1, 1, -1, self.distance-1)
        self.checkAndChange(x-1, y+1, -1, 1, self.distance-1)
            
    def disp(self):
        i = self.size[0] - 1
        while i > 0:
            j = self.size[1] - 1
            while j > 0:
                if self.grid[i][j] == 1:    
                    pygame.draw.circle(self.screen, (255,   0,   0), 40*np.array([j, i])+50, 10, 0)
                if self.grid[i][j] == 2:  
                    pygame.draw.circle(self.screen, (  0, 255,   0), 40*np.array([j, i])+50, 10, 0)
                j -= 1
            i -= 1
        pygame.display.flip()
        pygame.display.update()
        
    def percolation(self):
        #print self.grid
        if self.nPassenger == 0 and self.nInfected == 0:
            return [0, 0]
        for n in range(0, self.iter):
            #sleep(1) #I have to move this sleep call to the method where I display Percolation
            for i in range(0, self.size[0]):
                for j in range(0, self.size[1]):
                    if self.grid[i][j] == 2:
                        self.allCheck([i, j])

            for i in range(0, self.size[0]):
                for j in range(0, self.size[1]):                
                    if self.grid[i][j] == 3:
                        self.grid[i][j] = 2
            #self.disp()
        #print "\n\n"
        Np = 0
        Ni = 0
    
        for i in range(0, self.size[0]):
            for j in range(0, self.size[1]):   
                if self.grid[i][j] == 2:
                    Ni += 1  
                if self.grid[i][j] != 0:
                    Np += 1 
        return [Np, Ni]
        #print self.grid
        #self.disp()
                
                
        
        
