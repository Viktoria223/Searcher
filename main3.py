import string
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pymorphy2

morph = pymorphy2.MorphAnalyzer()


# Функция для токенизации
def tokenize(text):
    word_tokens = word_tokenize(text)  # токенизация
    remove_punc = [ch for ch in word_tokens if ch not in string.punctuation]  # удаление знаков препинания
    remove_not_alfabet = [word.lower() for word in remove_punc if word.isalpha()]  # удаление символов не из алфавита
    russian_pattern = re.compile('[а-яА-ЯёЁ]+')
    remove_not_russian = [word for word in remove_not_alfabet if russian_pattern.match(word)]  # удаление нерусских слов
    stop_words = set(stopwords.words('russian'))  # стоп-слова для русского языка
    filtered_tokens = [word for word in remove_not_russian if word not in stop_words]  # удаление стоп-слов
    return filtered_tokens


# Функция для чтения файла
def read_file(name):
    file_name = f"texts/{name}.txt"
    file = open(file_name, "r", encoding="utf-8")
    return file.read()


# Функция для записи в файл
def write_tokens_in_file(tokens):
    with open(r"tokens.txt", "w", encoding="utf-8") as file:
        for token in tokens:
            file.write(token + '\n')
        print("Write tokens in file - successfully")


# Лемматизация
def lemmatize(tokens):
    res = {}  # Пустой словарь для лемм и токенов
    lemmas = []
    for token in tokens:
        p = morph.parse(token)[0]
        norm = p.normal_form  # Определение леммы
        if norm not in lemmas:  # Запись леммы и ее токена
            lemmas.append(norm)
    return lemmas


# Функция для записи лемм и токенов
def write_lemmas_in_file(lemmas):
    with open("lemmas.txt", "w", encoding="utf-8") as file:
        for key, value in lemmas.items():
            values = ' '.join(value)
            file.write(f"{key}: {values}\n")
        print("Write lemmas in file - successfully")

def determining_the_indexes_of_lemmas(lemmas, i):
    indexes = {}
    for lemm in lemmas:
        if lemm not in indexes:
            indexes[lemm] = []
            indexes[lemm].append(i)
        else:
            indexes[lemm].append(i)
    return indexes

def search_indexes(request_user, indexes_list):
    res = {}
    i = 0
    while len(request_user) > 1:
        i += 1
        last_open_parenthesis = -1
        first_close_parenthesis = -1
        index_open_par = -1
        index_close_par = -1
        for char in request_user:
            index_open_par += 1
            if char == '(':
                last_open_parenthesis = index_open_par
                print(f"Последняя открытая скобка: {last_open_parenthesis}")
        for char in request_user:
            index_close_par += 1
            if (char == ')') and index_close_par > last_open_parenthesis:
                first_close_parenthesis = index_close_par
                print(f"Первая закрытая скобка: {first_close_parenthesis}")
                break

        if '(' not in request_user and ')' not in request_user:
            q = '(' + request_user + ')'
            request_user = q
            last_open_parenthesis = 0
            first_close_parenthesis = int(len(request_user)) - 1
        elif ('(' in request_user and ')' not in request_user) or ('(' not in request_user and ')' in request_user):
            return "Ошибка в последовательности скобок"
        last_open_parenthesis += 1
        work_request = request_user[last_open_parenthesis:first_close_parenthesis]
        list_req = work_request.split(' ')
        first_word = list_req[0]
        operator = list_req[1]
        second_word = list_req[2]
        print(first_word, second_word)
        if first_word not in indexes_list and first_word.isdigit() == False:
            return f"{first_word} not in pages"
        if second_word not in indexes_list and second_word.isdigit() == False:
            return f"{second_word} not in pages"
        first_set = list()
        second_set = list()
        three_set = list()
        general_list = list()

        for lemm in indexes_list:
            if not first_word.isdigit():
                if lemm == first_word:
                    add_values(lemm, first_set, indexes_list, general_list)

            if not second_word.isdigit():
                if lemm == second_word:
                    add_values(lemm, second_set, indexes_list, general_list)

        if first_word.isdigit():
            add_values(int(first_word), first_set, res, general_list)

        if second_word.isdigit():
            add_values(int(second_word), second_set, res, general_list)

        if operator == "OR":
            for word in second_set:
                if word not in first_set:
                    first_set.append(word)
            res[i] = first_set
        elif operator == "AND":
             for word in second_set:
                 if word in first_set:
                     three_set.append(word)
             res[i] = three_set
        elif operator == "NOT":
            for word in first_set:
                if word not in second_set:
                    three_set.append(word)
            res[i] = three_set

        check_NOT = request_user[last_open_parenthesis - 4:last_open_parenthesis - 1]
        minus = list()

        if check_NOT == "NOT":
            for word in general_list:
                if word not in res[i]:
                    minus.append(word)

            res[i] = minus

            prom_req = request_user[0:last_open_parenthesis - 4] + str(i) + request_user[first_close_parenthesis + 1:]
            request_user = prom_req
        else:
            prom_req = request_user[0:last_open_parenthesis-1] + str(i) + request_user[first_close_parenthesis + 1:]
            request_user = prom_req
        print(request_user)

    return res[len(res)]


def add_values(lemm, request_set, indexes_list, general_list):
    for word in indexes_list[lemm]:
        request_set.append(word)
        if word not in general_list:
            general_list.append(word)


def main():
    token_list = list()  # Пустой лист для добавления токенов
    tokens_in_file = {}
    lemmas_with_indexes = {}
    i_num = 1
    j_num = 103
    for i in range(i_num, j_num):  # Запускаем цикл для прохождения по всем файлам
        file = read_file(i)  # Чтение файла
        tokens = tokenize(file)  # Токенизация файла
        tokens_in_file[i] = tokens
    for i in range(i_num, j_num):
        tokens_in_file[i] = list(set(tokens_in_file[i]))
        tokens_in_file[i] = lemmatize(tokens_in_file[i])
    for i in range(i_num, j_num):
        lemm_work = determining_the_indexes_of_lemmas(tokens_in_file[i], i)
        for lemm in lemm_work:
            if lemm not in lemmas_with_indexes:
                lemmas_with_indexes[lemm] = []
                lemmas_with_indexes[lemm].append(lemm_work[lemm])
            else:
                lemmas_with_indexes[lemm].append(lemm_work[lemm])
    print(lemmas_with_indexes)
    request_user = input("Enter your request: ")
    answer = search_indexes(request_user, lemmas_with_indexes)
    print(f"Страницы, удовлетворяющие запросу: {answer}")

if __name__ == "__main__":
    main()

