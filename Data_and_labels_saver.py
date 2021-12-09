#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 18:57:41 2021

@author: peeyushkumar
"""




from graph_generator import graph_generation
from Image_mapping import image_mapping



'''This module will generate and save the graph images and labels in the memory'''


if __name__ == "__main__":
    
    n=20000
    
    print('Generating {} graphs and respective labels'.format(n))

    img_converter=image_mapping()
    
    grp= graph_generation()
    
    graphs,points=grp.n_graph_initializer(n)
    
    solutions=grp.n_graph_solver(graphs)
    
    '''path to save examples'''
    path_1='/Users/peeyushkumar/Desktop/ML Project/Data/examples'

    img_converter.n_image_mapper(graphs,points,path=path_1)
    
    
    '''path to save labels for the examples'''
    path_2='/Users/peeyushkumar/Desktop/ML Project/Data/labels'
    img_converter.n_label_image_mapper(graphs,points, solutions,path=path_2)
    path_3='/Users/peeyushkumar/Desktop/ML Project/Data/labels_only_nodes'
    
    img_converter.n_label_image_mapper(graphs,points, solutions,flag=True,path=path_3)
    