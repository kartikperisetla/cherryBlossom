import sys, nltk
from stanfordcorenlp import StanfordCoreNLP
from collections import defaultdict

def get_pos_and_ner_using_corenlp(query):
    nlp_tags = defaultdict()
    nlp = StanfordCoreNLP(r'stanford-corenlp-full-2018-02-27')
    nlp_tags['pos'] = nlp.pos_tag(query)
    nlp_tags['ne'] = nlp.ner(query)
    nlp.close()

    return nlp_tags

def get_pos_and_ner_using_nltk(query):
    nlp_tags = defaultdict()
    word_tokens = nltk.word_tokenize(query)
    nlp_tags['pos'] = nltk.pos_tag(word_tokens)
    nlp_tags['ne'] = nltk.ne_chunk(word_tokens)

    return nlp_tags

if __name__ == '__main__':
    print(get_pos_and_ner_using_nltk(sys.argv[1]))