import re
import string

import pandas as pd

class DataPreparator:

    df: pd.DataFrame

    def __init__(self, data_path: str):
        self.df = pd.read_csv(data_path)

    def __preprocess(self):
        self.df["Resume"] = self.df["Resume"].apply(lambda x: self.__clean_text(x))
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
