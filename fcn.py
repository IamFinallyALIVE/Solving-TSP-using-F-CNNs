# -*- coding: utf-8 -*-
"""
Author : Peeyush Kumar

"""

# Import Modules here----
from google.colab.patches import cv2_imshow
import tensorflow as tf
from tensorflow import keras
from keras.datasets import cifar10
from tensorflow.keras import models,layers,optimizers
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score
from keras.utils.np_utils import to_categorical
from keras.preprocessing.text import Tokenizer
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import time
import matplotlib.pyplot as plt
from sklearn.model_selection  import GridSearchCV, RandomizedSearchCV
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
from sklearn.metrics import accuracy_score
from sklearn.utils import shuffle
from keras.models import Input

from google.colab import drive
drive._mount('/content/drive')
import os
os.chdir("/content/drive/My Drive")


'''Load data'''
import pickle

with open("ML_Project/labels.pkl", 'rb') as f:
                    Y=pickle.load( f)

with open("ML_Project/training_examples.pkl", 'rb') as f:
                    X=pickle.load( f)    
                    
with open("ML_Project/labels_no_edges.pkl", 'rb') as f:
                    Y_2=pickle.load( f) 


'''Split Data'''
total_images=17000
x_train, x_test, y_train, y_test = train_test_split(X[:total_images], Y[:total_images], test_size=0.2, random_state=42)

print(X[:total_images].shape)
print('x_train.shape= {}'.format(x_train.shape))
print('y_train.shape= {}'.format(y_train.shape))
print('x_test.shape= {}'.format(x_test.shape))
print('y_test.shape= {}'.format(y_test.shape))


''' encode data'''

from tensorflow.keras.utils import  to_categorical

y_train_c = to_categorical(y_train)
y_test_c = to_categorical(y_test)

print('y_train_c.shape= {}'.format(y_train_c.shape))
print('y_test_c.shape= {}'.format(y_test_c.shape))

class my_model():
  def __init__(self):
    print('Model Initializing...')
    

  def FCN_encoder(self,x):

      x=layers.Conv2D(64, (3, 3), padding="same", activation="relu")(x) 
      x=layers.Conv2D(64, (3, 3), padding="same", activation="relu")(x)
      p1=layers.MaxPooling2D(pool_size=(2, 2),strides=(2,2))(x)

      x=layers.Conv2D(128, (3, 3), padding="same", activation="relu")(p1)
      x=layers.Conv2D(128, (3, 3), padding="same", activation="relu")(x)
      p2=layers.MaxPooling2D(pool_size=(2, 2),strides=(2,2))(x)

      x=layers.Conv2D(256, (3, 3), padding="same", activation="relu")(p2)
      x=layers.Conv2D(256, (3, 3), padding="same", activation="relu")(x)
      x=layers.Conv2D(256, (3, 3), padding="same", activation="relu")(x)
      p3=layers.MaxPooling2D(pool_size=(2, 2),strides=(2,2))(x)

      x=layers.Conv2D(512, (3, 3), padding="same", activation="relu")(p3)
      x=layers.Conv2D(512, (3, 3), padding="same", activation="relu")(x)
      x=layers.Conv2D(512, (3, 3), padding="same", activation="relu")(x)
      p4=layers.MaxPooling2D(pool_size=(2, 2),strides=(2,2))(x)


      x=layers.Conv2D(1024, (3, 3), padding="same", activation="relu")(p4)
      x=layers.Conv2D(1024, (3, 3), padding="same", activation="relu")(x)
      x=layers.Conv2D(1024, (3, 3), padding="same", activation="relu")(x)
      p5=layers.MaxPooling2D(pool_size=(2, 2),strides=(2,2))(x)

      return p1,p2,p3,p4,p5

  def FCN(self,x,n_classes):
    op=layers.Conv2D(n_classes,(1,1),strides=1,activation="relu",kernel_initializer=tf.keras.initializers.TruncatedNormal(stddev=0.01),
                                kernel_regularizer = tf.keras.regularizers.L2(1e-3))(x)
    return op

  def FCN_decoder(self,p1,p2,p3,p4,p5,n_classes=2):

    encoder_out= self.FCN(p5,n_classes)
    # num_classes. num_classes should be 2 for this project -- a



   

    # Transposed/backward convolutions for creating a decoder
    deconv_1 = layers.Conv2DTranspose( n_classes, 4, 2, 'SAME',
                                          kernel_initializer=keras.initializers.TruncatedNormal(stddev=0.01)
                                ,kernel_regularizer = keras.regularizers.l2(1e-3))(encoder_out)
    
    # Add a skip connection to previous VGG layer

    skip_1= self.FCN(p4,n_classes)
    add1=layers.Add()([deconv_1,skip_1])

    # Up-sampling
    deconv_2 = layers.Conv2DTranspose( n_classes, 4, 2, 'SAME',
                                          kernel_initializer=keras.initializers.TruncatedNormal(stddev=0.01),
                                kernel_regularizer = keras.regularizers.L2(1e-3))(add1)

    skip_2 = self.FCN(p3,n_classes)
    add2=layers.Add()([deconv_2,skip_2])


    deconv_3 = layers.Conv2DTranspose(n_classes, 16, 8, 'SAME',
                                          kernel_initializer=keras.initializers.TruncatedNormal(stddev=0.01),
                                kernel_regularizer = keras.regularizers.L2(1e-3))(add2 )
    
    return deconv_3

  def make_model(self,input_shape=(224,224,3)):

      input=Input(shape=input_shape)
      p1,p2,p3,p4,p5=self.FCN_encoder(input) # encoder
      output=self.FCN_decoder(p1,p2,p3,p4,p5)
      final_output=layers.Activation('softmax')(output)

      model=models.Model(input,final_output)
    
      model.compile(optimizer=tf.keras.optimizers.Adam( learning_rate=0.001) ,
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
      return model


class TrainingCallback(keras.callbacks.Callback):
    def on_train_begin(self, logs=None):
        pass
        
    def on_epoch_begin(self, epoch, logs=None):
        print(f"Starting epoch {epoch}")
    def on_train_batch_begin(self, batch, logs=None):
        pass
        
    def on_train_batch_end(self, batch, logs=None):
        pass
        
    def display(self,img):
          plt.imshow(np.round(np.argmax(img, axis=2, out=None)))

    def on_epoch_end(self, epoch, logs=None):
        if (epoch%10==0):
          print(f"Finished epoch {epoch}, loss is {logs['loss']}, accuracy is {logs['accuracy']}")
          im=model.predict(x_train[:16])
          dic.append(im[0])
          cv2_imshow((np.round(np.argmax(im[15], axis=2, out=None)))*255.)
          #cv2_imshow((np.round(im[0])*255))
          # save model weights
          
          print('Saving model...')
          filename='Model_'+str(epoch)+'.h5' 
          model.save(filename)

    def on_train_end(self, logs=None):
        print("Finished training")




m=my_model()
model=m.make_model(input_shape=(224,224,3))
model.summary()


def alpha_changer(epoch,lr,val_loss=None):
  if (epoch==20):
    return lr/10.0
  else :
    return lr

lr_callback=callback=keras.callbacks.LearningRateScheduler(alpha_changer)



history_2=model.fit(x_train, y_train_c,batch_size=100,epochs=6000,callbacks=[TrainingCallback()]) 

model.evaluate(x_test, y_test_c)
preds=model.predict(x_test)
