import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.svm import SVR
import math
CONST_RET_START = 28
CONST_RET_END = 207


df = pd.read_csv('train.csv', sep=',')
test = pd.read_csv('test.csv', sep = ',')
l = len(df.index)
def my_kernel(X, Y):
	return (1+ X*Y)**2

X = [[float(i+1)] for i in range(CONST_RET_END-CONST_RET_START)]
Z = [[float(i+1)] for i in range(180, 180+119)]
Z= [[i+1] for i in range(CONST_RET_END-CONST_RET_START)]
dfs = df.iterrows()
for index, row in dfs :
	#print index
	if(index == 3): 
		Y = []
		aux = 0
		for i in range(CONST_RET_START, CONST_RET_END):
			aux += 1
			if(math.isnan(row[i])):
				firstnotnull = i-1
				while(math.isnan(row[firstnotnull])):
					firstnotnull = firstnotnull-1
				Y.append(row[firstnotnull]*100000)
			else:	
				Y.append(row[i]*100000)

		###############################################################################
		# Add noise to targets

		svr_rbf = SVR(kernel='rbf', C=10, gamma=0.001)
		svr_lin = SVR(kernel='linear', C=10)
		#svr_poly = SVR(kernel='poly', C=1, degree=3)

		y_rbf = svr_rbf.fit(X, Y).predict(Z)
		y_lin = svr_lin.fit(X, Y).predict(X)
		#y_poly = svr_poly.fit(X, Y).predict(X)
		print(y_rbf)

		plt.scatter(X,Y, c='g', label='data')
		plt.hold('on')
		plt.plot(X, y_rbf, c='g', label='RBF model')
		plt.plot(X,y_lin, c='k', label='Linear model')
		#plt.plot(X, y_poly, c='k', label='Polynomial model')
		plt.xlabel('data')
		plt.ylabel('target')
		plt.title('Support Vector Regression')
		plt.legend()
		plt.show()






