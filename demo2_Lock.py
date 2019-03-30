import threading
import random
import time

gMoney = 1000
gLock = threading.Lock()

class Producer(threading.Thread):
    def run(self):
        global gMoney
        while True:
            money = random.randint(100, 1000)
            gLock.acquire()
            gMoney += money
            print("%s生产了%d元，剩余%d元" % (threading.current_thread(), money, gMoney))
            gLock.release()
            time.sleep(0.5)


class Consumer(threading.Thread):
    def run(self):
        global gMoney
        while True:
            money = random.randint(100,1000)
            gLock.acquire()
            if gMoney >= money:
                gMoney -= money
                print('%s消费者消费了%d元钱， 剩余%d元钱' % (threading.current_thread(), money, gMoney))
            gLock.release()
            time.sleep(0.5)


def main():
    for i in range(5):
        t = Producer(name="生产者线程%d"%i)
        t.start()

    for i in range(3):
        t = Consumer(name="消费者线程%d"%i)
        t.start()


if __name__ == '__main__':
    main()