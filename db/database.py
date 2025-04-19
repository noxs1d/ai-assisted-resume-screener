from typing import List, Union, Tuple
from dotenv import load_dotenv
import mysql.connector
import os

load_dotenv()
class DataBase:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host=os.getenv('DB_HOST'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD')
        )
        self.mycursor = self.mydb.cursor()

    def create_db(self, database_name):
        self.mycursor.execute("CREATE DATABASE " + database_name)

    def connect_db(self, name):
        self.mydb = mysql.connector.connect(
            host=os.getenv('DB_HOST'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), database=name
        )
        self.mycursor = self.mydb.cursor()
    def create_table(self, table_name, datas: Union[List, str]):
        if isinstance(datas, list):
            datas = ", ".join(datas)
        query = f"CREATE TABLE {table_name} ({datas});"
        print(query)
        self.mycursor.execute(query)

    def insert_data(self, table_name, datas: Union[List[Tuple], str], attributes: Union[List, str]):
        if isinstance(attributes, list):
            attributes = ", ".join(attributes)


        if isinstance(datas, list):
            if len(datas[0]) > 1:
                s = (len(datas[0]) - 1) * "%s, " + "%s"
            query = f"INSERT INTO {table_name} ({attributes}) VALUES (s)"
            self.mycursor.executemany(query, datas)
        else:
            datas = ", ".join([f"'{data}'" for data in datas.split(", ")])
            print(f"INSERT INTO {table_name} ({attributes}) VALUES ({datas})")
            self.mycursor.execute(f"INSERT INTO {table_name} ({attributes}) VALUES ({datas})")

        self.mydb.commit()


if __name__ == "__main__":
    print(os.getenv('DB_HOST'))
    db = DataBase()
    db.connect_db("resumeai")
    db.insert_data("candidates",  "1, Nurik, Urazbaev, ML-engineer, 7", "CandidateID, name, lastname, positon, rate")
