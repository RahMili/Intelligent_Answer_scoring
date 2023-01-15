from pymongo import MongoClient
import pandas as pd
import ast
from src.config import basic_config
from src.logger import get_logger

logger = get_logger(__name__)


class SetupMongo():

    def __init__(self):
        self.client = MongoClient("mongodb://127.0.0.1:27017/")
        self.db_name = 'answer_scoring'
        self.quest_col = 'questions'


    def load_questions(self, question_doc):

        df_qa = pd.read_csv(question_doc)

        db = self.client[self.db_name]
        col = db[self.quest_col]

        for i, row in df_qa.iterrows():
            question = {'Question': row.Question, 'Answer': row.Answer}
            col.insert_one(question)

        logger.info('Questions stored successfully')


if __name__ == "__main__":
    mongo = SetupMongo()
    mongo.load_questions('qabank.csv')
