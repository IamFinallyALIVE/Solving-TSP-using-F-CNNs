#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 23:42:40 2021

@author: peeyushkumar
"""

import numpy as np
import cv2

if cv2.__version__ !='4.5.4-dev':
    print('Warning: The Module was created in Cv2 version {} but the available version on this system is {}'.format('4.5.4-dev',cv2.__version__))

class image_mapping:
    
    def __init__(self,height=224,width=224,special_factor=20,image_h=224,image_w=224):
        self.height=height
        self.width=width
        self.special_factor=special_factor
        self.image_h=image_h
        self.image_w=image_w
        
    def coordinate_mapper(self,x,y,x_max,y_max,x_min,y_min):
        
        lam_x=float((x_max-x_min)/self.width)
        lam_y=float((y_max-y_min)/self.height)

        if(lam_x)==0:
            lam_x=1
        if(lam_y==0):
            lam_y=1
        return abs(int((x-x_min)/lam_x)),abs(int((y-y_min)/lam_y))
    
    
    def find_min_and_max(self,mat,points): # find max (x,y) and min(x,y) in the given set of coordinates
        # find max and min dist node
        MAX=np.amax(points,axis=0)
        x_max=MAX[0]
        y_max=MAX[1]
        
        MIN=np.amin(points,axis=0)
        x_min=MIN[0]
        y_min=MIN[1]
        
        return  x_max+self.special_factor, y_max+self.special_factor, x_min-self.special_factor, y_min-self.special_factor

    
    def image_mapper(self,matrix,points,channel=3,factor_r=6,node_color=(0,0,0)):
        
        #img=np.ones(shape=(self.height,self.width,channel))*255
        img=np.ones(shape=(self.image_h,self.image_w,channel))*255
        x_max,y_max,x_min,y_min=self.find_min_and_max(matrix,points)
        w=matrix.shape[0]
         
        X=np.arange(1,w+1)  # w+1 because we dont wanna plot 0,0 coordinate on image
        Y=np.arange(1,w+1)

        for i in range(w):
            point=points[i]
            X[i],Y[i]=self.coordinate_mapper( point[0],point[1],x_max,y_max,x_min,y_min)
            #corner_from.append([abs(X[i]-factor_r),abs(Y[i]-factor_r)])
            #corner_to.append([X[i]+factor_r,Y[i]+factor_r])
        '''draw graphs edges'''
        for i in range(len(X)):
            x,y=X[i],Y[i]
            
            for j in range(len(X)):
                if i!=j:
       
                    img = cv2.line(img, (x,y), (X[j],Y[j]),(0,0,255), thickness=1)    
        '''draw graph nodes'''
        for x,y in zip( X,Y):
            img = cv2.circle(img, (x,y), 2, color=(0,0,0), thickness=3)
            
        
        return img
        
    def n_image_mapper(self,graphs,points,path=''):
        p=''
        if path == '':
            print('No path is given so the data will be stored in te default path i.e in directory where this module is present')
        else:
            p=path+'/'
        i=1
        
        for graph,point in zip(graphs,points):
            img=self.image_mapper(graph, point)
            cv2.imwrite(p+'graph_'+str(i)+'.jpg',img)
            i=i+1
            
    def label_image_mapper(self,matrix,points,solution,flag,factor_r=6,node_color=(1)):
        
        #img=np.ones(shape=(self.height,self.width,channel))*255
        ''' initialize an image map '''
        img=np.zeros(shape=(self.image_h,self.image_w,1)) 
        
        x_max,y_max,x_min,y_min=self.find_min_and_max(matrix,points)
        
        w=matrix.shape[0]
         
        X=np.arange(1,w+1)  # w+1 because we dont wanna plot 0,0 coordinate on image
        Y=np.arange(1,w+1)

        for i in range(w):
            point=points[i]
            X[i],Y[i]=self.coordinate_mapper( point[0],point[1],x_max,y_max,x_min,y_min)
            #corner_from.append([abs(X[i]-factor_r),abs(Y[i]-factor_r)])
            #corner_to.append([X[i]+factor_r,Y[i]+factor_r])
            
        if flag !=True:
            '''draw graphs edges of TSP '''
            for i in range(len(solution)):
                
                if i+1<len(solution):
                    '''First node'''
                    x,y=X[solution[i]],Y[solution[i]]
                    '''Second node'''
                    x_1,y_1=X[solution[i+1]],Y[solution[i+1]]
                    
                    img = cv2.line(img, (x,y), (x_1,y_1),(255,255,255), thickness=1)  
                
        '''Draw Nodes'''
        for i in range(len(solution)):
            x,y=X[solution[i]],Y[solution[i]]
            img = cv2.circle(img, (x,y), 2, color=(255,255,255), thickness=3)
        
        return img
    
    def n_label_image_mapper(self,graphs,points,solutions,flag=False,path=''):
        p=''
        if path == '':
            print('No path is given so the data will be stored in te default path i.e in directory where this module is present')
        else:
            p=path+'/'
        i=1
        
        for graph,point,solution in zip(graphs,points,solutions):
            img=self.label_image_mapper(graph,point,solution,flag=flag)
            cv2.imwrite(p+'graph_label_'+str(i)+'.jpg',img)
            i=i+1

        






