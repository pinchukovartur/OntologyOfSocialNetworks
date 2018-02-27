class OWLFileManager:
    def __init__(self, ontology_name):
        """
        Инициализация класса для работы с данными онтологии
        :param ontology_name: название онтологии
        """
        self.ontology_name = ontology_name
        self.header = \
            """<?xml version="1.0"?>
        <rdf:RDF xmlns="http://www.semanticweb.org/iiiiii/ontologies/2018/0/""" + self.ontology_name + """#"
             xml:base="http://www.semanticweb.org/iiiiii/ontologies/2018/0/""" + self.ontology_name + """"
             xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
             xmlns:owl="http://www.w3.org/2002/07/owl#"
             xmlns:xml="http://www.w3.org/XML/1998/namespace"
             xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
             xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">
             
             <owl:Ontology rdf:about="http://www.semanticweb.org/iiiiii/ontologies/2018/0/""" \
            + self.ontology_name + """"/>\n""" + \
            """
            <!--
            Generate by OntologyOfSocialNetworks
            
            github: https://github.com/pinchukovartur/OntologyOfSocialNetworks
            author: Pinchukov Artur
            date: 27.02.2018
            -->
            """
        self.footer = """\n</rdf:RDF>"""

        self.list_replaces = ["$", "&", "%", "#", "№", "@", "!", "*", "<", ">"]

    def create_owl_file(self, file_path, file_name, file_content):
        file = open(file_path + "/" + file_name, "w", encoding="utf8")
        file.write(self.header + file_content + self.footer)
        file.close()
