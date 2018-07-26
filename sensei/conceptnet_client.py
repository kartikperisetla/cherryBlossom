import os
import requests, re
import json
import math
from collections import defaultdict

EDGES = "edges"
DEFAULT_IS_SOURCE = True
DEFAULT_WEIGHT_THRESHOLD = -math.inf
DEFAULT_MAX_ITEMS = math.inf

class Edge:
    def __init__(self):
        self.type = "Edge"

        # points to start node from where relation begins i.e. Subject
        self.start = None

        # points to end node at which relation ends i.e. Object
        self.end = None

        # points to relation instance i.e. Predicate
        self.rel = None

        # indicates the surface text for how this relation connects Subject and Object
        self.surface_text = None

        self.weight = None

class Filter:
    def __init__(self, is_source = DEFAULT_IS_SOURCE, weight_threshold = DEFAULT_WEIGHT_THRESHOLD, max_items = DEFAULT_MAX_ITEMS):
        self.filter = { is_source : FilterParams(weight_threshold, max_items) }
        #self.is_source = is_source
        #self.weight_threshold = weight_threshold
        #self.max_items = max_items
class FilterParams:
    def __init__(self, weight_threshold, max_items):
        self.weight_threshold = weight_threshold
        self.max_items = max_items

class Node:
    def __init__(self):
        self.id = None
        self.type = "Node"
        self.label = None

class Relation:
    def __init__(self):
        self.type = "Relation"
        self.label = None


class ConceptnetClient:
    def __init__(self):
        self.endpoint = "http://api.conceptnet.io/c/en/"
        self.default_is_source = True
        self.default_weight_threshold = 5
        self.default_max_items = math.inf

    def _parse_json(self, response):
        raw = json.loads(response)

        # parse edges
        # if EDGES in raw:
        #     edges = raw[EDGES]

        #     for edge in edges:
                # WIP - Kartik working on creating in graph structure for consumption
                
    # filters - dictionary of parameters {relationship_name: ( isSource = True, weight_threshold = 5, max_items = math.Inf) }
    def filter_concepts(self, name, edges, filters):
        items_per_relation = defaultdict(int)
        concepts_per_relation = defaultdict(list)

        for edge in edges:
            # Check if relationship is required
            edge_relationship = edge['rel']['label']
            if edge_relationship in filters:
                config = filters[edge_relationship]
                is_source_flags = config.keys()

                for is_source in is_source_flags:
                    if (( ( is_source and edge['start']['label'].lower() == name ) or
                        (not is_source and edge['end']['label'].lower() == name) ) and
                        (edge['weight'] >= config[is_source].weight_threshold) and 
                        (items_per_relation.get( (edge_relationship, is_source), 0) < config[is_source].max_items)):
                    
                        items_per_relation[(edge_relationship, is_source)] += 1

                        if is_source:
                            concepts_per_relation[(edge_relationship, is_source)].append((edge['end']['label'].lower(), edge['weight']))
                        else:
                            concepts_per_relation[(edge_relationship, is_source)].append((edge['start']['label'].lower(), edge['weight']))

        return concepts_per_relation

    def format_filters(self, filters):
        formatted_filters = defaultdict(dict)
        for relation, config in filters.items():
            relation_name = relation[0]
            is_source_flag = relation[1] if len(relation) > 1 else DEFAULT_IS_SOURCE
            if len(config) == 0:
                formatted_filters[relation_name].update(Filter(is_source_flag).filter)
            elif len(config) == 1:
                formatted_filters[relation_name].update(Filter(is_source_flag, config[0]).filter)
            elif len(config) == 2:
                formatted_filters[relation_name].update(Filter(is_source_flag, config[0], config[1]).filter)

        return formatted_filters

    def get_concept(self, name, filters):

        name = name.lower()
        _url = self.endpoint + re.sub(' +','_', name)
        contents = requests.get(_url).json()

        if contents.get('error',{}).get('status',200) == 404:
            return None

        formatted_filters = self.format_filters(filters)
        filtered_concepts = self.filter_concepts(name, contents['edges'], formatted_filters)

        return filtered_concepts

if __name__ == "__main__":
    c = ConceptnetClient()

    filters = {('DefinedAs', True): (), ('DefinedAs', False): ()}
    print(c.get_concept("playing", filters))
