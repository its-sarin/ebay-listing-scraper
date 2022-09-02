#!/usr/bin/python3

import os
import json
import argparse
import requests
from bs4 import BeautifulSoup
from progress.bar import Bar

parser = argparse.ArgumentParser(description='** Ebay listing scraper and image retrieval **')

parser.add_argument('--search', dest='search_query', type=str, help='Term to search for on ebay')
parser.add_argument('--write', dest='file_name', type=str,
                    help='Filename prefix (search query is automatically appended to the filename)')
parser.add_argument('--pages', dest='page_count', type=int, help='Number of page results to scrape (default: 1)')
parser.add_argument('--images', dest='get_images', type=bool,
                    help='Whether or not to retrieve image links (default: False)')
parser.add_argument('--download', dest='download_images', type=bool,
                    help='Whether or not to download gathered images - Note: this only works if you opt to retrieve image links (default: False)')
parser.add_argument('--folder', dest='folder_name', type=str, help='Custom folder name for downloaded images (default: scraped-images)')

args = parser.parse_args()

SHOULD_GET_IMAGE_LINKS = args.get_images or False
SHOULD_DL_IMAGES = True if args.get_images and args.download_images else False
SEARCH_QUERY = args.search_query.replace(' ', '+') if args.search_query is not None else ''
NUM_PAGES = args.page_count or 1
FILE_NAME = args.file_name or 'ebay-scraped-results'
FILE_NAME = FILE_NAME.replace(' ', '-') + '--' + SEARCH_QUERY.replace('+', '-') + '.json'
FOLDER_NAME = args.folder_name.replace(' ', '-') or 'scraped-images'


item_names = []
item_links = []
item_image_links = []
output = {}


def retrieve_listings():
    if SEARCH_QUERY == '':
        print("Please use the --search argument with a search query")
        return

    for i in range(NUM_PAGES):
        print('** Scraping results page: ' + str(i) + ' **')
        ebay_url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=" + SEARCH_QUERY + "&_sacat=0&LH_TitleDesc=0&_pgn=" + str(
            i)
        r = requests.get(ebay_url)
        soup = BeautifulSoup(r.content, features="lxml")
        listings = soup.find_all('li', attrs={'class': "s-item s-item__pl-on-bottom s-item--watch-at-corner"})

        with Bar('Processing Listings', max=len(listings)) as bar:
            for listing in listings:
                bar.next()
                for title_divs in listing.find_all('div', attrs={'class': "s-item__title"}):
                    for title_div in title_divs:
                        item_title = title_div.text

                        if item_title is not None:
                            if item_title.count('New Listing'):
                                item_title = item_title.replace('New Listing', '')

                            item_names.append(item_title)

                            link = listing.find('a', attrs={'class': "s-item__link"})['href']

                            if link is not None:
                                item_links.append(link)

                                output[item_title] = {
                                    'url': link
                                }

            bar.finish()

    if SHOULD_GET_IMAGE_LINKS:
        retrieve_image_links()
    else:
        write_to_file()


def retrieve_image_links():
    with Bar('Processing Images  ', max=len(item_links)) as bar:
        for i in range(len(item_links)):
            bar.next()
            ebay_url = item_links[i]
            r = requests.get(ebay_url)
            soup = BeautifulSoup(r.content, features="lxml")
            image_div = soup.find('div', attrs={'id': 'vi_main_img_fs'})

            if image_div is not None:
                images = image_div.find_all('li', attrs={'class': 'v-pic-item'})

                for image in images:
                    image_link = image.find('img')['src']

                    if image_link is not None:
                        if image_link.count('ebaystatic'):
                            continue
                        else:
                            image_link = image_link.split('/')
                            image_link[6] = 's-l1600.jpg'
                            joiner = '/'
                            image_link = joiner.join(image_link)

                            item_image_links.append(image_link)

                output[item_names[i]].update({
                    'image_urls': item_image_links
                })

        bar.finish()

    write_to_file()

    if SHOULD_DL_IMAGES:
        download_images()


def download_images():
    if not os.path.exists(FOLDER_NAME):
        os.mkdir(FOLDER_NAME)

    print('** Downloading Images **')

    with Bar('Downloading Images  ', max=len(item_image_links)) as bar:
        for image_link in item_image_links:
            bar.next()
            response = requests.get(image_link)
            image_id = image_link.split('/')
            destination = FOLDER_NAME + '/' + SEARCH_QUERY.replace('+', '-') + '--' + image_id[5] + '.jpg'

            with open(destination, 'wb') as fh:
                fh.write(response.content)

        bar.finish()


def write_to_file():
    with open(FILE_NAME, 'w') as file:
        file.write(json.dumps(output, indent=4))
        print("File created at: " + FILE_NAME + '\n')


if __name__ == '__main__':
    retrieve_listings()
