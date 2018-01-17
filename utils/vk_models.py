from abc import abstractmethod


class Base:
    def __init__(self, id_entity, name):
        self.name = name
        self.id = id_entity

    def is_consist_in(self, entity_set):
        for entity in entity_set:
            if entity.id == self.id:
                return True
        return False

    @staticmethod
    @abstractmethod
    def get_parents():
        return []

    @staticmethod
    def get_class_name():
        pass

    @abstractmethod
    def create_owl_content(self, ontology_name):
        content = """<owl:NamedIndividual rdf:about="http://www.semanticweb.org/iiiiii/ontologies/2018/0/""" \
                  + ontology_name + """#""" + str(self.id) + """">\n"""

        # назначаем группу для сущности
        content += """<rdf:type rdf:resource="http://www.semanticweb.org/iiiiii/ontologies/2018/0/""" \
                   + ontology_name + """#""" + str(self.get_class_name()) + """"/>\n"""

        # назначаем данные атрибутов
        for key, value in self.get_attributes().items():
            content += '  <' + str(key) + '>' \
                       + str(value) + \
                       '</' + str(key) + '>\n'
        return content

    @staticmethod
    @abstractmethod
    def get_references():
        return []

    @abstractmethod
    def get_attributes(self):
        return {"name": self.name, "id": self.id}

    def create_owl_class(self, ontology_name):
        parents = self.get_parents()
        content = ""
        if len(parents) > 0:
            for parent in parents:
                content += """<owl:Class rdf:about="http://www.semanticweb.org/iiiiii/ontologies/2018/0/""" \
                          + ontology_name + """#""" + str(self.get_class_name()) + """">\n""" + \
                          """\t<rdfs:subClassOf rdf:resource="http://www.semanticweb.org/iiiiii/ontologies/2018/0/""" \
                          + ontology_name + """#""" + str(parent) + """"/>\n</owl:Class>\n\n"""
        else:
            content += """<owl:Class rdf:about="http://www.semanticweb.org/iiiiii/ontologies/2018/0/""" \
                  + ontology_name + """#""" + str(self.get_class_name()) + """"/>\n\n"""
        return content

    def create_data_properties(self, ontology_name):

        content = ""
        for property_key in self.get_attributes().keys():
            content += """<owl:DatatypeProperty rdf:about="http://www.semanticweb.org/iiiiii/ontologies/2018/0/""" + \
                       ontology_name + """#""" + str(property_key) + """">\n""" + \
                       """\t<rdfs:subPropertyOf rdf:resource="http://www.w3.org/2002/07/owl#topDataProperty"/>\n""" + \
                       """\t<rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>\n""" + \
                       """</owl:DatatypeProperty>\n\n"""
        return content

    def create_object_properties(self, ontology_name):

        content = ""
        for property_key in self.get_references():
            content += """<owl:ObjectProperty rdf:about="http://www.semanticweb.org/iiiiii/ontologies/2018/0/"""+ \
                        ontology_name + """#""" + property_key + """"/>\n\n"""
        return content


class Person(Base):
    def get_attributes(self):
        attributes = super().get_attributes()
        attributes["surname"] = self.surname
        return attributes

    @staticmethod
    def get_references():
        return ["isStudy"]

    def create_owl_content(self, ontology_name):
        content = super().create_owl_content(ontology_name)
        content += "<" + "isStudy" + """ rdf:resource="http://www.semanticweb.org/iiiiii/ontologies/2018/0/""" + \
                   ontology_name + "#" + str(self.faculty.id) + '"/>\n'

        content += """</owl:NamedIndividual>\n\n"""
        return content

    @staticmethod
    def get_class_name():
        return "Person"

    @staticmethod
    def get_parents():
        return ["Faculty"]

    def __init__(self, id_person, name, surname, faculty):
        super().__init__(id_person, name)
        self.surname = surname
        self.faculty = faculty


class Faculty(Base):
    def get_attributes(self):
        return super().get_attributes()

    def create_owl_content(self, ontology_name):
        content = super().create_owl_content(ontology_name)
        content += "<" + "isBelongs" + """ rdf:resource="http://www.semanticweb.org/iiiiii/ontologies/2018/0/""" + \
                   ontology_name + "#" + str(self.university.id) + '"/>\n'

        content += """</owl:NamedIndividual>\n\n"""
        return content

    @staticmethod
    def get_references():
        return ["isBelongs"]

    @staticmethod
    def get_class_name():
        return "Faculty"

    @staticmethod
    def get_parents():
        return ["University"]

    def __init__(self, id_faculty, name, university):
        super().__init__(id_faculty, name)
        self.university = university


class University(Base):
    def get_attributes(self):
        return super().get_attributes()

    def create_owl_content(self, ontology_name):
        content = super().create_owl_content(ontology_name)
        content += """</owl:NamedIndividual>\n\n"""
        return content

    @staticmethod
    def get_references():
        return []

    @staticmethod
    def get_class_name():
        return "University"

    @staticmethod
    def get_parents():
        return []

    def __init__(self, id_university, name):
        super().__init__(id_university, name)
