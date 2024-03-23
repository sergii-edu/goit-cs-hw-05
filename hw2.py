import string
import requests
from collections import defaultdict
import matplotlib.pyplot as plt


def get_text(url):
    try:
        return requests.get(url).text
    except requests.RequestException:
        return None


def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))


def map_function(word):
    return word, 1


def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()


def reduce_function(key_values):
    return key_values[0], sum(key_values[1])


def map_reduce(text):
    text = remove_punctuation(text)
    words = text.split()
    mapped_values = map(map_function, words)
    shuffled_values = shuffle_function(mapped_values)
    reduced_values = map(reduce_function, shuffled_values)
    return dict(reduced_values)


def visualize_top_words(word_counts, n=10):
    sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[
        :n
    ]
    top_words, top_counts = zip(*sorted_word_counts)
    plt.figure(figsize=(10, 6))
    plt.barh(top_words, top_counts, color="skyblue")
    plt.xlabel("Frequency")
    plt.ylabel("Words")
    plt.title(f"Top {n} Words")
    plt.gca().invert_yaxis()
    plt.show()


if __name__ == "__main__":
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    text = get_text(url)
    if text:
        word_counts = map_reduce(text)
        visualize_top_words(word_counts)
