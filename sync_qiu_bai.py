import os

__author__ = 'Administrator'
import requests
import shutil


if __name__ == '__main__':
    r = requests.get("http://www.qiushibaike.com/pic")
    page = r.text.split('class="pagebar"')[1].split('href=\"')[1].split('\"')[0]
    base_page_url = str(page).replace('/2', '/%s')
    for i in range(1, 350):
        page_url = base_page_url % i
        result = requests.get("http://www.qiushibaike.com%s" % page_url)
        if r.status_code == 200:
            thumbnails = r.text.split('class=\"thumb\"')
            for i in range(1, len(thumbnails)):
                img_url = str(thumbnails[i].split('src=\"')[1].split('\" alt')[0])
                src = requests.get(img_url, stream=True)
                path = os.path.join(os.path.dirname(__file__), '', 'media/').replace('\\', '/')
                img_name = img_url.split('/')[-1]
                with open(path + img_name, 'wb') as out_file:
                    shutil.copyfileobj(src.raw, out_file)
                comment = thumbnails[i].split('src=\"')[1].split('alt=\"')[1].split('\"')[0]

    print
