import requests
#import queue
#from multiprocessing.managers import BaseManager
import multiprocessing.managers
import os
import shutil
import sys
#from socket import *
import glob
import subprocess
import time

def write(url,fname,t,ra,c=0):
	s = requests.session()
	#if t >= 10 and t1 < 10:
	#	t1 = '0' + str(t1)
	##t = str(t) if t >= 10 else '0'+str(t)
	#else:
	t = str(t)
	if c:
		mode = 'ab'
		print('续传模式')
		if os.path.exists('.tmp/'+fname+'.'+t+'.bj'):
			op = os.path.getsize('.tmp/'+fname+'.'+t+'.bj')
			ra = str(int(ra.split('-')[0])+op) + '-' + ra.split('-')[1]
	else:
		mode = 'wb'
	s.headers['Range'] = 'bytes='+ra
	s.headers['User-Agent'] = 'netdisk'
	r = s.get(url,stream=True,headers=s.headers)
	with open('.tmp/'+fname+'.'+t+'.bj',mode) as f:
		for i in r.iter_content(chunk_size=512):
			f.write(i)
			f.flush()
		#f.write(r.content)

def main(c):
	if not os.path.exists('.tmp'):
		os.mkdir('.tmp')
	#else:
	print('高达编号:零号机 启动')
	b = multiprocessing.managers.BaseManager
	b.register('q')
	b.register('q1')
	b.register('q3')
	m = b(address=('192.168.233.15',5000),authkey='abc'.encode('utf-8'))

	while True:
		#send = socket(AF_INET,SOCK_STREAM)
		#recv = socket(AF_INET,SOCK_STREAM)
		#recv.bind(('0.0.0.0',8001))
		#recv.listen(True)
		#conn,addr = recv.accept()
		#send.send(True)
		#while True:
		#	if conn.recv:
		#		break
		#send.connect(('192.168.233.15',8000))

		try:
			m.connect()
			l = m.q().get()
		except:
			continue

		if not c:
			for i in glob.glob('.tmp/*'):
				os.remove(i)

		print('脱离母舰...')
		if l == '0':
		#	url = l[0]
		#	fname = l[1]
			ps = []
			size = 0
			while True:
				l = m.q().get()
				if not l:
					print('前方高能，非战斗人员请迅速撤离')
					print('作战开始')
					break
				print(l[1],l[2],l[3],l[4])
				size += l[4]
				p = multiprocessing.Process(target=write,args=(l[0],l[1],l[2],l[3],c))
				p.start()
				ps.append(p)

			while True:
				time.sleep(1)
				size1 = 0
				#if not glob.glob('.tmp/*.bj'):
				#   break
				for i in glob.glob('.tmp/*.bj'):
					size1 += os.path.getsize(i)
				col = int(subprocess.getoutput('stty size').split(' ')[1])
				col1 = col-8
				p = int(size1/size*col1)
				#print(col,col1,p,col1-p-1)
				if size1 != size:
					print('\r['+'='*p+'>'+' '*(col1-p-1)+']{0:>4.1f}% '.format(size1/size*100),end='')
					#print(']{0:>4.1f}% '.format(size1/size*100),end='\r')
				else:
					#print('['+'='*p+' '*(col1-p),end='')
					print('\r['+'='*(col1-1)+'>',end='')
					print(']100.0%')
					break

			for i in ps:
				i.join()

			while True:
				if not m.q3().get():
					break
			m.q1().put(None)
			print('战斗完毕，归队')
			print('Done.')

		else:
			wurl = []
			#wt = 0
			while True:
				l = m.q().get()
				if not l:
					break
				print(l[0])
				wurl.append(l[0])
				#wt += int(l[1])
			#print(' '.join(wurl),wt)
			with open('url.txt','w') as f:
				f.write('\n'.join(wurl))
			print('前方高能，非战斗人员请迅速撤离')
			print('作战开始')
			os.system('aria2c -j4 -x4 -s4 -c -U "" -i url.txt -d .tmp/')

			while True:
				if not m.q3().get():
					break
			m.q1().put(None)

			print('战斗完毕，归队')
			print('Done.')
			#l = glob.glob('.tmp/*')
			#l.sort()
			#for i in l:
			#	print(i)
			#	f = open(i,'rb')
			#	while True:
			#		filedata = f.read(8)
			#		if not filedata:
			#			break
			#		send.send(filedata)
			#	f.close

			#shutil.rmtree('.tmp')

if __name__ == '__main__':
	if len(sys.argv) == 2:
		if sys.argv[1] == '-c':
			c = 1
	else:
		c = 0
	main(c)
