import string
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pymorphy2


morph = pymorphy2.MorphAnalyzer()


#Функция для токенизации
def tokenize(text):
    word_tokens = word_tokenize(text)   #токенизация
    remove_punc = [ch for ch in word_tokens if ch not in string.punctuation]    #удаление знаков препинания
    remove_not_alfabet = [word.lower() for word in remove_punc if word.isalpha()]   #удаление символов не из алфавита
    russian_pattern = re.compile('[а-яА-ЯёЁ]+')
    remove_not_russian = [word for word in remove_not_alfabet if russian_pattern.match(word)]   #удаление нерусских слов
    stop_words = set(stopwords.words('russian'))    #стоп-слова для русского языка
    filtered_tokens = [word for word in remove_not_russian if word not in stop_words]   #удаление стоп-слов
    return filtered_tokens

#Функция для чтения файла
def read_file(name):
    file_name = f"texts/{name}.txt"
    file = open(file_name, "r", encoding="utf-8")
    return file.read()


#Функция для записи в файл
def write_tokens_in_file(tokens):
    with open(r"tokens.txt", "w", encoding="utf-8") as file:
        for token in tokens:
            file.write(token + '\n')
        print("Write tokens in file - successfully")

#Лемматизация
def lemmatize(tokens):
    res = {}    #Пустой словарь для лемм и токенов
    for token in tokens:
        p = morph.parse(token)[0]
        norm = p.normal_form       #Определение леммы
        if norm not in res:     #Запись леммы и ее токена
            res[norm] = []
            res[norm].append(token)
        else:
            res[norm].append(token)
    return res

#Функция для записи лемм и токенов
def write_lemmas_in_file(lemmas):
    with open("lemmas.txt", "w", encoding="utf-8") as file:
        for key, value in lemmas.items():
            values = ' '.join(value)
            file.write(f"{key}: {values}\n")
        print("Write lemmas in file - successfully")

def main():
    token_list = list()     #Пустой лист для добавления токенов
    for i in range(1, 103):     #Запускаем цикл для прохождения по всем файлам
        file = read_file(i)     #Чтение файла
        tokens = tokenize(file)     #Токенизация файла
        token_list += tokens    #Добавление токенов в лист
    unique_list = list(set(token_list))     #Удаление дубликатов
    write_tokens_in_file(unique_list)   #Запись токенов в файл
    write_lemmas_in_file(lemmatize(unique_list))     #Определение лемм, запись лемм и токенов в файл

if __name__ == "__main__":
    main()