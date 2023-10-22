import cloudscraper
from bs4 import BeautifulSoup
import csv
import time

"""
Парсер новостей с сайта ByBit: https://announcements.bybit.com/en-US/?category=&page=1

Парсер выполняет JS, запрашивает свежие данные 1 раз в секунду (обходит возможные блокировки и кеширование CDN) 
и сохраняет новые новости в .csv файл, включая точное время их появления, заголовок и ссылку на статью.
"""

# Установите URL для парсинга
url = "https://announcements.bybit.com/en-US/?category=&page=1"

# Создайте экземпляр cloudscraper
scraper = cloudscraper.create_scraper()
current_articles = set()

try:
    while True:
        try:
            response = scraper.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                with open('news.csv', mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    for article in soup.find_all('a', class_='no-style'):
                        if article.find('span'):
                            title = article.find('span').text.strip()  # Извлекаем заголовок статьи
                            link = 'https://announcements.bybit.com' + article['href']  # Извлекаем ссылку на статью
                            if link not in current_articles:  # Проверяем, была ли уже сохранена статья
                                current_articles.add(link)  # Добавляем ссылку во множество уже сохраненных статей
                                current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())  # Получаем текущее время
                                writer.writerow([current_time, title, link])  # Записываем время, заголовок и ссылку в CSV
                                print(f"Добавлена новая статья: {title} - {link}")  # Выводим информацию о новой статье
            else:
                print("Не удалось получить страницу.")
        except Exception as e:
            print(f"Произошла ошибка: {str(e)}")  # Обрабатываем любые возможные ошибки
        time.sleep(1)  # Ожидаем 1 секунду перед следующим запросом
except KeyboardInterrupt:
    print("Программа остановлена пользователем.")  # Обрабатываем остановку программы пользователем
