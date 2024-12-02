# import multiprocessing
from rdflib import Graph


class GraphDesigner:
    
    # make it singleton
    
    g = None
    path_to_graph = ""
    
    def __init__(self, path = '/Users/manendraranathunga/Documents/Thesis/predictions/Graph/Learning_Courses.ttl'):
        self.g = Graph()
        self.path_to_graph = path
        
    def get_graph(self):
        return self.g
    
    def set_graph(self, graph):
        self.g = graph
        
    def add_node(self, subject, predicate, object):
        self.g.add((
                subject,
                predicate,
                object
            ))
        
    def save_graph(self):
        self.g.serialize(destination=self.path_to_graph)

    def show_namespaces(self):
        for ns_prefix, namespace in self.g.namespaces():
            print(ns_prefix, namespace)
    
    def show_graph(self):
        for s, p, o in self.g:
            print(s, p, o)