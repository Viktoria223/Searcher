import requests
from bs4 import BeautifulSoup

# Функция для обработки ссылок
def process_link(link):
    response = requests.get(link)
    full_text = ""  # Переменная для хранения всего текста страницы
    # Проверка успешности запроса
    if response.status_code == 200:
        # Создаем объект BeautifulSoup для парсинга HTML-кода страницы
        soup = BeautifulSoup(response.content, 'html.parser')

        # Находим все теги <p>, содержащие текстовый контент
        paragraphs = soup.find_all('p')

        # Перебираем найденные абзацы и записываем их в переменную full_text
        for paragraph in paragraphs:
            full_text += paragraph.text + "\n"
    else:
        # Если запрос не удалось выполнить, выводим сообщение об ошибке
        print('Ошибка при выполнении GET-запроса.')

    return full_text

# Функция для сохранения результата в файл с указанным номером
def save_result(result, file_number):
    file_name = f"texts\{file_number}.txt"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(result)

def main():
    # Открываем файл с ссылками и читаем их
    with open("links.txt", "r", encoding="utf-8") as file:
        links = file.read().splitlines()

    # Проходимся по каждой ссылке и обрабатываем ее
    for i, link in enumerate(links, start=1):
        result = process_link(link)  # Обрабатываем ссылку
        save_result(result, i)  # Сохраняем результат в файл
        print(f"Ссылка {link} обработана. Результат сохранен в файл {i}.txt")

if __name__ == "__main__":
    main()

