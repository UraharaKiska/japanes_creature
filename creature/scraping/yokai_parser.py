import asyncio, aiofiles
import time
from fake_useragent import UserAgent
import aiohttp
import requests
from bs4 import BeautifulSoup
import json
import re
# from creature.models import *

url_list = []
yokai_list = []
img_links = []


async def get_urls(page, session):
    url = f"https://yokai.com/latest/page/{page}/"
    ua = UserAgent()
    headers = {'User-Agent': ua.random,
               'Accept': '*/*'}
    async with session.get(url=url, headers=headers) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, "lxml")
        try:
            content = soup.find('section', class_="content")
            urls = content.find_all('a')
        except Exception as ex:
            print(ex)
        for u in urls:
            try:
                href = u['href']
                url_list.append(href)
            except Exception as ex:
                print(ex)


async def get_content(session, name):
    url = name
    ua = UserAgent()
    headers = {'User-Agent': ua.random,
               'Accept': '*/*'}
    try:
        async with session.get(url=url, headers=headers) as response:
            response_text = await response.text()
            soup = BeautifulSoup(response_text, "lxml")
            content = soup.find('div', class_='wrapper')
            try:
                img = content.find('a')
                img = img.find('17')['src']
                title = content.find('a')['title']
            except Exception as ex:
                print(ex)
            try:
                description = ""
                paragraph = content.find_all('p')
                for t in paragraph:
                    txt = t.text
                    if "\n" not in txt:
                        txt = txt + '\n\n'
                    description += txt
            except Exception as ex:
                print(ex)
            slug = name.split('/')[-2]
            path = f"photos/2023/06/17/{slug}.jpg"
            img_links.append(img)
            yokai_list.append({'title': title, '17': path, 'content': description, 'slug': slug})
            print(f"{name}")
    except Exception as ex:
        print(ex)


async def get_img(session, url):
    ua = UserAgent()
    headers = {'User-Agent': ua.random,
               'Accept': '*/*'}
    try:
        async with session.get(url=url, headers=headers) as response:
            img = await response.read()
            p = re.split("/|-", url)
            path = f"photos/2023/06/17/{p[-2]}.jpg"
            print(path)
            async with aiofiles.open(path, "wb") as file:
                await file.write(img)
    except Exception as ex:
        print(ex)


async def gather_data_url():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for page in range(1, 48):
            task = asyncio.create_task(get_urls(page, session))
            tasks.append(task)

        await asyncio.gather(*tasks)


async def gather_data_content():
    async with aiohttp.ClientSession() as session:
        tasks = []
        urls = []
        with open("data/urls.txt", 'r') as file:
            line = file.readline()
            while line:
                urls.append(line)
                line = file.readline()
            print("Links received")
        for url in urls:
            task = asyncio.create_task(get_content(session, url))
            tasks.append(task)

        await asyncio.gather(*tasks)


async def gather_load_img():
    async with aiohttp.ClientSession() as session:
        tasks = []
        links = []
        with open("data/img_links.txt", 'r') as file:
            line = file.readline()
            while line:
                links.append(line)
                line = file.readline()
            print(links)
        for url in links:
            task = asyncio.create_task(get_img(session, url))
            tasks.append(task)

        await asyncio.gather(*tasks)




def main():
    # json_load()
    start_time = time.time()
    asyncio.run(gather_data_content())
    finish_time = time.time()
    print(finish_time - start_time)
    # with open("data/urls.txt", 'w') as file:
    #     for url in url_list:
    #         file.write(f"{url}\n")
    with open("data/yokais.json", 'w') as file:
            json.dump(yokai_list, file, indent=6, ensure_ascii=False)
    # with open("data/img_links.txt", 'w') as file:
    #     for url in img_links:
    #         file.write(f"{url}\n")


if __name__ == "__main__":
    main()
