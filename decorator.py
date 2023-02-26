# 1.
import os
import datetime

def logger(old_function):

    def new_function(*args, **kwargs):
        with open('main.log', 'a') as file:
            file.write(f'Вызвана функция {old_function} c аргументами, ')
            file.write(f'args: {args}; ')
            file.write(f'kwargs: {kwargs}; ')
            file.write(f'Начало работы: {datetime.datetime.now()}; ')
            value = old_function(*args, **kwargs)
            file.write(f'Возвращаемое значение: {value}.')

            return value

    return new_function


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()

    
    
# 2.
import os
import datetime

def logger(path):

    def __logger(old_function):
        def new_function(*args, **kwargs):
            with open(path, 'a') as file:
                file.write(f'Вызвана функция {old_function} c аргументами, ')
                file.write(f'args: {args}; ')
                file.write(f'kwargs: {kwargs}; ')
                file.write(f'Начало работы: {datetime.datetime.now()}; ')
                value = old_function(*args, **kwargs)
                file.write(f'Возвращаемое значение: {value}.')

                return value

        return new_function

    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()
    
# 3.
# применила к домашке по парсингу
import requests
from bs4 import BeautifulSoup
from web_ import logger

@logger
def search(key1='django', key2='flask'):
    url = f'https://spb.hh.ru/search/vacancy?text={key1}%2C+{key2}&salary=&area=1&area=2&ored_clusters=true'
    headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    vacancies = soup.findAll('div', class_='serp-item')
    data = []

    for vacancy in vacancies:
        link = vacancy.find('a', class_='serp-item__title').get('href')
        position = vacancy.find('a', class_='serp-item__title').text
        try:
            salary = vacancy.find('span', class_='bloko-header-section-3').text.replace("\u202f", " ").replace("\xa0", " ")
        except:
            salary = 'нет информации по зп вилке'
        company_name = vacancy.find('a', class_='bloko-link bloko-link_kind-tertiary').text.replace("\xa0", " ")
        location = vacancy.findAll('div', class_='bloko-text')[1].text.replace("\xa0", " ")

        data.append([link, position, salary, company_name, location])

    return data
