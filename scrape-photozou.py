from bs4 import BeautifulSoup
import json
import logging
import os
import pickle
import re
import requests
import time


def get_webpage(url, cookie, tmp_dir='./tmp'):
    '''Save Web page as a pickle.'''
    escaped_url = url.replace('/', ':')
    tmp_name = f'{tmp_dir}/{escaped_url}.pkl'
    if not os.path.exists(tmp_name):
        response = requests.get(url=url,cookies=cookie)
        time.sleep(sleep_time)
        if response.ok:
            with open(tmp_name, 'wb') as f: 
                pickle.dump(response, f)
        else:
            return None

    with open(tmp_name, 'rb') as f:
        response = pickle.load(f)

    print(".", end="", flush=True)

    return response.content


def get_photo_urls(html, cookie, tag):
    soup = BeautifulSoup(html, 'html.parser')
    a_thumbnail_photos = soup.select('a[class="thumbnail_photo"]')

    photo_urls = []

    for athumb in a_thumbnail_photos:
        url = photo_only_url + '/'.join(athumb.attrs['href'].split('/')[-2:])
        html = get_webpage(url, cookie)
        soup = BeautifulSoup(html, 'html.parser')
        for area in soup.select('div[id="photo_area"]'):
            original_photo_url = area.select('img')[0].attrs['src']
            photo_urls.append(original_photo_url)

    return photo_urls


def download_photo(url):
    response = requests.get(url, cookies=cookie)
    time.sleep(sleep_time)
    if response.ok:
        return response.content
    else:
        logging.error(f'HTTP Error {response.status_code}')
        return None


def save_photos(tag, urls):
    print('\nSaving photos tagged as ' + tag_name, flush=True)
    for url in urls:
        print(".", end="", flush=True)
        photo_id = url.split('/')[-2]
        photo_save_name = f'./data/{tag}/{photo_id}.jpg'
        if not os.path.exists(photo_save_name):
            photo_bin = download_photo(url)
            with open(photo_save_name, 'wb') as f:
                f.write(photo_bin)                   

    
def list_tags(userid, cookie):
    html = get_webpage(f'http://photozou.jp/photo/alltags/{userid}', cookie)
    soup = BeautifulSoup(html, 'html.parser')
    tags = []
    for tag_level in range(1, 7):
        tag_elements = soup.select(f'a[class="tag_level{tag_level}"]')
        tags += [(x.text, x.attrs['href'].split('/')[-1], tag_level) for x in tag_elements]

    return tags

    
if __name__ == '__main__':
    with open('login_info.json') as f:
        info = json.load(f)
        cookie = info['cookie']
        userid = info['userid']

    root_url = 'http://photozou.jp/'
    photo_only_url = 'http://photozou.jp/photo/photo_only/'
    data_dir = './data/'

    sleep_time = 2

    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    tags = list_tags(userid, cookie)
    photo_urls = {tag_name: [] for tag_name, _, _ in tags}

    tag_pattern = re.compile('.*')
    # tag_pattern = re.compile('^[0-9]{3}$') # 001 など、数字3ケタのタグのみ抽出する場合
    
    for tag_name, tag_url, tag_level in tags:
        if tag_pattern.match(tag_name) is None:
            logging.info(f'\n{tag_name} is skipped.')
            continue
        tagdir = data_dir + tag_name
        print('\nCreating a list of photos tagged as '+tag_name, flush=True)
        if not os.path.exists(tagdir):
            os.mkdir(tagdir)
        for page in range(1, 100000):
            list_url = f'http://photozou.jp/photo/tagged/{userid}/{tag_url}?page={page}'

            html = get_webpage(list_url, cookie)
            if html is not None:
                urls = get_photo_urls(html, cookie, tag_name)
                if len(urls) == 0:
                    break
                else:
                    photo_urls[tag_name] += urls
    print(photo_urls)

    for tag_name, urls in photo_urls.items():
        save_photos(tag_name, urls)
