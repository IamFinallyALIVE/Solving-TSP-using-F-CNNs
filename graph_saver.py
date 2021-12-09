#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 14:29:24 2021

@author: peeyushkumar
"""

import graph_generator

# create graphs


'''This module saves the graphs in a txt file in the form of lists'''

class graphs_saver:
    def __init__(self,n_graphs):
        self.n_graphs=n_graphs

        self.graphs,_=graph_generator.graph_generation().n_graph_initializer(n_graphs)
        
    def save_as_list(self,file_name,directory=''):
        # name of file 
        if directory != '':
            path=directory+'/'+file_name
        else:
            path=file_name 
        # writing to txt file     
        with open(path, 'w') as f:
            for arr in self.graphs:
                for i in range(arr.shape[0]):
                    for j in range(arr.shape[1]):
                        if i !=j:
                            f.write('{},{},{}'.format(i,j,arr[i][j]))
                            f.write('\n')
                f.write('\n')
                
                

graphs_saver(2).save_as_list('tester.txt')