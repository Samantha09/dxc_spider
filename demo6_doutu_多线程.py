import requests
from lxml import etree
from urllib import request
import os, re
from queue import Queue
import threading
import csv

class Producer(threading.Thread):
    def __init__(self, page_queue, img_queue,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            self.parse_page(url)


    def parse_page(self, url):
        headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
        }

        response = requests.get(url, headers)
        text = response.text

        html = etree.HTML(text)

        imgs = html.xpath("//div[@class ='page-content text-center']//img[@class!='gif']")

        for img in imgs:
            img_url = img.get('data-original')  # get()函数可以获取属性
            img_name = img.get('alt')
            # img_name = re.sub('[\?？。\.，！@#￥%^!]', '', img_name)
            suffix = os.path.splitext(img_url)[1]
            file_name = 'images/' + img_name + suffix
            print(file_name)
            self.img_queue.put((img_url, file_name))  # 在队列中放元祖


class Consumer(threading.Thread):
    def __init__(self, page_queue, img_queue,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.img_queue.empty() and self.page_queue.empty():
                break
            img_url, filename = self.img_queue.get()
            request.urlretrieve(img_url, filename)
            print(filename, "下载完成")


def main():
    page_queue = Queue(100)
    img_queue = Queue(1000)
    for x in range(1, 100):
        url = 'https://www.doutula.com/photo/list/?page=%d' % x
        page_queue.put(url)

    for x in range(10):
        t = Producer(page_queue, img_queue)
        t.start()

    for x in range(10):
        t = Consumer(page_queue, img_queue)
        t.start()


if __name__ == '__main__':
    main()