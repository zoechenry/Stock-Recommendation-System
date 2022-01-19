# -*- coding: utf-8 -*-
import pandas as pd
import tushare as ts
import sklearn as skl
import numpy as np
from sklearn import datasets,linear_model
from sklearn.model_selection import train_test_split,cross_val_score
import time
import datetime
import json
import sys
import csv
import xgboost as xgb

from numpy import *

def predict(acode,aname):

	timestring = time.strftime('%Y.%m.%d',time.localtime(time.time()))
	timearr = timestring.split('.')
	times = timearr[0]+'-'+timearr[1]+'-'+timearr[2]

	#################准备股票数据。#################
	date_end_str = times
	code = str(acode)

	date_end = datetime.datetime.strptime(date_end_str, "%Y-%m-%d")
	date_start = (date_end + datetime.timedelta(days=-300)).strftime("%Y-%m-%d")
	date_end = date_end.strftime("%Y-%m-%d")
	# open high close low volume price_change p_change ma5 ma10 ma20 v_ma5 v_ma10 v_ma20 turnover
	stock_X = ts.get_hist_data(code,start=date_start,end=date_end)
	if not stock_X is None:
		stock_X.to_csv('data.csv')
		column=[]
		with open('data.csv','rt', encoding="utf-8") as csvfile:
			reader = csv.reader(csvfile)
			column = [row[3] for row in reader]
			column.remove('close')
			# print(column)

		stock_X = stock_X.sort_index()  # 将数据按照日期排序下。###############这里改了，可以不改
		stock_y = pd.Series(stock_X["close"].values) #标签

		stock_X_test = stock_X.iloc[len(stock_X)-1]
		# 使用今天的交易价格，13 个指标预测明天的价格。偏移股票数据，今天的数据，目标是明天的价格。
		stock_X = stock_X.drop(stock_X.index[len(stock_X)-1]) # 删除最后一条数据
		stock_y = stock_y.drop(stock_y.index[0]) # 删除第一条数据
		#删除掉close 也就是收盘价格。
		del stock_X["close"]
		del stock_X_test["close"]

		#使用最后一个数据做测试。
		stock_y_test = stock_y.iloc[len(stock_y)-1]

		model= xgb.XGBRegressor()
		#model = linear_model.LinearRegression()
		model.fit(stock_X.values,stock_y)
		# print("############## test & target #############")
		# print(model.predict([stock_X_test.values]))
		# print(stock_y_test)
		column2=[]
		for x in column:
			column2.append(float(x)) 

			pass
		narray=np.array(column2)
		sum1=narray.sum()
		mean=sum1/len(column2)
		diff_square=(narray-mean)*(narray-mean)
		var=diff_square.sum()/len(column2)
		v1,v2,v3,v4,v5=float(model.predict([stock_X_test.values])[0]),float(stock_y_test),acode,aname,float(var)
		#原数据为numpy数据类型，JSON5库不支持

		# print("############## coef_ & intercept_ #############")
		# print(model.coef_) #系数
		# print(model.intercept_) #截距
		# print("score:", model.score(stock_X.values,stock_y)) #评分

		return json.dumps({"price":v1,"oldPrice":v2,"code":v3,"name":v4,"volatility":v5})


if __name__ == '__main__':
	predict(603369,'')###############这里改了，可以不改
	pass
