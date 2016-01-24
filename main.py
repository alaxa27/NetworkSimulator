#!/usr/bin/python


import time

import gtk

from utils import Map
import utils
import numpy as np
import time
import pickle

import pygame
from Simulation import Simulation

class NetworkSimulator(gtk.Window): 
    def __init__(self):
        super(NetworkSimulator, self).__init__()
        
        self.set_size_request(300, 500)
        self.set_position(gtk.WIN_POS_CENTER)
        self.connect("destroy", self.destroy)
        self.set_title("Difficult Networking")
        
        
        self.info = gtk.Label("Wilkommen!")

        
        addNodeBTN = gtk.Button("+ Node")
        addNodeBTN.connect("clicked", self.add_node)
        
        addConnectorBTN = gtk.Button("+ Connector")
        addConnectorBTN.connect("clicked", self.add_connector)
        
        simulateBTN = gtk.Button("Simulate!")
        simulateBTN.connect("clicked", self.start_simulation)

        fix = gtk.Fixed()
        #fix.put(button, 100, 30)
        fix.put(addNodeBTN, 100, 30)
        fix.put(addConnectorBTN, 100, 100)
        fix.put(self.info, 30, 200)
        fix.put(simulateBTN, 100, 400)
        self.add(fix)

        self.show_all()
        self.Nodes = [['St Laz', (10, 10), (127, 193), [], 0],
                      ['Madeleine', (10, 10), (352, 313), [], 0],
                      ['Pyramide', (10, 10), (390, 101), [], 0],
                      ['Univ', (10, 10), (148, 376), [], 0]]
        self.Connectors = [[(86, 145, 16), [3, 0, 1, 2], 3, 10],
                           [(30, 0, 255), [2, 1, 0], 1, 15]]

        self.Nodes = []
        fh = open("data2", 'r')
        if len(fh.read()) == 0:
            with open("data2", 'wb') as f:
                pickle.dump([self.Connectors, self.Nodes], f)
        with open("data2", 'rb') as f:
            self.h = pickle.load(f)
        self.Connectors = self.h[0]
        self.Nodes = self.h[1]


        #fh = open("data", "r")
        #a = fh.readlines()
        #self.Connectors = 
        
  
    def destroy(self, widget, data=None):
        fh = open("data", "w")
        fh.write(str(self.Connectors))
        fh.close()
        fh = open("data", "a")
        fh.write("\n"+ str(self.Nodes))
        fh.close()
        
        with open("data2", 'wb') as f:
            pickle.dump([self.Connectors, self.Nodes], f)
        gtk.main_quit()     
         
    def start_simulation(self, widget):
        N = []
        t_zero = time.time()
        for i in range(0, len(self.Nodes)):
            N.append([[0, 0], 0])
        
        M = Map(self.Nodes, self.Connectors)
        S = Simulation(10, 2, self.Nodes, self.Connectors)
        print "Nodes: " + str(self.Nodes)
        print "Connectors: " + str(self.Connectors)
        self.Vehicles = utils.generate_vehicles(self.Connectors)
        print "Vehicles: "  + str(self.Vehicles)
        M.disp_map()
        while True:
            time.sleep(0.05)
            [N, self.Vehicles] = S.simulate_vehicles(self.Vehicles, N)
            M.disp_vehicles(self.Vehicles, N)
            #M.disp_infections(self.Vehicles, N)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    M.close_window()
                    #DB.save(x)
                    self.info.set_text("Runtime: " + str(time.time() - t_zero) + "s")
                    print "Runtime: " + str(time.time() - t_zero) + "s"
                    return 0
                
        
            
            

