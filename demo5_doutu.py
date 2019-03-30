import requests
from lxml import etree
from urllib import request
import os, re

def parse_page(url):
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

        request.urlretrieve(img_url, file_name)




def main():
    for x in range(1, 10):
        url = 'https://www.doutula.com/photo/list/?page=%d' % x
        parse_page(url)


if __name__ == '__main__':
    main()