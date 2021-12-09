#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 22:18:06 2021

@author: peeyushkumar

numpy version used : '1.19.5'
"""



import numpy as np
from sys import maxsize
from itertools import permutations


if np.__version__ != '1.19.5':
    print('Warning')
    print('This modeule used version 1.19.5 and your are using {}'.format(np.__version__))


class graph_generation:
    
    ''' height = rows in graph matrix
    width = columns in graph matrix
    '''
    
    def __init__(self,height=None,high=10,low=5):
        self.low=low
        self.high=high
        if height==None:
            self.height=np.random.randint(low=low,high=high)
        else: 
            self.height=height
  
    def graph_initializer(self,low=500,high=1000):
        
        size=np.random.randint(low=self.low,high=self.high)
        
        temp_x_and_y = np.random.randint(low=low,high=high, size=(size,2))
        
        # make it in a matrix form
        
        mat=np.zeros((temp_x_and_y.shape[0],temp_x_and_y.shape[0]))
        
        
        for i in range(temp_x_and_y.shape[0]):
            point=temp_x_and_y[i]
            for j in range(temp_x_and_y.shape[0]):
                if(i!=j):
                    temp=temp_x_and_y[j]
                    
                    mat[i][j]= (((point[0]-temp[0])**2)+((point[1]-temp[1])**2))**(1/2)
                
        
        return temp_x_and_y, mat
    
    
    
    def n_graph_initializer(self,n,low=2,high=1000):
     temp=[]
     P=[]
     
     for a in range(n):
         points,mat=self.graph_initializer(low=low,high=high)
         
         temp.append(mat)
         P.append(points)
         
     return temp, P
 

    '''Code for solving the grpahs'''
    
    def travellingSalesmanProblem(self,graph, s=0):
        V=graph.shape[0]

        '''Create a list of all vertex so that we can find all possible combinations'''
        vertex=[]
        for i in range(V):
            if i!=s:
                vertex.append(i)
                
        ''' Will store minimum weight Hamiltonian Cycle'''
        min_path = maxsize # use the maximum possible value
        next_permutation=permutations(vertex)
        dict={}
        #dict_2={}
        
        for path in next_permutation:
            
            ''' the value for each path will be stored in this variable 
            and then in dictionat above'''
            path=list(path)
            current_pathweight = 0
            path.insert(0,s)
            path.append(s)
            
            c=[]
            for j in range(len(path)):
                
                if j+1<len(path):
                    current_pathweight=current_pathweight+graph[path[j]][path[j+1]]
                    c.append(graph[path[j]][path[j+1]])
            #current_pathweight=current_pathweight+graph[path[-1]][s]
            
            dict[str(current_pathweight)]=path
            #dict_2[str(current_pathweight)]=c
            # update minimum
            min_path = min(min_path, current_pathweight)

        return dict[str(min_path)],min_path # returns solution , _
    
    def n_graph_solver(self,graphs):
        
        sol=[]
        for graph in graphs:
            s,_=self.travellingSalesmanProblem(graph)
            sol.append(s)
        return sol




 
