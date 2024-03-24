import string
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pymorphy2
import math

morph = pymorphy2.MorphAnalyzer()


# Функция для токенизации
def tokenize(text):
    word_tokens = word_tokenize(text)  # токенизация
    remove_punc = [ch for ch in word_tokens if ch not in string.punctuation]  # удаление знаков препинания

    russian_pattern = re.compile('[а-яА-ЯёЁ]+')
    remove_not_russian = [word for word in remove_punc if russian_pattern.match(word)]  # удаление нерусских слов
    stop_words = set(stopwords.words('russian'))  # стоп-слова для русского языка
    filtered_tokens = [word for word in remove_not_russian if word not in stop_words]  # удаление стоп-слов
    remove_not_alfabet = [word.lower() for word in filtered_tokens if word.isalpha()]  # удаление символов не из алфавита
    return remove_not_alfabet


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
    lemmas = []
    for token in tokens:
        p = morph.parse(token)[0]
        norm = p.normal_form  # Определение леммы
        if norm not in lemmas:  # Запись леммы и ее токена
            lemmas.append(norm)
    return lemmas

# Функция для поиска количества лемм в файле
def lemmatize_count(tokens):
    lemmas = []
    count_lemmas = {}
    for token in tokens:
        p = morph.parse(token)[0]
        norm = p.normal_form  # Определение леммы
        if norm not in lemmas:  # Запись леммы и ее токена
            lemmas.append(norm)
            count_lemmas[norm] = 1
        else:
            count_lemmas[norm] = count_lemmas[norm] + 1
    return count_lemmas

# Функция для индексации
def determining_the_indexes_of_lemmas(lemmas, i):
    indexes = {}
    for lemm in lemmas:
        if lemm not in indexes:
            indexes[lemm] = []
            indexes[lemm].append(i)
        else:
            indexes[lemm].append(i)
    return indexes

# Поиск tf, idf для токенов
def search_tf_idf_tokens(text, tokens, tokens_with_indexes, j, i):
    count_tokens = {}
    for token in tokens:
        if token in count_tokens:
            count_tokens[token] = count_tokens[token] + 1
        else:
            count_tokens[token] = 1
    tf = {}
    for token in count_tokens:
        tf[token] = count_tokens[token] / text
    idf = {}
    count_index = count_indexes(tokens_with_indexes, i)
    for token in count_index:
        idf[token] = math.log10(j / count_index[token])
    return tf, idf

# Поиск tf, idf для лемм
def search_tf_idf_lemmas(text, tokens, tokens_with_indexes, j, i):
    tf = {}
    for token in tokens_with_indexes:
        tf[token] = tokens_with_indexes[token] / text
    idf = {}
    count_index = count_indexes(tokens, i)
    for token in tokens_with_indexes:
        idf[token] = math.log10(j / count_index[token])
    return tf, idf

# Подсчет количества файлов с определенной леммой или токеном
def count_indexes(list_with_indexes, i):
    count_indexes = {}
    for word in list_with_indexes:
        flat_list = [item for sublist in list_with_indexes[word] for item in sublist]
        if i in flat_list:
            count_indexes[word] = len(list_with_indexes[word])
    return count_indexes

def main():
    lemmas_list = {}
    tokens_in_file = {}
    lemmas_with_indexes = {}
    tokens_with_indexes = {}
    count_ind_lemmas = {}
    tokens = {}
    i_num = 1
    j_num = 103
    count_files = j_num - i_num
    for i in range(i_num, j_num):  # Запускаем цикл для прохождения по всем файлам
        file = read_file(i)  # Чтение файла
        tokens[i] = tokenize(file)  # Токенизация файла
        tokens_in_file[i] = tokens[i]
    for i in range(i_num, j_num):   # Лемматизация токенов
        count_ind_lemmas[i] = lemmatize_count(tokens_in_file[i])
        tokens_in_file[i] = list(set(tokens_in_file[i]))
        lemmas_list[i] = lemmatize(tokens_in_file[i])
    for i in range(i_num, j_num):   # Индексация токенов и лемм
        lemm_work = determining_the_indexes_of_lemmas(lemmas_list[i], i)
        token_work = determining_the_indexes_of_lemmas(tokens_in_file[i], i)
        for lemm in lemm_work:
            if lemm not in lemmas_with_indexes:
                lemmas_with_indexes[lemm] = []
                lemmas_with_indexes[lemm].append(lemm_work[lemm])
            else:
                lemmas_with_indexes[lemm].append(lemm_work[lemm])
        for token in token_work:
            if token not in tokens_with_indexes:
                tokens_with_indexes[token] = []
                tokens_with_indexes[token].append(token_work[token])
            else:
                tokens_with_indexes[token].append(token_work[token])

    for i in range(i_num, j_num):   # Поиск tf, idf
        tf_tokens, idf_tokens = search_tf_idf_tokens(len(tokens[i]), tokens[i], tokens_with_indexes, count_files, i)
        tf_lemmas, idf_lemmas = search_tf_idf_lemmas(len(tokens[i]), lemmas_with_indexes, count_ind_lemmas[i], count_files, i)
        with open(f"tokens_idf_tfidf/{i}.txt", "w", encoding="utf-8") as file:  # Запись в файл
            for key, value in idf_tokens.items():
                file.write(f"{key}: {value} {tf_tokens[key] * value}\n")
        with open(f"lemmas_idf_tfidf/{i}.txt", "w", encoding="utf-8") as file:  # Запись в файл
            for key, value in idf_lemmas.items():
                file.write(f"{key}: {value} {tf_lemmas[key] * value}\n")
        tf_tokens.clear()
        tf_lemmas.clear()
        idf_tokens.clear()
        idf_lemmas.clear()

if __name__ == "__main__":
    main()

