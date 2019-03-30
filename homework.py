import requests
import re, os
from queue import Queue
import threading
from lxml import etree
import csv


class Producer(threading.Thread):

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    }

    def __init__(self, page_queue, joke_queue):
        super().__init__()
        self.base_domain = 'http://www.budejie.com'
        self.page_queue = page_queue
        self.joke_queue = joke_queue

    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get(timeout=10)
            response = requests.get(url, headers=self.headers, timeout=5)
            text = response.text

            html = etree.HTML(text)

            descs = html.xpath("//div[@class='j-r-list']/ul/li")

            for desc in descs:
                user_name = desc.xpath(".//a[@class='u-user-name']/text()")
                if user_name:
                    user_name = user_name[0]
                else:
                    user_name = "NULL"
                content = desc.xpath("./div[@class='j-r-list-tool']/@data-title")
                if content:
                    content = content[0]
                else:
                    content = "NULL"
                like_num = desc.xpath(".//li[@class='j-r-list-tool-l-up']//span/text()")
                if like_num:
                    like_num = like_num[0]
                else:
                    like_num = "NULL"
                img_url = desc.xpath(".//div[@class='j-r-list-c-img']//img/@src")
                if img_url:
                    img_url = img_url[0]
                else:
                    img_url = "NULL"
                self.joke_queue.put((user_name, content, like_num, img_url))
            self.page_queue.task_done()
            if self.page_queue.empty():
                break


class Consumer(threading.Thread):

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    }

    def __init__(self, page_queue, joke_queue):
        super().__init__()
        self.page_queue = page_queue
        self.joke_queue = joke_queue

    def run(self):
        while True:
            if self.page_queue.empty() and self.joke_queue.empty():
                break
            user_name, content, like_num, img_url = self.joke_queue.get(timeout=10)
            print(user_name)
            titles = ["user_name", "content", "like_num", "img_url"]

            value = {
                "user_name": user_name,
                "content": content,
                "like_num": like_num,
                "img_url": img_url
            }

            with open("joke.csv", 'a', encoding='utf8') as f:
                writer = csv.DictWriter(f, titles)
                # 写入表头数据的时候，需要调用writeheader
                writer.writeheader()
                writer.writerow(value)
            self.joke_queue.task_done()


def main():
    page_queue = Queue()
    joke_queue = Queue()

    for i in range(1, 50):
        url = "http://www.budejie.com/%d" % i
        print(url)
        page_queue.put(url)

    for i in range(5):
        t = Producer(page_queue, joke_queue)
        # t.setDaemon(True)
        t.start()

    for i in range(5):
        t = Consumer(page_queue, joke_queue)
        # t.setDaemon(True)
        t.start()

    # for q in [page_queue, joke_queue]:
    #     q.join()


if __name__ == '__main__':
    main()




