from keybert import KeyBERT
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer


model = SentenceTransformer('bert-base-nli-mean-tokens')


# calculating the semantic similarity between the two sentences
# org_answer is the answer in the database
# candidate_answer is the answer given by candidate
def semantic_score(org_answer, candidate_answer):
    answers = list()
    answers.append(org_answer)
    answers.append(candidate_answer)
    embeddings = model.encode(answers)
    return cosine_similarity(
        [embeddings[0]],
        embeddings[1:]
    )


# function for generating the keywords
# words that are in the question are removed from the list of keywords
def keyword_gen(ans, ques, ans_size):
    # question is the question asked
    # making a list of the words in the question
    words = []
    words = ques.split()
    kw_model = KeyBERT()
    n = max(int(ans_size/3), 12)
    n = min(n, 25)
    keywords = kw_model.extract_keywords(ans, top_n=n)
    keys = []

    for i in range(0, len(keywords)):
        keys.append(keywords[i][0])
    pos = []
    for i in range(0, len(keys)):
        if keys[i] in words:
            pos.append(i)
    for i in range(0, len(pos)):
        keywords.remove(keywords[pos[i] - i])
    return keywords


# function for calculating the keyword score and final score
def final_score(keywords_org, keywords_candidate):
    keys_org = []
    keys_cand = []
    for i in range(0, len(keywords_org)):
        keys_org.append(keywords_org[i][0])
    for i in range(0, len(keywords_candidate)):
        keys_cand.append(keywords_candidate[i][0])
    fin_score = 0.0
    for i in range(0, len(keys_cand)):
        if keys_cand[i] in keys_org:
            fin_score = fin_score + 100 / len(keys_org)
    return fin_score


repo = "roberta-large-mnli"


def compare_answer(question, org_ans, cand_ans):
    question = question.lower()
    org_ans, cand_ans = org_ans.lower(), cand_ans.lower()

    # counting the number of words in the org and candidate answer
    count_words_org = len(org_ans.split())
    count_words_cand = len(cand_ans.split())

    sem_score = semantic_score(org_ans, cand_ans)
    ss = sem_score[0][0]
    keywords_org = keyword_gen(org_ans, question, count_words_org)
    keywords_candidate = keyword_gen(cand_ans, question, count_words_org)
    score = final_score(keywords_org, keywords_candidate)
    s_s = (ss * 180) + score

    return (s_s*100)/280