#####################################################################################################    
    def add_node(self, widget):
        self.newNode = [-1]*4
        self.newNode[3] = []
        
        dialog = gtk.Dialog("Add a node",
                   None,
                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                   (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                    gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        dialog.vbox.set_spacing(10)
        
        e_name = gtk.Entry()
        e_name.set_text("Name")
        dialog.vbox.pack_start(e_name)
        
        
        l_size = gtk.Label("Size")
        dialog.vbox.pack_start(l_size)

        box_size = gtk.HBox(True, 10)
        

        e_x = gtk.Entry()
        self.numbify(e_x)
        box_size.pack_start(e_x) 
        
        e_y = gtk.Entry()
        self.numbify(e_y)
        box_size.pack_end(e_y)
        dialog.vbox.pack_start(box_size)
        
        b_nodePos = gtk.Button("Select Node Position")
        b_nodePos.connect("clicked", self.get_node_pos)
        dialog.vbox.pack_start(b_nodePos)

        dialog.show_all()
        response = dialog.run()
        self.newNode[0] = e_name.get_text()
        self.newNode[1] = (e_x.get_text(), e_y.get_text())

        if response == gtk.RESPONSE_ACCEPT:
            r = self.is_node_ok(self.newNode)
            # L'utilisateur valide
            if r is True:
                self.newNode[1] = (int(e_x.get_text()), int(e_y.get_text()))
                self.Nodes.append(self.newNode)
                self.info.set_text("Node has been added successfully!")
                print "node created"
                print self.newNode
            else:
                self.info.set_text(str(r))
                dialog.destroy()
                return -1
        else:
            # L'utilisateur annule (soit gtk.RESPONSE_CANCEL, soit gtk.RESPONSE_NONE)
            print"Cancel"
     
        del(self.newNode)
        dialog.destroy()
       
    def get_node_pos(self, widget):
        NNM = Map(self.Nodes, self.Connectors)
        NNM.disp_map()
        self.newNode[2] = NNM.get_pos()
        NNM.close_window()
    
    def is_node_ok(self, node):
        if len(node[1][0]) < 1 or len(node[1][1]) < 1:
            return "Node size not correct"
        if node[0] == '':
            return "Fill the name field"
        for n in self.Nodes:
            if n[0] == node[0]:
                return "Name already used"
            if node[2] != -1:
                M = Map(self.Nodes, self.Connectors)
                if utils.dist(n[2], node[2]) < M.hitbox:
                    return "Node too close to a peer"
                del(M)
            else:
                return "Choose a position for the node"
        return True
#####################################################################################################    

#####################################################################################################            
    def add_connector(self, widget):
        self.newConnector = [(0, 0, 0), [], 0, 10]
        
        dialog = gtk.Dialog("Add a connector",
                   None,
                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                   (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                    gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        dialog.vbox.set_spacing(10)
        
        b_connectorSpec = gtk.Button("Connect The Nodes")
        b_connectorSpec.connect("clicked", self.get_connector_spec)
        dialog.vbox.pack_start(b_connectorSpec)
        
        l_vehicle_nb = gtk.Label("Vehicle number:")
        dialog.vbox.pack_start(l_vehicle_nb)
        
        e_vehicle_nb = gtk.Entry()
        self.numbify(e_vehicle_nb)
        dialog.vbox.pack_start(e_vehicle_nb) 
        
        l_vehicle_sp = gtk.Label("Vehicle speed:")
        dialog.vbox.pack_start(l_vehicle_sp)
        
        e_vehicle_sp = gtk.Entry()
        self.numbify(e_vehicle_sp)
        dialog.vbox.pack_start(e_vehicle_sp)
        
        l_pick_color = gtk.Label("Pick a connector color")
        dialog.vbox.pack_start(l_pick_color)
        
        colorselwidget = gtk.ColorSelection()
        dialog.vbox.pack_start(colorselwidget)
        
        dialog.show_all()
        response = dialog.run()
        if response == gtk.RESPONSE_ACCEPT:
            # L'utilisateur valide
            if self.is_connector_ok(self.newConnector) is True:
                self.newConnector[0] = self.hex_to_rgb(str(colorselwidget.get_current_color()))
                self.newConnector[2] = int(e_vehicle_nb.get_text())
                self.newConnector[3] = int(e_vehicle_sp.get_text())
                self.Connectors.append(self.newConnector)
                self.Nodes = utils.count_connectors_per_node(self.Nodes, self.Connectors)
                self.info.set_text("Connector has been added successfully!")
                print "connector created"
            else:
                self.info.set_text("Error creating connector")
                dialog.destroy()
                return -1
        else:
            # L'utilisateur annule (soit gtk.RESPONSE_CANCEL, soit gtk.RESPONSE_NONE)
            print"Cancel"
    
            #message d'erreur AFAIRE
        del self.newConnector
        dialog.destroy()
        return 0
    
    def get_connector_spec(self, widget):
        NCM = Map(self.Nodes, self.Connectors)
        #NCM.Connectors.append(self.newConnector)
        while True:
            NCM.Conn.append(self.newConnector)
            NCM.disp_map()#, self.newConnector])
            NCM.Conn.pop(-1)
            pos = NCM.get_pos()
            if not NCM.Open:
                del(NCM)
                return 0
            for node in self.Nodes:
                if utils.dist(pos, node[2]) < NCM.hitbox:
                    if len(self.newConnector[1]) < 1:
                        self.newConnector[1].append(self.Nodes.index(node))
                    elif pos != self.newConnector[1][-1]:
                        self.newConnector[1].append(self.Nodes.index(node))
                        #NCM.Conn.append(self.newConnector)
                        #NCM.Connectors[-1][1].append(self.Nodes.index(node))

    def is_connector_ok(self, connector):
        if len(connector[1]) < 2:
            return False
        for n in self.Nodes:
            if n[0] == connector[0]:
                return False
        return True
#####################################################################################################    
        
    def numbify(self, widget):
        def filter_numbers(entry, *args):
            text = entry.get_text().strip()
            entry.set_text(''.join([i for i in text if i in '0123456789']))

        widget.connect('changed', filter_numbers)

    def hex_to_rgb(self, value):
        value = value.lstrip('#')
        lv = len(value)
        a = tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))
        a = list(a)
        for i in a:
            m = a.index(i)
            a[m] = i/255
            if a[m] > 2:
                a[m] -= 2

        return tuple(a)
    

NetworkSimulator()
gtk.main()
