import sys
from stanfordcorenlp import StanfordCoreNLP
from collections import defaultdict

def put_pos_and_ner(query):
    nlp_tags = defaultdict()
    nlp = StanfordCoreNLP(r'stanford-corenlp-full-2018-02-27')
    nlp_tags['pos'] = nlp.pos_tag(query)
    nlp_tags['ne'] = nlp.ner(query)
    nlp.close()

    return nlp_tags

if __name__ == '__main__':
    print(put_pos_and_ner(sys.argv[1]))