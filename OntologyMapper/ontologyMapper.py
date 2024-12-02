import os
from rdflib import Graph, Namespace, URIRef, Literal, IdentifiedNode
import rdflib
from rdflib.util import from_n3
from rdflib.namespace import RDF, RDFS, XSD
# import multiprocessing
from termcolor import colored

from OntologyMapper.graph import GraphDesigner


class OntologyMapper:
    
    gD = None
    nsp = None
    current_course = 0
    _lock = None
    
    def __init__(self, gd: GraphDesigner):
        name_space = "http://uni-koblenz.de/"
        self.nsp = Namespace(name_space)
        self.gD = gd
        # self._lock = multiprocessing.Lock()
    
    def setup(self):
        self.gD.get_graph().bind("uniko", self.nsp)
        self.gD.add_node(self.nsp.Course, RDF.type, RDFS.Class)
        
        self.gD.add_node(self.nsp.Titel, RDF.type, RDF.Property)
        self.gD.add_node(self.nsp.Titel, RDFS.domain, self.nsp.Course)
        self.gD.add_node(self.nsp.Titel, RDFS.range, XSD.string)
        
        self.gD.add_node(self.nsp.Abschluss, RDF.type, RDF.Property)
        self.gD.add_node(self.nsp.Abschluss, RDFS.domain, self.nsp.Course)
        self.gD.add_node(self.nsp.Abschluss, RDFS.range, XSD.string)
        
        self.gD.add_node(self.nsp.Ansprechpartner, RDF.type, RDF.Property)
        self.gD.add_node(self.nsp.Ansprechpartner, RDFS.domain, self.nsp.Course)
        self.gD.add_node(self.nsp.Ansprechpartner, RDFS.range, XSD.string)
        
        self.gD.add_node(self.nsp.Voraussetzungen, RDF.type, RDF.Property)
        self.gD.add_node(self.nsp.Voraussetzungen, RDFS.domain, self.nsp.Course)
        self.gD.add_node(self.nsp.Voraussetzungen, RDFS.range, XSD.string)
        
        self.gD.add_node(self.nsp.Termine, RDF.type, RDF.Property)
        self.gD.add_node(self.nsp.Termine, RDFS.domain, self.nsp.Course)
        self.gD.add_node(self.nsp.Termine, RDFS.range, XSD.string)
        
        self.gD.add_node(self.nsp.Inhalt, RDF.type, RDF.Property)
        self.gD.add_node(self.nsp.Inhalt, RDFS.domain, self.nsp.Course)
        self.gD.add_node(self.nsp.Inhalt, RDFS.range, XSD.string)
        
        self.gD.add_node(self.nsp.Ziel, RDF.type, RDF.Property)
        self.gD.add_node(self.nsp.Ziel, RDFS.domain, self.nsp.Course)
        self.gD.add_node(self.nsp.Ziel, RDFS.range, XSD.string)
        
        self.gD.add_node(self.nsp.Zielgruppe, RDF.type, RDF.Property)
        self.gD.add_node(self.nsp.Zielgruppe, RDFS.domain, self.nsp.Course)
        self.gD.add_node(self.nsp.Zielgruppe, RDFS.range, XSD.string)
        
        self.gD.add_node(self.nsp.Dauer, RDF.type, RDF.Property)
        self.gD.add_node(self.nsp.Dauer, RDFS.domain, self.nsp.Course)
        self.gD.add_node(self.nsp.Dauer, RDFS.range, XSD.string)
        
        self.gD.add_node(self.nsp.Telefon, RDF.type, RDF.Property)
        self.gD.add_node(self.nsp.Telefon, RDFS.domain, self.nsp.Course)
        self.gD.add_node(self.nsp.Telefon, RDFS.range, XSD.string)
        
        self.gD.add_node(self.nsp.Fax, RDF.type, RDF.Property)
        self.gD.add_node(self.nsp.Fax, RDFS.domain, self.nsp.Course)
        self.gD.add_node(self.nsp.Fax, RDFS.range, XSD.string)
        
        self.gD.add_node(self.nsp.Email, RDF.type, RDF.Property)
        self.gD.add_node(self.nsp.Email, RDFS.domain, self.nsp.Course)
        self.gD.add_node(self.nsp.Email, RDFS.range, XSD.string)
        
        self.gD.save_graph()
    
    def load(self):
        if (os.path.isfile(self.gD.path_to_graph)):
            self.gD.get_graph().parse(self.gD.path_to_graph)
        else:
            self.setup()
     
    def writeCourse(self, data):
        id = str(data["id"])
        self.gD.add_node(URIRef(id, self.nsp), RDF.type, self.nsp.Course)
        for key in data:
            if(key != "id"):
                values = data[key]
                value = values[0]
                if(len(values) > 1):
                    value = ' '.join(map(str, values))
                self.mapper(id, key, value)
            #  make the graph a static variable       
        self.gD.save_graph()
        # with self._lock:
            
        
    def mapper(self, id, prediction, value):
        if prediction == "Titel":
            self.gD.add_node(URIRef(str(id), self.nsp), self.nsp.Titel, Literal(value))
        elif prediction == "Voraussetzungen":
            self.gD.add_node(URIRef(str(id), self.nsp), self.nsp.Voraussetzungen, Literal(value))
        elif prediction == "Zielgruppe":
            self.gD.add_node(URIRef(str(id), self.nsp), self.nsp.Zielgruppe, Literal(value))
        elif prediction == "Ziele":
            self.gD.add_node(URIRef(str(id), self.nsp), self.nsp.Ziel, Literal(value))
        elif prediction == "Telefon":
            self.gD.add_node(URIRef(str(id), self.nsp), self.nsp.Telefon, Literal(value))
        elif prediction == "Dauer":
            self.gD.add_node(URIRef(str(id), self.nsp), self.nsp.Dauer, Literal(value))
        elif prediction == "Ansprechpartner":
            self.gD.add_node(URIRef(str(id), self.nsp), self.nsp.Ansprechpartner, Literal(value))
        elif prediction == "Abschluss":
            self.gD.add_node(URIRef(str(id), self.nsp), self.nsp.Abschluss, Literal(value))
        elif prediction == "Fax":
            self.gD.add_node(URIRef(str(id), self.nsp), self.nsp.Fax, Literal(value))
        elif prediction == "Termine":
            self.gD.add_node(URIRef(str(id), self.nsp), self.nsp.Termine, Literal(value))
        elif prediction == "Email":
            self.gD.add_node(URIRef(str(id), self.nsp), self.nsp.Email, Literal(value))
        elif prediction == "Beschreibung":
            print(colored('Beschreibung --> Not yet implemented', 'red'))
        elif prediction == "Inhalt":
            self.gD.add_node(URIRef(str(id), self.nsp), self.nsp.Inhalt, Literal(value))
        
    
