#!/usr/bin/python

import pandas as pd
import math
import operator
import collections
import matplotlib.pyplot as plt
import numpy as np
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise

CONST_RET_START = 28
CONST_RET_END = 207
CONST_WINDOW_SIZE = 3 # min=3, max=181
CONST_ROW_TERM = 0 # number of rows to extract features, all = 0

class KalmanFilter1D:
    def __init__(self, x0, P, R, Q):
        self.x = x0
        self.P = P
        self.R = R
        self.Q = Q

    def update(self, z):

        self.x = (self.P*z + self.x*self.R) / (self.P + self.R)
        if(self.R == 0):
        	self.P = 1. / (1./self.P )
        else:
        	self.P = 1. / (1./self.P + 1./self.R)

    def predict(self, u=0.0):
        self.x += u
        self.P += self.Q

df = pd.read_csv('train.csv', sep=',')
test = pd.read_csv('test.csv', sep = ',')
l = len(df.index)






for index, row in df.iterrows():
	#print index
	if(index == 0):
		x = []
		for i in range(CONST_RET_START, CONST_RET_END):
			if(math.isnan(row[i])):
				firstnotnull = i-1
				while(math.isnan(row[firstnotnull])):
					firstnotnull = firstnotnull-1
				x.append(row[firstnotnull])
			else:	
				x.append(row[i])

		N = len(x)

		ps = []
		estimates = []

		kf = KalmanFilter1D(x0=0,            # initial state
		                    P=x[0],           # initial variance 
		                    R=1, # sensor noise
		                    Q=1) # error in prediction


		i = 1
		while( i < N):
		    kf.predict(0)
		    kf.update(x[i])

		    # save for latter plotting
		    estimates.append(kf.x)
		    ps.append(kf.P)

		    i += 1

		plt.plot(x)
		plt.plot(estimates)
		plt.show()
		
		x2 = []
		
		for index, row in test.iterrows():
			#print index
			if(index == 0):

				for i in range(28,146):
					if(math.isnan(row[i])):
						firstnotnull = i-1
						while(math.isnan(row[firstnotnull])):
							firstnotnull = firstnotnull-1
						x2.append(row[firstnotnull])
					else:	
						x2.append(row[i])
			break

		i = 0
		estimates = []
		while( i < len(x2)):
		    kf.predict(0)
		    # save for latter plotting
		    estimates.append(kf.x)
		    ps.append(kf.P)

		    i += 1


		plt.plot(x2)
		estimates.insert(0,0);
		plt.plot(estimates)
		plt.show()

	break;


