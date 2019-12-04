import re
from nltk.stem import PorterStemmer



def porter_stem(content):
    ps = PorterStemmer()
    content = (str(content)).lower()
    words = []
    words.extend(re.findall("[a-z0-9]+", content))
    for i, word in enumerate(words):
        words[i] = ps.stem(word)
    return words


def get_tf_idfs(line):
    items = line
    to_return = []
    for item in items[1:]:
        temp = item.split(":")
        to_return.append((int(temp[0]), float(temp[1])))
    return to_return


def get_query():
    query = input("******************** Qīαη Dμ Search Engine ********************\n").split()
    return porter_stem(query)



url_id = {}
with open("id_url.txt", 'r') as f:
    for line in f:
        tokens = line.split()
        url_id[tokens[0]] = tokens[1]

while True:
    query_list = get_query()

    scores = {}
    for term in query_list:
        filename = ""
        if term[0] <= 'b':
            filename = "token_tfidf1.txt"
        elif term[0] <= 'n':
            filename = "token_tfidf2.txt"
        else:
            filename = "token_tfidf3.txt"
        with open(filename, "r") as f:
            for line in f:
                l = line.split()
                if l[0] == term:
                    tfidfs = get_tf_idfs(l)
                    for t in tfidfs:
                        if t[0] in scores.keys():
                            scores[t[0]] += t[1]
                        else:
                            scores[t[0]] = t[1]
    sorted_scores_items = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    result_url_ids = []
    for items in sorted_scores_items:
        result_url_ids.append(items[0])
    urls = []
    for id in result_url_ids:
        result_url = url_id[str(id)]
        urls.append(result_url)
    url_set = set()
    urls_to_print = []
    for url in urls:
        if url not in url_set:
            print(url)
            urls_to_print.append(url)
            url_set.add(url)
        if len(urls_to_print) == 5:
            break


