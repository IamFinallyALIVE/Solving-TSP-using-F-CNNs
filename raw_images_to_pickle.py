#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 23:55:06 2021

@author: peeyushkumar
"""



''' This module loads the images generated to a an array and then dumps them in a  PICKLE file '''


import pickle
import numpy as np


import cv2





def load_and_save_training_eg(path,n=20000):
    
    data=[]
    for i in range(1,n+1):
        
        img=cv2.imread(path+str(i)+'.jpg') 
        data.append(img)
    data=np.array(data)
    
    with open("training_examples.pkl", 'wb') as f:
                    pickle.dump(data, f)


def load_and_save_labels(path,n=20000):
    
    data=[]
    for i in range(1,n+1):
        
        img=cv2.imread(path+str(i)+'.jpg',0) 
        _,thres = cv2.threshold(img,245,255,cv2.THRESH_BINARY)
        thres=thres/255.
        data.append(thres)
    
    data=np.array(data)
    data=data.astype('uint8')
    with open("labels.pkl", 'wb') as f:
                    pickle.dump(data, f)
                    
def load_and_save_labels_with_nodes(path,n=20000):
    
    data=[]
    for i in range(1,n+1):
        
        img=cv2.imread(path+str(i)+'.jpg',0) 
        _,thres = cv2.threshold(img,245,255,cv2.THRESH_BINARY)
        thres=thres/255.
        data.append(thres)
    
    data=np.array(data)
    data=data.astype('uint8')
    with open("labels_no_edges.pkl", 'wb') as f:
                    pickle.dump(data, f)
    
    
    
    
''' Set directories accordingly'''
    
if __name__ == "__main__":
    
    
    
    '''path to save examples'''
    path_1='/Users/peeyushkumar/Desktop/ML Project/Data/examples/graph_'
    
    
    '''path to save labels for the examples'''
    path_2='/Users/peeyushkumar/Desktop/ML Project/Data/labels/graph_label_'
    
    
    #load_and_save_training_eg(path_1)
    load_and_save_labels(path_2)   
    
    
    path_3='/Users/peeyushkumar/Desktop/ML Project/Data/labels_only_nodes/graph_label_'

    load_and_save_labels_with_nodes(path_3)
    
   
                    

