# X-Scraper

Simple tool for concurrent web scraping. To use,

```sh
pip install requirements.txt
python xscraper.py
```

Add your target urls to `scrape_urls.csv` (or whichever file you specify), separated by commas.

## Advanced usage:

```sh
usage: xscraper.py [-h] [-c CONCURRENT_LIMIT] [-b BASE_URL] [-p CSV_PATH]
                   [-d CSV_DELIMITER] [-o OUTPATH]

Concurrent web scraping tool using parallelized coroutines.

optional arguments:
  -h, --help            show this help message and exit
  -c CONCURRENT_LIMIT, --concurrent-limit CONCURRENT_LIMIT
                        Number of simultaneous connections to allow.
  -b BASE_URL, --base-url BASE_URL
                        Base url to which requests will be made.
  -p CSV_PATH, --csv-path CSV_PATH
                        Path to file containing list of IDs to retrieve.
  -d CSV_DELIMITER, --csv-delimiter CSV_DELIMITER
                        Delimiter to use when reading csv file.
  -o OUTPATH, --outpath OUTPATH
                        Path at which results are saved.
```
