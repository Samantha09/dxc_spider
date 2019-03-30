"""
Lock版本的生产者与消费者模式可以正常的运行，但是存在着一个不足，在消费者中，总是通过while true死循环并且上锁的方式去判断钱够不够，上锁是一个很耗费CPU的操作，因此这种方式不是最好的。
用threading.Condition来实现。threading.Condition可以在没有数据的时候处于阻塞等待状态。一旦有合适的数据了，还可以使用notify相关的函数做个介绍
"""
import threading
import random
import time

gMoney = 1000
gCondition = threading.Condition()
gTotalTimes = 10
gTimes = 0

class Producer(threading.Thread):
    def run(self):
        global gMoney, gTimes, gTotalTimes
        while True:
            money = random.randint(100, 1000)
            gCondition.acquire()
            if gTimes >= gTotalTimes:
                gCondition.release()
                break
            gMoney += money
            print("%s生产了%d元，剩余%d元" % (threading.current_thread(), money, gMoney))
            gTimes += 1
            gCondition.notify_all()
            gCondition.release()
            time.sleep(0.5)


class Consumer(threading.Thread):
    def run(self):
        global gMoney
        while True:
            money = random.randint(100,1000)
            gCondition.acquire()

            while gMoney < money:
                if gTimes >= gTotalTimes:
                    gCondition.release()
                    return
                print("%s准备消费%d元钱，剩余%d元钱， 不足！" % (threading.current_thread(), money, gMoney))
                gCondition.wait()
            gMoney -= money
            print("%s消费了%d元，剩余%d元" % (threading.current_thread(), money, gMoney))
            gCondition.release()
            time.sleep(0.5)


def main():
    for i in range(5):
        t = Consumer(name="消费者线程%d" % i)
        t.start()

    for i in range(5):
        t = Producer(name="生产者线程%d" % i)
        t.start()




if __name__ == '__main__':
    main()