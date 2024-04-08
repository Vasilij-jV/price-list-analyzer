import csv
import os
from pprint import pprint


class PriceMachine:

    def __init__(self):
        self.data = []
        self.result = ''
        self.columns = []

    def load_prices(self, file_path):
        # Открываю по очереди файлы в списке файлов и итерируюсь по первой строке

        for price in file_path:
            with open(price, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for item in reader:
                    item.append(price)
                    self.columns.append(self._search_product_price_weight(item))
                    break

    def _search_product_price_weight(self, row):
        # Получаю в параметры первую строку файла и создаю списки из трёх позиций заданных столбцов
        # Добавляю в конец каждого списка название файла к которому относятся столбцы в списке
        column_store = []
        for elem in row:
            if elem == 'наименование' or elem == 'продукт' or elem == 'название' or elem == 'товар':
                column_store.insert(0, row.index(elem))
            elif elem == 'розница' or elem == 'цена':
                column_store.insert(1, row.index(elem))
            elif elem == 'вес' or elem == 'масса' or elem == 'фасовка':
                column_store.insert(2, row.index(elem))
            elif elem == row[-1]:
                column_store.append(elem)
        return column_store

    def export_to_html(self, fname):
        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table>
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''
        # Создаю разметку
        for number, item in enumerate(self.data):
            number_product = number + 1
            product_name, price, weight, file_name, price_per_kilo = item
            result += (f'<tr><td>{number_product};</td><td>{product_name};</td><td>{price};</td'
                       f'><td>{weight};</td><td>{file_name};</td><td>{price_per_kilo};</td></tr>\n')
            if number_product == len(self.data):
                result += '<table>'

        with open(fname, mode='w', encoding='utf-8') as htmlf:
            htmlf.write(result)

    def find_text(self, text):
        if text == 'exit':
            print('Работа закончена')
        # Обхожу список с номерами столбцов и создаю строки, которые буду использовать в html коде
        for file_path in self.columns:
            one_file = file_path[-1]
            with open(one_file, mode='r', encoding='utf-8') as ff:
                reader = csv.reader(ff)
                for sub_str in reader:
                    str_title = sub_str[file_path[0]]
                    if text in str_title:
                        selected_elem = [sub_str[file_path[0]], sub_str[file_path[1]], sub_str[file_path[2]],
                                         file_path[3]]
                        price_per_kilo = int(sub_str[file_path[1]]) / int(sub_str[file_path[2]])
                        selected_elem.append(round(price_per_kilo, 1))
                        self.data.append(selected_elem)

        # Сортирую по стоимости за килограмм
        was_swap = True
        while was_swap:
            was_swap = False
            for i in range(len(self.data) - 1):
                if self.data[i][4] > self.data[i + 1][4]:
                    self.data[i][4], self.data[i + 1][4] = self.data[i + 1][4], self.data[i][4]
                    was_swap = True


# Из текущего каталога получаю список файлов
list_prices = []
current_directory = os.getcwd()
list_all_files = os.listdir(current_directory)
for file in list_all_files:
    if file.startswith('price_'):
        list_prices.append(file)

# Создаю экземпляр класса
pm = PriceMachine()
pm.load_prices(file_path=list_prices)

text = input()
pm.find_text(text)
pm.export_to_html(fname='output.html')
