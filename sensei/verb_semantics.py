from conceptnet_client import ConceptnetClient, Relationship
from stanfordcorenlp import StanfordCoreNLP
import nltk, re

class VerbSemantics:
    def __init__(self):
        self.filters = {(Relationship.UsedFor.value, True): (),      # dancing is used for fun, exercise, ...
                        (Relationship.UsedFor.value, False): (),     # things used for dancing: disco, dance club, party, ...
                        (Relationship.Causes.value, True): (),       # dancing causes fatigue, happiness, ...
                        (Relationship.HasSubevent.value, True): (),  # subevent of dancing: exercise, movement
                        (Relationship.HasSubevent.value, False): (), # dancing is subevent of: go to party, hear music, have party
                        (Relationship.IsA.value, False): (),         # dance is a type of self-expression, diversion, pastime, ...
                        (Relationship.HasProperty, True): ()}        # property of dance: harder than parallel parking
        self.verb_semantics = {}
        self.conceptnet_client = ConceptnetClient()
        #self.corenlp_processor = StanfordCoreNLP(r'..\stanford-corenlp-full-2018-02-27')

    def _get_semantics_for_a_verb(self, verb):
        verb_semantics = self.conceptnet_client.get_concept(verb, self.filters)
        if verb_semantics is not None and len(verb_semantics) == 0:
            # try to get verb semantics of the root 'verb' word
            roots = self.conceptnet_client.get_concept(verb, {(Relationship.FormOf.value, True): ()}, end_sense_label = 'v')
            if len(roots) > 0:
                print(roots.values().__iter__().__next__()[0][0])
                verb_semantics = self.conceptnet_client.get_concept(roots.values().__iter__().__next__()[0][0], self.filters)

        return verb_semantics

    def _get_verbs_in_a_sentence(self, sentence):
        #pos_tags = self.corenlp_processor.pos_tag(sentence)
        pos_tags = [ verb for verb, pos_tag in nltk.pos_tag(nltk.word_tokenize(sentence)) if pos_tag.startswith('VB')]
        print(pos_tags)
        return pos_tags

    def _get_semantics_for_a_sentence(self, sentence):
        verbs = self._get_verbs_in_a_sentence(sentence)
        for verb in verbs:
            if verb not in self.verb_semantics:
                verb_semantics = self._get_semantics_for_a_verb(verb)
                if len(verb_semantics) > 0:
                    self.verb_semantics[verb] = self._get_semantics_for_a_verb(verb)

    def get_semantics_for_captions(self, captions):
        sentences = re.split("\[.*?\]\|", captions)
        [self._get_semantics_for_a_sentence(sentence) for sentence in sentences]
        return self.verb_semantics

if __name__ == '__main__':
    conceptnet_client = ConceptnetClient()
    verb_semantics = VerbSemantics()
    print(verb_semantics.get_semantics_for_captions("the meal is prepared and ready to be eaten"))
