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

def write(url,fname,t,ra):
	s = requests.session()
	s.headers['Range'] = 'bytes='+ra
	r = s.get(url,stream=True,headers=s.headers)
	t = str(t) if t >= 10 else '0'+str(t)
	with open('.tmp/'+fname+'.'+t+'.bj','wb') as f:
		for i in r.iter_content(chunk_size=1024*128):
			f.write(i)
			f.flush()

def main(url,t=2):
	print('母舰:STEINS GATE 动力引擎初始化...')
	#url = []
	#url,文件名,线程数
	s = requests.session()
	#url.append('http://img4.duitang.com/uploads/item/201302/11/20130211102522_nAVxM.jpeg')
	#url.append('http://softfile.3g.qq.com/msoft/179/1105/71666/qq2012_beta1_build0016_unsigned.rar')
	#url = ['http://cdn.ovear.info:8999/upload/71d9078c-4f0f-4ef1-ab31-fa9f3549f163.jpg','http://cdn.ovear.info:8999/upload/cbdadd83-9772-40d5-8100-7ccfa351d2ee.jpg']
	#url.append('http://softfile.3g.qq.com/msoft/179/1105/90992/qq_2013_0_0_1718_s60v3_signed.sisx')
	#url.append('http://down.myapp.com/myapp/qqteam/Androidlite/qqlite_3.2.0.361.apk')
	#url.append('http://cdn.ovear.info:8999/upload/5c8173cd-ac7f-4405-8a1c-4b886db85412.jpg')
	#url.append('http://cdn.ovear.info:8999/upload/71d9078c-4f0f-4ef1-ab31-fa9f3549f163.jpg')
	#url.append('http://cdn.ovear.info:8999/upload/cbdadd83-9772-40d5-8100-7ccfa351d2ee.jpg')
	#url.append('http://dldir1.qq.com/qqfile/QQIntl/QQi_wireless/Android/qqi_4.6.13.6034_office.apk')
	#url = sys.argv[1]
	#t = 4
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
	#manager.q().put([url,fname])

	if len(url) == 1:
		manager.q().put('0')
		z = {}
		#进程池
		ps = []
		#创建临时文件夹
		if not os.path.exists('.tmp'):
			os.mkdir('.tmp')
		else:
			for i in glob.glob('.tmp/*.bj'):
				os.remove(i)

		#t1 = t if t <= len(url) else len(url)
		#for i in range(t1):
		z['url'] = url[0]
		z['filename'] = url[0].split('/')[-1]

		#for i in range(len(z)):
		r = s.get(z['url'],stream=True)
		#文件长度
		le = int(r.headers['Content-Length'])
		#分块
		#t3 = t2//(len(z)-i) if t2%(len(z)-i) == 0 else t2//(len(z)-i)+1
		#t2 -= t3
		l = [le//t+1 if i < le%t else le//t for i in range(t)]
		print('敌军高达数目:{} 分割:{}'.format(le,l))
		l1 = []
		b = -1
		for j in range(len(l)):
			a = b + 1
			b = a + l[j] - 1
			l1.append('{}-{}'.format(a,b))
		z['length'] = l
		z['range'] = l1

		#t1 = [[],[]]
		size = 0
		print('母舰:STEINS GATE进入战斗战斗状态')
		print('释放高达')
		ra = len(z['length'])
		for i in range(ra):
			print(i,z['range'][i],end=' ')
			#room(l[i],i)
			ra1 = ra//2 if ra%2 == 0 else ra//2+1
			if i+1 <= ra1:
				print(z['length'][i])
				size += z['length'][i]
				#print(size)
				p = multiprocessing.Process(target=write,args=(z['url'],z['filename'],i,z['range'][i]))
				p.start()
				ps.append(p)
			else:
				print(z['length'][i],end=' ')
				print('僚机')
				#pass
				manager.q().put([z['url'],z['filename'],i,z['range'][i],z['length'][i]])
	#exit()

	#else:
	#	i1 = len(z)//2 if len(z)%2 == 0 else len(z)//2+1
	#	for i in range(len(z)):
	#		ra = len(z[i]['range'])
	#		if i+1 <= i1:
	#			for j in range(ra):
	#				print(z[i]['length'][j],end=' ')
	#				size += z[i]['length'][j]
	#				#print(size)
	#				p = multiprocessing.Process(target=write,args=(z[i]['url'],z[i]['filename'],j,z[i]['range'][j]))
	#				p.start()
	#				ps.append(p)
	#		else:
	#			print('\n僚机')
	#			for j in range(ra):
	#				print(z[i]['length'][j],end=' ')
	#				#pass
	#				manager.q().put([z[i]['url'],z[i]['filename'],j,z[i]['range'][j],z[i]['length'][j]])
	

		manager.q().put(None)

		print('作战开始')
		while True:
			time.sleep(1)
			size1 = 0
			if not glob.glob('.tmp/*.bj'):
				break
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

		#for i in range(len(z)):
		os.system('cat .tmp/{}* > '.format(z['filename'])+z['filename'])
		shutil.rmtree('.tmp')

	else:
		#print(url,t)
		manager.q().put('1')
		#z = []
		#t1 = t
		#for i in range(len(url)):
		#	t2 = t1//(len(url)-i) if t1%(len(url)-i) == 0 else t1//(len(url)-i)+1
		#	t1 -= t2
		#	z.append({'url':url[i],'t':t2})
		#print(z)
		print('母舰:STEINS GATE进入战斗战斗状态')
		print('释放高达')

		i1 = len(url)//2 if len(url)%2 == 0 else len(url)//2+1
		murl = []
		mt = 0
		for i in range(len(url)):
			if i+1 <= i1:
				print(i,url[i])
				murl.append(url[i])
				#mt += z[i]['t']
			else:
				print(i,url[i],'僚机')
				manager.q().put([url[i]])
				#os.system('aria2c -x{0} -s{0} -c -U "" "{1}"')

		manager.q().put(None)
		with open('url.txt','w') as f:
			f.write('\n'.join(murl))

		#os.system('aria2c -j4 -x{0} -s{0} -c -U "" -i .tmp/url.txt'.format(mt//len(murl)))
		os.system('aria2c -j4 -x4 -s4 -c -U "" -i url.txt')
		while True:
			if not manager.q1().get():
				break
		print('战斗完毕。花费时间:'+str(int(time.time())-nt))
		print('回收高达...')
		os.system('scp -r pi@192.168.233.17:/home/pi/py/pymultidm/.tmp/ ./')
		os.system('mv .tmp/* ./')
		#shutil.rmtree('.tmp')

if __name__ == '__main__':
	main()
