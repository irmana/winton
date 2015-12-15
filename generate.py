#!/usr/bin/python

import pandas as pd
import math
import operator
import collections

CONST_RET_START = 0
CONST_RET_END = 181
CONST_WINDOW_SIZE = 3 # min=3, max=181
CONST_ROW_TERM = 0 # number of rows to extract features, all = 0

def ret_not_nan(r, s, e): #row with returns, start id, end id
	for i in range(s, e):
        	if (math.isnan(r['Ret_%s'%(i,)])):
			return False
	return True

def get_keys(r):
	keys = []
	for key in r.keys():
        	keys.append(key)
	return keys

def get_values(r):
        for key, value in r.items():
                r[key] = [value]
        return r

def get_header(r):
        for key, value in r.items():
                r[key] = [key]
        return r

def get_features(r, i1, i2):
	f = {}
	s = 0
	p = None
	for i in range(i1, i2):
		ret = r['Ret_%s'%(i,)]
		s += ret
		#minimum
		if f.get("Min",9999) == 9999 or f.get("Min",0)>ret:
			f['Min'] = ret
		#maximum
		if f.get("Max",-9999) == -9999 or f.get("Max",0)<ret:
                        f['Max'] = ret

		#difference for i1 to 12
		if p is None:
			p = ret
		else:
			f['Diff_%s_%s'%(int(math.fabs(i-i2+1)),int(math.fabs(i-i2)),)] = ret - p

		#past n returns, n = CONST_WINDOW_SIZE-1
		f['Ret_%s'%(int(math.fabs(i-i2+1)),)] = ret
	
	#difference between target ret value and last input ret value
	f['Diff_%s_%s'%(int(i2-i1-1),int(i2-i1),)] = r['Ret_%s'%(i2,)] - r['Ret_%s'%(i2-1,)]

	#average value of past n returns	
	f['Avg'] = s/(i2-i1)

	var = 0
	for i in range(i1, i2):
                ret = r['Ret_%s'%(i,)]
		var += math.pow(f['Avg']-ret, 2)
	#standard deviation
	f['Std'] = math.sqrt(var/(i2-i1))
	#sum
	f['Sum'] = s
	
	#target value
	f['Target'] = r['Ret_%s'%(i2,)]

	return collections.OrderedDict(sorted(f.items()))

df = pd.read_csv('train.csv', sep=',')
l = len(df.index)
for index, row in df.iterrows():
	if (index%100 == 0):
		print "%s/%s"%(index,l,)

	#print index
	row['Ret_0'] = row['Ret_MinusTwo']
	row['Ret_1'] = row['Ret_MinusOne']

	for i in range(CONST_RET_START, CONST_RET_END-(CONST_WINDOW_SIZE-1)):
		ret = row['Ret_%s'%(i,)]
		
		if math.isnan(ret):
			continue

		ret_start = i
		ret_end = i+CONST_WINDOW_SIZE
		
		if ret_not_nan(row, ret_start, ret_end):
			ret_f_end = ret_end-1
			f = get_features(row, ret_start, ret_f_end)
			if (i==0):
				with open('output/output_%s_%s.csv'%(CONST_WINDOW_SIZE,index,), 'w') as o:
					pd.DataFrame(get_values(f)).to_csv(o, columns=get_keys(f), header=True, index=False)
			else:
				with open('output/output_%s_%s.csv'%(CONST_WINDOW_SIZE,index,), 'a') as o:
    					pd.DataFrame(get_values(f)).to_csv(o, columns=get_keys(f), header=False, index=False)
		
	if (index!=0 and index==CONST_ROW_TERM-1):
		break




