import os
import aiohttp
import asyncio
import argparse
import json
from pathlib import Path
from hashlib import md5

def get_filename(url):
    return md5(url.encode('utf-8')).hexdigest()

async def fetch(session, base_url, id, save_path):
    url = base_url + id

    async with session.get(url) as response:
        text = await response.text()
        filename = get_filename(base_url + id)

        with open(os.path.join(save_path, filename), 'w') as f:
            f.write(text)

        # do something with the response text here
        print(f'sent request to {url}')

        return text

async def main(args):
    # create outpath if it doesn't exist
    Path(args['outpath']).mkdir(exist_ok=True)

    with open(args['csv_path'], 'r') as f:
        ids = [x.strip() for x in f.read().split(args['csv_delimiter'])]

    # limit the number of concurrent connections using a custom connector
    connector = aiohttp.TCPConnector(limit_per_host=args['concurrent_limit'])

    async with aiohttp.ClientSession(connector=connector) as session:
        await asyncio.wait([fetch(session, args['base_url'], id, args['outpath']) for id in ids])

    with open(os.path.join(args['outpath'], 'metadata.json'), 'w') as f:
        meta = {get_filename(args['base_url'] + x):(args['base_url'] + x) for x in ids}
        json.dump(meta, f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Concurrent web scraping tool using parallelized coroutines.")
    parser.add_argument("-c", "--concurrent-limit", type=int, default=10, help="Number of simultaneous connections to allow.")
    parser.add_argument("-b", "--base-url", type=str, default="https://en.wikipedia.org/wiki/", help="Base url to which requests will be made.")
    parser.add_argument("-p", "--csv-path", type=str, default="scrape_urls.csv", help="Path to file containing list of IDs to retrieve.")
    parser.add_argument("-d", "--csv-delimiter", type=str, default=",", help="Delimiter to use when reading csv file.")
    parser.add_argument("-o", "--outpath", type=str, default="scraped", help="Path at which results are saved.")
    args = vars(parser.parse_args())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args))
