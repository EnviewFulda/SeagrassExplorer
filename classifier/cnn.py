#!/usr/bin/env python

import cv2
import numpy as np
import tensorflow as tf


SINGLE = 0
MULTIPLE = 1

cnn_instance = None

class CnnFeat(object):
    def __init__(self):
        self.sess = tf.Session()
    
    
    def features(self, X, mode):
        next_to_last_tensor = self.sess.graph.get_tensor_by_name('pool_3:0') # get the features from the pool_3:0 layer

        if (mode == MULTIPLE): # many features
            listFeatures = []
            len_x = len(X)
            for i, Patch in enumerate(X):
                feat = self.sess.run(next_to_last_tensor,{'DecodeJpeg:0': Patch})
                feat = np.squeeze(np.array(feat)) # convert to array, one dimension too much, remove it
                listFeatures.append(feat)
                if i % 500 == 0:
                    print('CNN features progress: {}%'.format(float(i/len_x)*100))
            return listFeatures

        if (mode == SINGLE): # single feature
            feat = self.sess.run(next_to_last_tensor,{'DecodeJpeg:0': X})
            feat = np.squeeze(np.array(feat)) # convert to array, one dimension too much, remove it
            return feat
    
    def close(self):
        self.sess.close()

def close ():
    cnn_instance.close()
    
def ini (folder):
    '''initialization

    Args:


    Returns:

    '''
    with tf.gfile.GFile(folder, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')
    global cnn_instance
    cnn_instance = CnnFeat()

def features(X, mode):
    '''extract features

    Args:
        X (list):  Patch or Patches
        mode: SINGLE, MULTIPLE

    Returns:
        features (list)
    '''
    config = tf.ConfigProto()
    with tf.Session(config=config) as sess:
        next_to_last_tensor = sess.graph.get_tensor_by_name('pool_3:0') # get the features from the pool_3:0 layer

        if (mode == MULTIPLE): # many features
            listFeatures = []
            len_x = len(X)
            for i, Patch in enumerate(X):
                feat = sess.run(next_to_last_tensor,{'DecodeJpeg:0': Patch})
                feat = np.squeeze(np.array(feat)) # convert to array, one dimension too much, remove it
                listFeatures.append(feat)
                if i % 500 == 0:
                    print('CNN features progress: {}%'.format(float(i/len_x)*100))
            return listFeatures

        if (mode == SINGLE): # single feature
            feat = sess.run(next_to_last_tensor,{'DecodeJpeg:0': X})
            feat = np.squeeze(np.array(feat)) # convert to array, one dimension too much, remove it
            return feat


def featurelist(path_train_set):
    '''load training patches and extract features

    Args:
        path_train_set (list): path to training patches


    Returns:
        features (list)

    '''
    listFeatures = []

    for index, Path in enumerate(path_train_set):
        loaded_patch = cv2.imread(Path)
        listFeatures.append(features(loaded_patch, SINGLE))

    return listFeatures
