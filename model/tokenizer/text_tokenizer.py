from typing import List

import pandas
import nltk
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords


class TextPreprocessor:

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

    def __stop_words(self, words):
        words = words.split()
        nltk.download('stopwords')
        stop_words = set(stopwords.words("english"))
        without_stopwords = " ".join([word for word in words if word not in stop_words])
        return without_stopwords

    def __lemmatize(self, words: List[str]) -> List[str]:
        lemmatizer = WordNetLemmatizer()
        lemmatized_words = []
        for word in words:
            lemmatized_words.append(lemmatizer.lemmatize(word))

        return lemmatized_words

    def prepare_dataframe(self):
        self.df["resume_text"] = self.df["resume_text"].apply(self.__stop_words)
        self.df["job_description_text"] = self.df["job_description_text"].apply(self.__stop_words)
        return self.df