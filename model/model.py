import numpy as np
import pandas as pd
from simpletransformers.classification import ClassificationModel
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, classification_report
from data_preparator.dataset_preparator import DataPreparator
from tokenizer.text_tokenizer import TextPreprocessor

class SimpleModel:
    def __init__(self):
        self.model = ClassificationModel("roberta", "roberta-base",
                                            args={
                                                'overwrite_output_dir': True, "train_batch_size": 32,
                                                "save_steps": 10000, "save_model_every_epoch": False,
                                                'num_train_epochs': 5
                                            },)
        self.df = pd.concat([pd.read_csv("hf://datasets/cnamuangtoun/resume-job-description-fit/train.csv"),
                            pd.read_csv("hf://datasets/cnamuangtoun/resume-job-description-fit/test.csv")])

    def train_model(self):
        preprocessor = DataPreparator(self.df)
        text_preprocessor = TextPreprocessor(preprocessor.preprocess())
        prepared_data = text_preprocessor.prepare_dataframe()
        x_train, x_test, y_train, y_test = train_test_split(prepared_data.drop("label", axis=1),
                                                            prepared_data["label"], test_size=0.20,
                                                            stratify=prepared_data["label"], random_state=666)
        train_df = pd.DataFrame({0: x_train, 1: y_train})
        test_df = pd.DataFrame({0: x_test, 1: y_test})
        self.model.train_model(train_df)
        result, model_outputs, wrong_predictions = self.model.eval_model(test_df)
        preds = [np.argmax(tuple(m)) for m in model_outputs]
        print(f1_score(test_df[1], preds, average='micro'))
        print(f1_score(test_df[1], preds, average='macro'))
        print(classification_report(test_df[1], preds))

    def predict(self, *arg):
        result = self.model.predict(arg)
        return result


if __name__ == '__main__':
    model = SimpleModel()
    model.train_model()
