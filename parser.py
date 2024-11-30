import requests
from bs4 import BeautifulSoup
from time import sleep
import xlsxwriter
import sqlite3

headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36", "Accept-Language": "en-US,en;q=0.9" }

def get_quotes():
    for page in range(1, 4):
        print(f"Page: {page}")
        url = f'https://quotes.toscrape.com/page/{page}/'
        response = requests.get(url, headers=headers)
        sleep(3)
        soup = BeautifulSoup(response.text, 'lxml')
        data = soup.find_all('div', class_='quote')

        counter = 0
        for i in data:
            author = str.strip(i.find('small', class_='author').text)
            text = str.strip(i.find('span', class_='text').text)
            counter = counter + 1

            print(f"Quote №{counter}. Text: {text}, Author: {author}\n\n")

            yield author, text

def write_to_excel(param):
    print("----------WRITING DATA TO XLSX----------")
    book = xlsxwriter.Workbook('quotes.xlsx')
    page = book.add_worksheet('quotes')

    row=0
    column=0

    page.set_column("A:A", 20)
    page.set_column("B:B", 400)

    for item in param():
        page.write(row, column, item[0])
        page.write(row, column+1, item[1])
        row+=1

    print("\n\nData about quotes successfully written to file quotes.xlsx")

    book.close()

def write_to_db(param):
    print("----------WRITING DATA TO DB----------")
    connection = sqlite3.connect('quotes.db')
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS quotes
                  (id INTEGER PRIMARY KEY, author TEXT, text TEXT)''')
    cursor.executemany('INSERT INTO quotes (author, text) VALUES (?, ?)', param())

    connection.commit()

    print("Data about quotes successfully written to DB quotes.db")

    connection.close()