from nltk import PorterStemmer
import Indexing

def read_file_to_tf_idf_score():
    '''
    read tf-idf.txt and import data to tf_idf_scores
    :return: None
    '''
    # filename = "short_tf_idf.txt"
    filename = "tf-dif.txt"
    f = open(filename, "r")

    line = f.readline()
    line = f.readline()[:-1]
    scores = {}
    document = 0
    while line:
        if "Document:" in line:
            document += 1
            tf_idf_scores[document] = scores
            scores = {}
            line = f.readline()[:-1]
            while "Document:" in line:  # in case empty document
                line = f.readline()[:-1]
                document += 1
        temp = line.split(" ")
        term = temp[0]
        score = float(temp[1])
        scores[term] = score
        line = f.readline()[:-1]
    tf_idf_scores[document][term] = scores


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
    for id, scores in tf_idf_scores.items():
        for key, value in scores.items():
            if token == key:
                token_scores[id] = float(value)
    return token_scores


def get_query():

    query = input("******************** Qīαη Dμ Search Engine ********************\n").split()
    return Indexing.porter_stem(query)


def get_url_from_doc_id(id: int):
    '''

    :param id: document id
    :return: url correspond
    '''
    return url_id[str(id)]

tf_idf_scores = {}  # {dict{}}
url_id = {}

if __name__ == "__main__":

    read_file_to_tf_idf_score()
    # print(type(tf_idf_scores[1]))
    read_file_to_url_id()

    while True:
        query_list = get_query()
        # print("query_list: ", query_list)
        scores = {}
        for term in query_list:
            tempDict = get_idf_scores(term)
            for key, value in tempDict.items():
                if key in scores.keys():
                    scores[key] += value
                else:
                    scores[key] = value
        sorted_scores_items = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
        url_ids = []
        for items in sorted_scores_items:
            url_ids.append(items[0])
            # print(items[0], items[1])
        urls = []
        for id in url_ids:
            urls.append(get_url_from_doc_id(id))
        if len(urls) <= 5:
            for url in urls:
                print(url)
        else:
            for i in range(5):
                print(urls[i])



