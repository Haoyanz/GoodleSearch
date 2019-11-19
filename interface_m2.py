from nltk import PorterStemmer


def read_file_to_tf_idf_score():
    '''
    read tf-idf.txt and import data to tf_idf_scores
    :return: None
    '''
    filename = "short_tf_idf.txt"
    f = open(filename, "r")

    line = f.readline()
    line = f.readline()[:-1]
    scores = {}
    document = 1
    while line:
        line = line[:-1]
        if "Document:" in line:
            tf_idf_scores.append(scores)
            scores.clear()
            line = f.readline()[:-1]
            while "Document:" in line:  # in case empty document
                line = f.readline()[:-1]
                document += 1
        temp = line.split(" ")
        term = temp[0]
        score = float(temp[1])
        scores[term] = score
        line = f.readline()
    tf_idf_scores.append(scores)


def read_file_to_url_id():
    '''
    read url_id.txt and import data to url_id
    :return:
    '''
    with open("url_id.txt", 'r') as f:
        for line in f:
            tokens = line.split()
            url_id[tokens[0]] = tokens[1]


def get_idf_scores(token: str):
    '''

    :param token: term
    :return: a dictionary by score {id: score}
    '''
    token_scores = {}
    doc_id = 1
    for doc in tf_idf_scores:
        if token in doc.keys():
            token_scores[doc_id] = float(doc[token])
        doc_id += 1
    return token_scores


def get_query():
    ps = PorterStemmer()
    query_list = []
    query = input("******************** Qīαη Dμ ********************\n").split()
    for term in query:
        ps.stem(term)
        query_list.append(term)
    return query_list

def get_url_from_doc_id(id: int):
    '''

    :param id: document id
    :return: url correspond
    '''


def get_page_total_score(scores: [dict]):
    '''

    :param scores: list of scores
    :return:
    '''

tf_idf_scores = []  # [dict{}], index + 1 = document id
url_id = {}

if __name__ == "__main__":
    read_file_to_tf_idf_score()

    print(get_idf_scores("ics"))
