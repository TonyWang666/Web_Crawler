# # import thread
# from threading import Thread, RLock
# # import threading

# gLock = RLock()

# def writeFile(val):
#     print('start printing...')
#     output = open('/Users/jiaxiangwang/Downloads/UCI/spring2020/CS121/HW2/spacetime-crawler4py/11111.txt', 'w', encoding="utf-8")
#     output.write("WE are the champion...")
#     output.write(val)
#     output.close()

# try:
#     gLock.acquire()
#     Thread(target=writeFile('1'))
#     gLock.release()
#     gLock.acquire()
#     Thread(target=writeFile('2'))
#     gLock.release()
# except Exception as e:
#     print(e)

# output = open('testing.txt', 'w')

# output.write('testing for fileName')
from queue import Queue, Empty
test = Queue()
test.put('Tony')
test.put('Bob')
test.put('Si')
print(test.get())

print(test.get())
test.put('Tim')
print(test.get())