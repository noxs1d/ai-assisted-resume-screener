import re
import string
import pandas as pd

class DataPreparator:

    df: pd.DataFrame

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def preprocess(self):
        self.df["resume_text"] = self.df["resume_text"].apply(lambda x: self.__clean_text(x))
        self.df["job_description_text"] = self.df["job_description_text"].apply(lambda x: self.__clean_text(x))
        return self.df

    def __clean_text(self, text: str) -> str:
        text = re.sub(r'http\S+', ' ', text)
        text = re.sub(r'@\S+', ' ', text)
        text = re.sub(r'RT|cc', ' ', text)
        text = re.sub(r'#\S+', ' ', text)
        text = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        text = text.lower()
        return text
