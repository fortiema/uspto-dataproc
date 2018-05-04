"""Crawler for USPTO buld download website

This script fetches full text patent grant data from USPTO website.
Implemented using async Producer/Consumer paradigm.
"""
import asyncio
import os
import sys

import aiohttp
import async_timeout
from bs4 import BeautifulSoup


ROOT_STORAGE = '/data/datasets/patents/'
ROOT_URL = 'https://bulkdata.uspto.gov/data/patent/grant/redbook/fulltext/'

CHUNK_SIZE = 1 * 1024 * 1024

Q_CRAWL = asyncio.Queue()


async def fetch_url(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()


async def file_fetcher():
    await asyncio.sleep(5)
    async with aiohttp.ClientSession() as session:
        print('Fetching work from queue...')
        while not Q_CRAWL.empty():
            url, fname = await Q_CRAWL.get()
            print('Downloading \'{}\'...'.format(url))
            with async_timeout.timeout(600):
                async with session.get(url) as resp:
                    with open(fname, 'wb') as fout:
                        while True:
                            chunk = await resp.content.read(CHUNK_SIZE)
                            if not chunk:
                                break
                            fout.write(chunk)
                print('\'{}\' saved!'.format(fname))
        print('Queue is empty - Bye!')


async def process_year(year, outdir):
    print('Crawling year {}'.format(year))
    async with aiohttp.ClientSession() as session:
        html = await fetch_url(session, ROOT_URL + str(year))

        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href', '')
            if href.endswith('.zip'):
                url = ROOT_URL + str(year) + '/' + href
                fname = os.path.join(outdir, url.split('/')[-1])
                if not os.path.exists(fname):
                    await Q_CRAWL.put((url, fname))


def main(year=None, outdir='uspto-data'):
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(process_year(year, outdir))]
    loop.run_until_complete(asyncio.wait(tasks))
    tasks2 = [loop.create_task(file_fetcher()) for _ in range(5)]
    loop.run_until_complete(asyncio.wait(tasks2))
    loop.close()


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
