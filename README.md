# Ebay Listing Scraper
Small tool to quickly scrape ebay listings based on a search query and optionally retrieve all images associated with each listing. Outputs to a JSON file.

 ## Todo:

    * Implement optional functionality for scraping completed ebay listings

## Required Packages:

[beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/)

[requests](https://github.com/psf/requests)

[progress](https://github.com/verigak/progress)

## Install:

    $ git clone https://github.com/its-sarin/ebay-listing-scraper.git
    $ pip3 install -r requirements.txt

## Basic Usage:
    # Perform a basic search using default values (defaults to searching through 1 page of results)
    $ ./scrape.py --search "product to search"

## Optional Usage:

    # Perform a search through 5 pages of results and write the output with the prefix "my output file"
    # (file name in this example would end up as: 'my-output-file--product-to-search.json'
    $ ./scrape.py --search "product to search" --pages 5 --write "my output file"
    
    # Perform a search through 5 pages of results and retrieve all associated listing images
    $ ./scrape.py --search "product to search" --pages 5 --images true

    # Perform a search, retrieve all associated listing images, and then download images to a custom folder
    $ ./scrape.py --search "product to search" --images true --download true --folder "my custom folder"
    
## Help output:

    usage: scrape.py [-h] [--search SEARCH_QUERY] [--write FILE_NAME] [--pages PAGE_COUNT] [--images GET_IMAGES] [--download DOWNLOAD_IMAGES] [--folder FOLDER_NAME]

    ** Ebay listing scraper and image retrieval **
    
    options:
      -h, --help            show this help message and exit
      --search SEARCH_QUERY
                            Term to search for on ebay
      --write FILE_NAME     Filename prefix (search query is automatically appended to the filename)
      --pages PAGE_COUNT    Number of page results to scrape (default: 1)
      --images GET_IMAGES   Whether or not to retrieve image links (default: False)
      --download DOWNLOAD_IMAGES
                            Whether or not to download gathered images - Note: this only works if you opt to retrieve image links (default: False)
      --folder FOLDER_NAME  Custom folder name for downloaded images (default: scraped-images)

