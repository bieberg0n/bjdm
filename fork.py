import requests
import multiprocessing
import multiprocessing.managers
import time
import os
import sys
import glob
import shutil
import queue
import subprocess
#from socket import *

#def room(i,n):
#	f = open('.tmp/'+fname+'.'+str(n)+'.bj','wb')
#	f.seek(i-1)
#	f.write(b'\x00')
#	f.close()

def write(t,ra):
	s = requests.session()
	s.headers['Range'] = 'bytes='+ra
	r = s.get(url,stream=True,headers=s.headers)
	t = str(t) if t >= 10 else '0'+str(t)
	with open('.tmp/'+fname+'.'+t+'.bj','wb') as f:
		for i in r.iter_content(chunk_size=1024*128):
			f.write(i)
			f.flush()

print('母舰:STEINS GATE 动力引擎初始化...')
#url,文件名,线程数
s = requests.session()
#url = 'http://img4.duitang.com/uploads/item/201302/11/20130211102522_nAVxM.jpeg'
#url = 'http://softfile.3g.qq.com/msoft/179/1105/71666/qq2012_beta1_build0016_unsigned.rar'
url = 'http://softfile.3g.qq.com/msoft/179/1105/90992/qq_2013_0_0_1718_s60v3_signed.sisx'
#url = 'http://down.myapp.com/myapp/qqteam/Androidlite/qqlite_3.2.0.361.apk'
#url = 'http://cdn.ovear.info:8999/upload/5c8173cd-ac7f-4405-8a1c-4b886db85412.jpg'
#url = 'http://cdn.ovear.info:8999/upload/71d9078c-4f0f-4ef1-ab31-fa9f3549f163.jpg'
#url = 'http://cdn.ovear.info:8999/upload/cbdadd83-9772-40d5-8100-7ccfa351d2ee.jpg'
#url = 'http://dldir1.qq.com/qqfile/QQIntl/QQi_wireless/Android/qqi_4.6.13.6034_office.apk'
#url = sys.argv[1]
fname = url.split('/')[-1]
t = 2

r = s.get(url,stream=True)
#文件长度
le = int(r.headers['Content-Length'])
#分块
l = [le//t+1 if i < le%t else le//t for i in range(t)]
print('敌军高达数目:{} 分割:{}'.format(le,l))
l1 = []
b = -1
for i in range(len(l)):
	a = b + 1
	b = a + l[i] - 1
	l1.append('{}-{}'.format(a,b))
#print(l1)
#创建临时文件夹
if not os.path.exists('.tmp'):
	os.mkdir('.tmp')
else:
	for i in glob.glob('.tmp/*.bj'):
		os.remove(i)

#进程池
ps = []
#计时器
nt = int(time.time())

#socket通信
#send = socket(AF_INET,SOCK_STREAM)
#recv = socket(AF_INET,SOCK_STREAM)
#recv.bind(('0.0.0.0',8000))
#recv.listen(True)
#send.connect(('192.168.233.17',8001))
#send.send('Start'.encode())
#conn,addr = recv.accept()

#queue通信
q = queue.Queue()
q1 = queue.Queue()
b = multiprocessing.managers.BaseManager
b.register('q',callable=lambda:q)
b.register('q1',callable=lambda:q1)
manager = b(address=('',5000),authkey='abc'.encode('utf-8'))
manager.start()
manager.q().put([url,fname])

#t1 = [[],[]]
size = 0
print('母舰:STEINS GATE进入战斗战斗状态')
for i in range(t):
	print(i,l1[i])
	#room(l[i],i)
	if i+1 <= t//2:
		size += l[i]
		p = multiprocessing.Process(target=write,args=(i,l1[i]))
		p.start()
		ps.append(p)
	else:
		manager.q().put([i,l1[i]])
		#t1[0].append(i)
		#t1[1].append(l[i])

print('释放高达')
manager.q().put(None)

print('作战开始')
while True:
	size1 = 0
	for i in glob.glob('.tmp/*.bj'):
		size1 += os.path.getsize(i)
	col = int(subprocess.getoutput('stty size').split(' ')[1])
	#print(col)
	col1 = col-8
	p = int(size1/size*col1)
	if size1 != size:
		print('['+'='*p+'>'+' '*(col1-p-1),end='')
		print(']{0:>4.1f}% '.format(size1/size*100),end='\r')
	else:
		#print('['+'='*p+' '*(col1-p),end='')
		print('['+'='*(col1-1)+'>',end='')
		print(']100.0%')
		break
	#print()
	time.sleep(1)
	
for i in ps:
	i.join()

while True:
	if not manager.q1().get():
		break

#print(t1)
print('战斗完毕。花费时间:'+str(int(time.time())-nt))
print('回收高达...')
os.system('scp -r pi@192.168.233.17:/home/pi/py/pymultidm/.tmp/ ./')
#for i in range(len(t1[0])):
#	print(i)
#exit()
#for i in range(len(t1[0])):
#	print(i)
#	size = 0
#	f = open('.tmp/'+fname+'.'+str(t1[0][i])+'.bj','wb')
#	while True:
#		if size+8 >= t1[1][i]:
#			print(size)
#			print(t1[1][i]-size)
#			filedata = conn.recv(t1[1][i]-size)
#			f.write(filedata)
#			break
#		size += 8
#		#print(size)
#		filedata = conn.recv(8)
#		f.write(filedata)
#	f.close()
os.system('cat .tmp/*.bj > '+fname)
shutil.rmtree('.tmp')
