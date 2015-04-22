#import os
#
#print('Process (%s) start...' % os.getpid())
#pid = os.fork()
#if pid==0:
#	print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
#else:
#	print('I (%s) just created a child process (%s).' % (os.getpid(), pid))
#from multiprocessing import Process


import requests
s = requests.session()
url = 'http://dmimg.5054399.com/allimg/narutopic/140218d/1.jpg'
fname = url.split('/')[-1]

r = s.head(url)
len = int(r.headers['Content-Length'])
sp = len//2
print(sp,len)

import multiprocessing,time
#
f = open(fname,'wb')
lock = multiprocessing.Lock()
f.seek(len-1)
f.write(b'\x00')
f.flush()

def write(offset,f,lock,op,ed):
#def write():
	s = requests.session()
	s.headers['Range'] = 'bytes='+op+'-'+ed
	print(s.headers)
	r = s.get(url,stream=True,headers=s.headers)
	for i in r.iter_content(chunk_size=1024):
		print(offset)
		if i:
			with lock:
				f.seek(offset)
				f.write(i)
				#print(i)
				f.flush()
		time.sleep(1)
		offset += 1024
#
a = 0
op = '0'
ed = str(sp)
ps = []
for i in range(multiprocessing.cpu_count()-2):
	#p = multiprocessing.Process(target=write,args=(s,a,f,lock,op,ed))
	p = multiprocessing.Process(target=write,args=(a,f,lock,op,ed))
	a += sp
	op = str(a)
	ed = ''
	p.start()
	ps.append(p)

for i in ps:
	p.join()

f.close()

#import urllib
#import urllib2
#import threading,time
#
# 
#
##线程函数
#def threadcode(start,end):
#req = urllib2.Request('http://guidetodatamining.com/guide/ch2/BX-Dump.zip')
#req.headers['Range'] = 'bytes=%s-%s' % (start, end)
#response = urllib2.urlopen(req)
#
##互斥临界区
#l.acquire()
#f.seek(start,0)
#f.write(response.read())
#l.release()
#
#
## Get file size function 获得文件大小
#def GetHttpFileSize(url): 
#length = 0 
#try: 
#conn = urllib.urlopen(url) 
#headers = conn.info()
#except Exception, err: 
#pass 
#
#return int (headers['Content-Length'])
#
##分割文件方便多线程下载 
#def Split(size,blocks): 
#
#ranges = [] 
#blocksize = size / blocks 
#for i in xrange(blocks-1): 
#ranges.append((i*blocksize,blocksize*i+blocksize-1))
#
#ranges.append(( blocksize*(blocks-1), size-1)) 
#print ranges 
#return ranges
#
#
##建立多线程
#url = 'http://guidetodatamining.com/guide/ch2/BX-Dump.zip'
#thread_num = 5
#file_len = GetHttpFileSize(url)
#l=threading.Lock()
#ranges=Split(file_len,thread_num)
#f=open("multithreads.zip",'wb+')
#childthreads=[]
#for i in range(thread_num):
#t = threading.Thread( target = threadcode, name="Thread-%d" % i,args=(ranges[i]))
#t.start()
#childthreads.append(t)
#
#for t in childthreads:
#t.join()
#
#f.close()
#print 'down'

# -*- coding: utf-8 -*-
# Author: ToughGuy
# Email: wj0630@gmail.com
# 写这玩意儿是为了初步了解下python的多线程机制
# 平时没写注释的习惯, 这次花时间在代码里面写上注释也是希望有问题的地方请各位指正, 因为可能我自己也没弄明白.
# 测试平台 Ubuntu 13.04 X86_64 Python 2.7.4
 
#import threading
#import urllib2
#import sys
# 
#max_thread = 10
## 初始化锁
#lock = threading.RLock()
# 
#class Downloader(threading.Thread):
#	def __init__(self, url, start_size, end_size, fobj, buffer):
#		self.url = url
#		self.buffer = buffer
#		self.start_size = start_size
#		self.end_size = end_size
#		self.fobj = fobj
#		threading.Thread.__init__(self)
# 
#	def run(self):
#		"""
#			马甲而已
#		"""
#		with lock:
#			print 'starting: %s' % self.getName()
#		self._download()
# 
#	def _download(self):
#		"""
#			我才是搬砖的
#		"""
#		req = urllib2.Request(self.url)
#		# 添加HTTP Header(RANGE)设置下载数据的范围
#		req.headers['Range'] = 'bytes=%s-%s' % (self.start_size, self.end_size)
#		f = urllib2.urlopen(req)
#		# 初始化当前线程文件对象偏移量
#		offset = self.start_size
#		while 1:
#			block = f.read(self.buffer)
#			# 当前线程数据获取完毕后则退出
#			if not block:
#				with lock:
#					print '%s done.' % self.getName()
#				break
#			# 写如数据的时候当然要锁住线程
#			# 使用 with lock 替代传统的 lock.acquire().....lock.release()
#			# 需要python >= 2.5
#			with lock:
#				sys.stdout.write('%s saveing block...' % self.getName())
#				# 设置文件对象偏移地址
#				self.fobj.seek(offset)
#				# 写入获取到的数据
#				self.fobj.write(block)
#				offset = offset + len(block)
#				sys.stdout.write('done.\n')
# 
# 
#def main(url, thread=3, save_file='', buffer=1024):
#	# 最大线程数量不能超过max_thread
#	thread = thread if thread <= max_thread else max_thread
#	# 获取文件的大小
#	req = urllib2.urlopen(url)
#	size = int(req.info().getheaders('Content-Length')[0])
#	# 初始化文件对象
#	fobj = open(save_file, 'wb')
#	# 根据线程数量计算 每个线程负责的http Range 大小
#	avg_size, pad_size = divmod(size, thread)
#	plist = []
#	for i in xrange(thread):
#		start_size = i*avg_size
#		end_size = start_size + avg_size - 1
#		if i == thread - 1:
#			# 最后一个线程加上pad_size
#			end_size = end_size + pad_size + 1
#		t = Downloader(url, start_size, end_size, fobj, buffer)
#		plist.append(t)
# 
#	#  开始搬砖
#	for t in plist:
#		t.start()
# 
#	# 等待所有线程结束
#	for t in plist:
#		t.join()
# 
#	# 结束当然记得关闭文件对象
#	fobj.close()
#	print 'Download completed!'
# 
#if __name__ == '__main__':
#	url = 'http://192.168.1.2:8082/downloads/10M.zip'
#	main(url=url, thread=10, save_file='test.iso', buffer=4096)
