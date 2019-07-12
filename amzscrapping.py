from lxml import html
import csv, os, json
import requests
from time import sleep


def AmzScrapper(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    page = requests.get(url, headers=headers)
    while True:
        try:
            doc = html.fromstring(page.content)
            XPATH_BOOK_NAME = '//h1[@id="title"]//text()'
            XPATH_SALE_PRICE = '//tr[contains(@class,"kindle-price") or contains(@class,"kindle-price")]/text()'
            XPATH_ORIGINAL_PRICE = '//tr[contains(text(),"print-list-price") or contains(text(),"M.R.P") or contains(text(),"print-list-price")]/following-sibling::tr/text()'
            XPATH_BOOK_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
            XPATH_BOOK_AVAILABILITY = '//div[@id="availability"]//text()'

            RAW_BOOK_NAME = doc.xpath(XPATH_BOOK_NAME)
            RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
            RAW_BOOK_CATEGORY = doc.xpath(XPATH_BOOK_CATEGORY)
            RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
            RAW_BOOK_AVAILABILITY = doc.xpath(XPATH_BOOK_AVAILABILITY)

            BOOK_NAME = ' '.join(''.join(RAW_BOOK_NAME).split()) if RAW_BOOK_NAME else None
            SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
            BOOK_CATEGORY = ' > '.join([i.strip() for i in RAW_BOOK_CATEGORY]) if RAW_BOOK_CATEGORY else None
            ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
            BOOK_AVAILABILITY = ''.join(RAW_BOOK_AVAILABILITY).strip() if RAW_BOOK_AVAILABILITY else None

            if not ORIGINAL_PRICE:
                ORIGINAL_PRICE = SALE_PRICE

            if page.status_code != 200:
                raise ValueError('capcha')
            data = {
                'BOOK_NAME': BOOK_NAME,
                'SALE_PRICE': SALE_PRICE,
                'BOOK_CATEGORY': BOOK_CATEGORY,
                'ORIGINAL_PRICE': ORIGINAL_PRICE,
                'BOOK_AVAILABILITY': BOOK_AVAILABILITY,
                'URL': url,
            }

            return data
        except Exception as excp:
            print(excp)


def ReadASIN():
    ASINList = ['B00DDZPC9S',
                '1617294438',
                '1078096163',
                'B0131L3PW4',
                'B01N1ZXVPL',
                'B0785Q7GSY',
                'B07V4KD4GF',
                '1593275994',
                'B07N4QDH92',
                '107042434X',
                '1980953902',
                '1980953902',
                '1593276036',
                '1795050535',
                'B079FY2ZPQ',
                'B0795X6Y25',
                'B07V2B5CGS',
                '1789808898',
                'B07TW4L2B1', ]
    extracted_data = []
    for i in ASINList:
        url = "http://www.amazon.fr/dp/" + i
        print("Processing: " + url)
        extracted_data.append(AmzScrapper(url))
    f = open('data.json', 'w')
    json.dump(extracted_data, f, indent=4)


if __name__ == "__main__":
    ReadASIN()
