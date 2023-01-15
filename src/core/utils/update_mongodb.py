from pymongo import MongoClient
import pandas as pd


client = MongoClient("mongodb://127.0.0.1:27017/")

qa_bank = {'Question': {0: 'what is artificial intelligence',
  1: 'what is machine learning',
  2: 'what is a search engine'
  },
  'Answer': {0: 'Artificial intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think and act like humans. These intelligent machines can be trained to perform a variety of tasks, such as recognizing patterns, learning from experience, making decisions, and adapting to new situations.',
  1: 'Machine learning is a type of artificial intelligence that allows software applications to become more accurate in predicting outcomes without being explicitly programmed. The basic idea behind machine learning is to build algorithms that can receive input data and use statistical analysis to predict an output value within an acceptable range.',
  2: 'A search engine is a software program that searches a database of Internet sites, such as Google or Bing, for keywords and returns a list of websites that are relevant to the search.'
  }}

df_qa = pd.DataFrame(qa_bank)
db = client["answer_scoring"]
db.list_collection_names()
col = db['questions']
for i, row in df_qa.iterrows():
    question = {'Question' : row.Question, 'Answer' : row.Answer}
    col.insert_one(question)
