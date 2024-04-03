import math
import numpy as np
import pymorphy2
from nltk.corpus import stopwords

morph = pymorphy2.MorphAnalyzer()
stop_words = stopwords.words("russian")

# Создаем словарь tf_idf лемм
def create_tfidf_docs_dict(n_docs):
    tfidf_dict = {}
    for i in range(1, n_docs):
        u = {}
        with open(f"lemmas_idf_tfidf/{i}.txt", 'r', encoding='utf-8') as file:
            lemmas = file.read().splitlines()
            for lemm in lemmas:
                lemm = lemm.replace(":", "")
                lemm = lemm.split(" ")
                if lemm[0] not in u:
                    u[lemm[0]] = float(lemm[2])
        tfidf_dict[i] = u
    return tfidf_dict


# Находим tf запроса
def search_tf(query):
    words = query.split()
    words = [word for word in words if word not in stop_words]
    word_counts = {}
    for word in words:
        word = morph.parse(word)[0].normal_form
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1
    len_words = len(words)
    tf = {}
    for word, count in word_counts.items():
        tf[word] = count / len_words
    return tf


# Находим idf запроса
def search_idf(token_counts, query, n_docs):
    tokens = query.split()
    tokens = [token for token in tokens if token not in stop_words]
    lemmas = []
    for token in tokens:
        lemmas.append(morph.parse(token)[0].normal_form)
    idf_data = {}
    for token, count in token_counts.items():
        if token in lemmas:
            idf_data[token] = math.log(n_docs / token_counts[token])
    return idf_data


# Находим tf-idf запроса
def search_tf_idf(tf, idf):
    tf_idf = {}
    for lemma, res in tf.items():
        tf_idf[lemma] = tf[lemma] * idf[lemma]
    return tf_idf


def inverted_index_count(file):
    token_numbers = {}
    for line in file:
        token, number = line.strip().split(': ')
        numbers = [int(num) for num in number.split(' ')]
        token_numbers[token] = len(numbers)
    return token_numbers


# Определение косинусного сходства
def cosine_similarity(vec1, vec2):
    general_words = set(vec1.keys()).union(set(vec2.keys()))
    v1 = np.array([vec1.get(k, 0) for k in general_words])
    v2 = np.array([vec2.get(k, 0) for k in general_words])
    dot = np.dot(v1, v2)
    norm_vec1 = np.linalg.norm(v1)
    norm_vec2 = np.linalg.norm(v2)
    return dot / (norm_vec1 * norm_vec2) if norm_vec1 * norm_vec2 != 0 else 0

# Векторный поиск
def vector_search(tf_idf_query, tfidf_docs_dict):
    scores = {}
    for key, value in tfidf_docs_dict.items():
        score = cosine_similarity(tf_idf_query, value)
        if score > 0:
            scores[key] = score
    return sorted(scores.items(), key=lambda item: item[1], reverse=True)

def main():
    n_docs = 103
    tf_idf_docs_dict = create_tfidf_docs_dict(n_docs)
    with open("indexes.txt", 'r', encoding='utf-8') as file:
        tokens_count_by_pages = inverted_index_count(file)
    query = input("Введите запрос: ")
    if query.lower() == 'exit':
        exit()
    tf_query = search_tf(query)
    idf_query = search_idf(tokens_count_by_pages, query, n_docs)
    tf_idf_query = search_tf_idf(tf_query, idf_query)
    search_results = vector_search(tf_idf_query, tf_idf_docs_dict)
    for value in search_results:
        print(f"{value[0]} : {value[1]}")

if __name__ == "__main__":
    main()


