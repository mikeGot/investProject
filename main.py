import requests
from bs4 import BeautifulSoup


class Currency:
    DOLLAR_RUB = 'https://www.google.ru/search?q=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0&newwindow=1&client=safari&channel=mac_bm&source=hp&ei=6a0nYeLxCYzy-QbTj7WoAQ&iflsig=AINFCbYAAAAAYSe7-WKeDsP6k2hm8vV1CJgpukS8OPQZ&oq=%D0%BA%D1%83%D1%80%D1%81+&gs_lcp=Cgdnd3Mtd2l6EAEYADINCAAQgAQQsQMQRhCCAjIICAAQgAQQsQMyCAgAEIAEELEDMggIABCABBCxAzILCAAQgAQQsQMQgwEyBQgAEIAEMgUIABCABDIFCAAQgAQyCAgAEIAEELEDMgUIABCABDoXCAAQgAQQsQMQxwEQ0QMQiwMQqAMQ0gM6GggAEIAEELEDEIMBEMcBEKMCEIsDEKgDEKcDUJ0bWKofYKcxaAFwAHgAgAHTAYgBrQWSAQUwLjQuMZgBAKABAbABALgBAg&sclient=gws-wiz'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15'}

    current_converted_price = 0

    def __init__(self):
        self.current_converted_price = float(self.get_currency_price().replace(",", "."))


    def get_currency_price(self):
        full_page = requests.get(self.DOLLAR_RUB, headers=self.headers)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        convert = soup.find_all("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
        return convert[0].text


    def check_currrency(self):
        currency = self.get_currency_price().replace(",", ".")
        print("Сейчас курс доллара: " + currency)

currency = Currency()
currency.check_currrency()
