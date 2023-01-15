import sys
from nltk.stem import WordNetLemmatizer
from src.core.utils.pdf_read_util import read_native_pdf
from src.core.utils.mongo_util import connect_collection
from src.core.utils.scoring_util import *
import pandas as pd


def preprocess_text(text):
    text = text.lower()
    # list of special characters that needs to be removed from the answer
    spec_chars = ["!", '"', "#", "%", "&", "'", "(", ")", "*", "+", ",", "-", "/", ":", ";", "<", "=", ">",
                  "@", "[", "\\", "]", "^", "_", ",", "\r", "`", "{", "|", "}", "~", "–"]
    # replacing the special characters with whitespaces
    for char in spec_chars:
        text = text.replace(char, ' ')

    lemmatizer = WordNetLemmatizer()
    text = " ".join([lemmatizer.lemmatize(word) for word in text.split()])

    text = "".join([i for i in text])
    return text


# reading filename from the command line
file_path = sys.argv[1]
# sending filename to utility method
read_sheet = read_native_pdf(file_path)
page_wise_text_list = [" ".join(page) for page in read_sheet.values()]
sheet_text = " ".join([preprocess_text(x) for x in page_wise_text_list])

questions = []
cand_answers = []
qna = sheet_text.split("?")
qnaa = []
for x in qna:
    q = x.split("q.")
    if len(q) >= 2:
        for j in q:
            qnaa.append(j)
    else:
        qnaa.append(x)

for i in range(1, len(qnaa), 2):
    questions.append(qnaa[i])
    cand_answers.append(qnaa[i+1])

db_name = 'answer_scoring'
question_colm = 'questions'
db, col = connect_collection(db_name, question_colm)
for i in range(len(questions)):
    quesdf = pd.DataFrame(col.find({'Question': questions[i]}))
    for j, row in quesdf.iterrows():
        ques = row.Question
        ans = row.Answer
        print("\nQuestion: ", ques, "\nAnswer: ", ans, "\nCandidates answer: ", cand_answers[i])
        score = compare_answer(questions[i], ans, cand_answers[i])
        print("\nscore of "+str(i)+"th answer is ", score)



