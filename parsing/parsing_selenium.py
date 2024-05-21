from typing import Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup as BS
from selenium.webdriver.common.by import By
from seleniumbase import SB

from sitemain.settings import PARSING_LINKS, logger


class ParsingSelenium:

    def __init__(self, count: int) -> None:
        self.count = count

    def verify_success(self, sb, selector: int = 1) -> str:
        if selector == 1:
            sb.find_element(By.CSS_SELECTOR, 'div.tile-root')
        else:
            sb.find_element(By.CSS_SELECTOR, 'h1.tsHeadline550Medium')
        sb.sleep(4)
        return sb.get_page_source()

    def parsing_goods(self) -> list:
        page_source = None
        links_products = []
        products = []

        for i in range(3):
            if len(links_products) > self.count:
                break
            full_url = urljoin(PARSING_LINKS, f'?page={i}')
            for j in range(1, 4):
                page_source = self.open_site(full_url)
                if page_source:
                    logger.info(f'Site open - {full_url} after trying - {j}')
                    break

            links_products.extend(self.get_links_products(page_source))

        user_links_products = links_products[:self.count]

        for url in user_links_products:

            for i in range(1, 4):
                page_source = self.open_site(url, 2)
                if page_source:
                    logger.info(f'Site open - {url} after trying - {i}')
                    break
            products.append(self.get_product(page_source, url))

        return products

    def open_site(self, url: str, selector: int = 1) -> Optional[str]:

        page_source = None

        with SB(uc_cdp=True, guest_mode=True) as sb:
            sb.open(url)
            try:
                page_source = self.verify_success(sb, selector)
            except Exception as e:
                logger.error(f'{type(e)} - {e}')
                if sb.is_element_visible('button#reload-button'):
                    sb.click('button#reload-button')
                elif sb.is_element_visible('iframe'):
                    sb.switch_to_frame('iframe')
                    sb.click('label.cb-lb')
                try:
                    self.verify_success(sb, selector)
                except Exception as e:
                    logger.error(f'{type(e)} - {e}')

        return page_source

    def get_links_products(self, page_source: str) -> list:
        links = []
        soup = BS(page_source, 'html.parser')
        goods = soup.select('div.tile-root')
        for item in goods:
            href = item.select_one('a.tile-hover-target').get('href')
            url = urljoin('https://www.ozon.ru', href)
            links.append(url)
        return links

    def get_product(self, page_source: str, url: str) -> dict:
        product = {}
        soup = BS(page_source, 'html.parser')
        try:
            product['name'] = soup.select_one('h1').text.strip()
            product['price'] = self.clean_field_price(soup.find('span', attrs={'class': ['yl6', 'zl2']}).text)
            description = soup.select_one('div.RA-a1')
            product['description'] = description.text.strip() if description else '-'
            product['image_url'] = soup.select_one('img.w0j').get('src')
            discount = soup.select_one('div[data-widget="webGallery"] div.b13-b0')
            if discount: product['discount'] = discount.text
        except Exception as e:
            logger.error(f'{type(e)} - {e}\n{url}')
        return product

    @classmethod
    def clean_field_price(cls, price: str) -> str:
        return price.strip(' ₽').replace(' ', '').replace('\u2009', '')
