# from collections import defaultdict
# from os.path import isfile
# from scipy.io import savemat
# from scipy.stats import spearmanr
# from scipy.linalg import orth
# from mpl_toolkits.mplot3d import Axes3D
from numpy.linalg import norm
# from math import sqrt
# from multiprocessing import cpu_count
# import multiprocessing
try:
   import cPickle as pickle
except:
   import pickle
# import threading
# import random
# import queue
# import scipy 
import numpy as np
# import sys
import array
import numpy.random as rn
# import itertools
# import os
# import logging
# import time
# import struct
FUNCWORD = 'funcWords.txt'

class Vocab:

    def __init__(self, vecDim, directory, vocabInputFile, vectorInputFile, isFunctional):

        self.vecDim = vecDim
        self.vocabFile = directory + vocabInputFile
        self.vecFile = directory + vectorInputFile

        self.readVocabFromFile()
        self.readVectorFromFile()
        self.readFuncWords(isFunctional)

                #self.sem = multiprocessing.BoundedSemaphore(3)


    def readVocabFromFile(self):
        # đọc file vocabulary dic và và lưu word vào vocablist, index tức là stt, count tức tần số

        vocabList = list()
        vocabIndex = dict()
        vocabCount = list()

        vocabList = open(self.vocabFile, "r", encoding='utf8').read().split('\n')[:-1]

        # f = open(self.vocabFile, "r", encoding='utf8')
        # idx = 0
        # for line in f.readlines():
        #     # try:
        #   raw = line
        #   vocabList.append(raw)
        #   # vocabCount.append(int(raw[1]))
        #   vocabIndex[raw] = idx 
        #   idx += 1
        #     # except :
        #     #     print("Lỗi >> ",line)
            
        #     #if idx == 200000:
        #     #	break

        self.vocabList = vocabList
        self.vocabIndex = vocabIndex
        self.vocabSize = len(self.vocabList)
        # self.vocabCount = vocabCount

        print ("Done loading vocabulary.")

    def readVectorFromFile(self):

        vecDim = self.vecDim
        # vecMatrix = array.array('f')
        # vecMatrix.fromfile(open(self.vecFile, 'rb'), self.vocabSize * vecDim)
        # vecMatrix = np.reshape(vecMatrix, (self.vocabSize, vecDim))[:, 0:vecDim]
        vecMatrix = np.load(self.vecFile)

        #vecMatrixNorm = normalizeMatrix(vecMatrix)
        #self.vecMatrixNorm = vecMatrixNorm
        self.vecMatrix = vecMatrix

        #print vecMatrix[:2]
        print("Done loading vectors.")

    def readFuncWords(self, isFunctional):
        funcWords = set()
        if isFunctional:
            f = open(FUNCWORD, 'r')
            for line in f.readlines():
                funcWords.add(line.rstrip())

        self.funcWords = funcWords

    def getWordIdList(self, word_list):
        # loại bỏ các từ function word, trả về word và id của word list
        """
        return a list of indices of word_list
        """
        selected_word_list = []
        wordId = []
        for word in word_list:
            if (word in self.funcWords):
                continue
            try:
                wordId.append(self.vocabList.index(word))
                selected_word_list.append(word)
            except:
                pass
        return selected_word_list, wordId
                                        

    def getContextIdList(self, contexts):
        contextList = []
        for context in contexts:
                    contextId = []
                    context = context.lower().rstrip().split()
                    for word in context:
                        if word in self.funcWords:
                            continue
                        try:
                            contextId.append(self.vocabList.index(word))
                        except:
                            pass
                    contextList.append(contextId[:])
        #print "contextList:", contextList[0]
        return contextList

                                        
    def getVecFromId(self, contextIdx):
        contextVecs = list()
        for idx in contextIdx:
            if (idx == []):
                vecs = np.array( [ [0]*self.vecDim ] )
            else:
                vecs = self.vecMatrix[np.array(idx)]
            contextVecs.append(vecs)
        return contextVecs		

    def getVectors(self, word_list):
        #vecDim = self.vecDim
        # loại bỏ function word và trả về từ + id của chúng 
        selected_word_list, idxList = self.getWordIdList(word_list)

        #print "debugging", "idxList:", idxList
        vecList = []
        for i in range(len(idxList)):
            # chạy so sanh từng word trong word list
            idx = idxList[i]
            if (idx == []):
                # hầu như không xảy ra
                vecs = np.array([[0]*self.vecDim])
                print ("no embedding for word",word_list)
            else:
                vecs = self.vecMatrix[np.array(idx)]
                
            vecList.append(vecs)
            # lấy ra vector của từng word

        #print "debugging", "vecList:", vecList
        # trả về list word sau khi đã loại func word  và list vector của các từ đó
        return selected_word_list, vecList
                                    
                        
