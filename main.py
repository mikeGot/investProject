import requests
from bs4 import BeautifulSoup
import sqlite3


def connect_database(_ticker) -> float:
    conn = sqlite3.connect("mydatabase.db")
    # conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    sql = "SELECT price FROM stocks WHERE ticker = '" + _ticker + "'"
    #improve query
    cursor.execute(sql)
    p = cursor.fetchall()[0][0]
    return p


def update_sqlite_table(_ticker, _current_price):
    try:
        sqlite_connection = sqlite3.connect('mydatabase.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sql_update_query = "UPDATE stocks SET current_price =" + str(_current_price) +" WHERE ticker ='" + _ticker + "'"
        cursor.execute(sql_update_query)
        sqlite_connection.commit()
        print("Запись успешно обновлена")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")




class Currency:
    DOLLAR_RUB = 'https://www.google.ru/search?q=%D0%BA%D1%83%D1%80%D1%81+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0&newwindow=1&client=safari&channel=mac_bm&source=hp&ei=6a0nYeLxCYzy-QbTj7WoAQ&iflsig=AINFCbYAAAAAYSe7-WKeDsP6k2hm8vV1CJgpukS8OPQZ&oq=%D0%BA%D1%83%D1%80%D1%81+&gs_lcp=Cgdnd3Mtd2l6EAEYADINCAAQgAQQsQMQRhCCAjIICAAQgAQQsQMyCAgAEIAEELEDMggIABCABBCxAzILCAAQgAQQsQMQgwEyBQgAEIAEMgUIABCABDIFCAAQgAQyCAgAEIAEELEDMgUIABCABDoXCAAQgAQQsQMQxwEQ0QMQiwMQqAMQ0gM6GggAEIAEELEDEIMBEMcBEKMCEIsDEKgDEKcDUJ0bWKofYKcxaAFwAHgAgAHTAYgBrQWSAQUwLjQuMZgBAKABAbABALgBAg&sclient=gws-wiz'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15'}

    current_converted_price = 0

    def __init__(self):
        self.current_converted_price = float(self.get_currency_price().replace(",", "."))


    def get_currency_price(self):
        full_page = requests.get(self.DOLLAR_RUB, headers=self.headers)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        convert = soup.find_all("span", {"class": "DFlfde", "data-precision": 2})

        return convert[0].text


    def check_currrency(self):
        currency = self.get_currency_price().replace(",", ".")
        print("Сейчас курс доллара: " + currency)


#currency = Currency()
#currency.check_currrency()

class Stocks:
    ticker = ""
    price = 0
    name = ""
    quantity = 0
    commission = 0
    purchase_date = ""

    def __init__(self):
        self.ticker = "gazp"
        self.price = connect_database("gazp")
        self.quantity = 10

    def total_purchase_value(self, price, quantity):
        return float(price) * float(quantity)


class main_invest:
    #S = Stocks()


    def __init__(self, ticker):
        self.ticker = ticker
        self.price = connect_database(self.ticker)




    def get_currency_price(self):
        url = "https://bcs-express.ru/kotirovki-i-grafiki/" + self.ticker
        headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Safari/605.1.15'}

        full_page = requests.get(url, headers=headers)

        soup = BeautifulSoup(full_page.content, 'html.parser')
        convert = soup.find("div", {"class": "quote-head__price-value"})
        return convert.get_text()


    def check_currrency(self):
        currency = self.get_currency_price().replace(",", ".")
        print("Сейчас стоимость акции: " + currency)
        update_sqlite_table(self.ticker, currency)
        print("Цена покупки: " + str(self.price))



def update_all_current_prices():
    sqlite_connection = sqlite3.connect('mydatabase.db')
    cursor = sqlite_connection.cursor()
    print("Подключен к SQLite")

    sql_update_query = "SELECT ticker FROM stocks"
    cursor.execute(sql_update_query)
    p = cursor.fetchall()
    sqlite_connection.commit()
    cursor.close()

    for i in p:
        print(i[0])
        currency = main_invest(i[0])
        currency.check_currrency()
    print("Data is updated")


update_all_current_prices()


