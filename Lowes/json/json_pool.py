# json_pool.py
# Lowes
# Created by Noah Christiano on 7/21/2014.
# noahchristiano@rochester.edu

from multiprocessing import Process
from lowes_json import LowesJson

job_q = Queue()
result_q = Queue()

def file_contains(num):
	file = open('test.txt')
	duplicate = False
	for line in file:
		if line == num + '\n':
			print 'Found duplicate: ' + num
			duplicate = True
	file.close()
	return duplicate

def write(results):
	for r in results:
		if not file_contains(r):
			file = open('test.txt', 'a')
			print 'Writing store: ' + r
			file.write(r + '\n')
			file.close()

def writer():
	while True:
		if not result_q.empty():
			s = result_q.get()
			if s != None:
				write(s)

def worker(num):
	collector = LowesJson()
	list = collector.get_stores(num)
	return list

if __name__ == '__main__':
	pool = Pool()
	stores = []
	for i in range(500, 100000):
		stores.append(pool.apply_async(worker, (i,)))
	for store in stores:
		s = store.get()
		if s != None:
			write(s)
	pool.close()
	pool.join()
