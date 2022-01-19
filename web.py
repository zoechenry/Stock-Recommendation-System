# -*- coding: utf-8 -*-
from flask import Flask, url_for, redirect, render_template, request, Response, stream_with_context
import json###################这里改了
import os
import time
import stockpredict
from gevent import pywsgi
from flask_cors import *

import sys
import lsqlite3

# reload(sys)
# sys.setdefaultencoding('utf8')

app = Flask(__name__)
CORS(app,supports_credentials=True)#跨域设置

#url_for('函数名称')
@app.route("/")############################################这里改了，重要！！！！
def index():
    return render_template('index.html')#已经默认在templates文件夹下

@app.route("/index")
def index_1():
    return render_template('index.html')

@app.route("/predict",methods=['POST'])
def predict():
	data = request.get_data().decode('utf-8')
	data = json.loads(data)
	return stockpredict.predict(data['code'],"")

@app.route("/download",methods=['GET'])
def download():
	# 服务器上文件的位置
	vf = 'data.csv'
	# 高级特性 生成器
	def generate(video_file):
		f = open(video_file, 'rb')
		while True:
			chunk = f.read(512*1024)
			if not chunk:
				break
			yield chunk
	return Response(
		stream_with_context(generate(vf)),
		# 控制浏览器怎么识别下载的东西
		mimetype='text/comma-separated-values', # 让浏览器用mp4播放
		# mimetype='application/octet-stream', # 让浏览器直接下载
		headers={"Content-Length": os.path.getsize(vf)})

# get请求
@app.route("/getSome",methods=['GET'])
def getSome():
    return "successCallback"+"("+stockpredict.predict(request.args.get('a','erro'),request.args.get('b','erro'))+")"
databaseUse='sqlite3'
# 上传数据
@app.route("/savedata",methods=['POST'])
def savedata():
	data = request.get_data().decode('utf-8')
	data = json.loads(data)
	data['creatTime']=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))

	if databaseUse=='sqlite3':
		lsqlite3.useSqliteInsert(data)
		return json.dumps({"msg":"保存成功"})
	return json.dumps({"msg":"保存成功"})

# 获取每一行数据
@app.route("/getdata",methods=['GET'])
def getdata():
	table = request.args.get('table','erro')
	database = request.args.get('database','erro')
	if databaseUse=='sqlite3':
		try:
			return json.dumps({"msg":"获取成功","data":lsqlite3.useSqliteSelect(database,table)})
			pass
		except Exception as e:
			return json.dumps({"msg":"获取成功","data":[]})
	return json.dumps({"msg":"获取成功","data":[]})

@app.route('/regist_user')
def regist_user():
	return render_template('regist_user.html')

@app.route('/more')
def more():
	return render_template('more.html')

@app.route('/list')
def list():
	return render_template('list.html')

@app.route('/main_part')
def main_part():
	return render_template('main_part.html')

@app.route('/entry')
def entry():
	return render_template('entry.html')

@app.route('/user_management')
def user_management():
	return render_template('user_management.html')

if __name__ == '__main__':
    #app.run(host='127.0.0.1', port=9997)###################这里改了，可以不改
	server = pywsgi.WSGIServer(('127.0.0.1',9997),app)###################这里改了
	print('服务器开始运行')
	server.serve_forever()###################这里改了
