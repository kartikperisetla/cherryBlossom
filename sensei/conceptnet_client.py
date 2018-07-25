import os
import urllib.request
import json

EDGES = "edges"

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

    def _parse_json(self, response):
        raw = json.loads(response)

        # parse edges
        if EDGES in raw:
            edges = raw[EDGES]

            for edge in edges:
                # WIP - Kartik working on creating in graph structure for consumption
                


    def get_concept(self, name):
        _url = self.endpoint + name
        contents = urllib.request.urlopen(_url).read()
        print(contents)

if __name__ == "__main__":
    c = ConceptnetClient()
    c.get_concept("orange")
        