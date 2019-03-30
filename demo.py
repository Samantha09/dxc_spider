import time
import threading

# 多线程共享全局变量以及锁机制
VALUE = 0

def add_value():
    global VALUE

    for x in range(10000000):
        VALUE += 1
    print('value:%d' % VALUE)

def main():
    for x in range(2):
        t = threading.Thread(target=add_value())
        t.start()

if __name__ == '__main__':
    main()
