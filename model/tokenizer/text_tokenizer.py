from typing import List

import pandas
import nltk
from nltk import WordNetLemmatizer


class TextPreproccessor:

    df: pandas.DataFrame

    def __init__(self, df: pandas.DataFrame):
        self.df = df

    def __tokenize(self, text: str):
        sentences = nltk.sent_tokenize(text)
        tokenized_words = list()
        for sentence in sentences:
            words = nltk.word_tokenize(sentence)
            tokenized_words.append(words)

        return tokenized_words, sentences

    def __stop_words(self, words: List[str]) -> List[str]:
        stop_words = set(nltk.corpus.stopwords("english"))
        without_stopwords = [word for word in words if word not in stop_words]
        return without_stopwords

    def __lemmatize(self, words: List[str]) -> List[str]:
        lemmatizer = WordNetLemmatizer()
        lemmatized_words = []
        for word in words:
            lemmatized_words.append(lemmatizer.lemmatize(word))

        return lemmatized_words

    def __prepare_dataframe(self):
        self.df["Resume"] = self.df["Resume"].apply(self.__tokenize).apply(self.__stop_words).apply(self.__lemmatize)
        return self.df