from queue import Queue
import time
import threading

# 创建队列时可以指定大小
# q = Queue(4)
# for i in range(5):
#     q.put(i)
#     print("写入队列")
#
# # 返回队列的大小
# print(q.qsize())
#
# # 判断是否为空
# print(q.empty())
#
# # 判断队列是否满了
# print(q.full())
#
# # 从队列当中取最先近队列的元素
# for i in range(4):
#     print(q.get()) # 先进先出
#
# q.put(block=True)  # 默认开启，队列为空时，会一直阻塞

def set_value(q):
    index = 0
    while True:
        q.put(index)
        index += 1
        time.sleep(3)


def get_value(q):
    while True:
        print(q.get())


def main():
    q = Queue(4)
    t1 = threading.Thread(target=set_value, args = [q])
    t2 = threading.Thread(target=get_value, args = [q])

    t1.start()
    t2.start()


if __name__ == '__main__':
    main()