from abc import abstractmethod


class Base:
    def __init__(self, id_entity, name):
        self.name = name
        self.id = str(id_entity).replace('"', "").replace(" ", "_")

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
    @abstractmethod
    def get_class_name():
        pass

    @abstractmethod
    def create_owl_content(self, ontology_name):
        content = """<owl:NamedIndividual rdf:about="http://www.semanticweb.org/iiiiii/ontologies/2018/0/""" \
                  + ontology_name + """#""" + str(self.id) \
                  + """">\n"""

        # назначаем группу для сущности
        content += """<rdf:type rdf:resource="http://www.semanticweb.org/iiiiii/ontologies/2018/0/""" \
                   + ontology_name + """#""" + str(self.get_class_name()) + """"/>\n"""

        # назначаем данные атрибутов
        for key, value in self.get_attributes().items():
            if value:
                content += '  <' + str(key) + '>' \
                           + str(value) + \
                           '</' + str(key) + '>\n'
        return content

    @abstractmethod
    def get_references(self):
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

    @staticmethod
    def create_data_properties(ontology_name, attributes):
        content = ""
        for property_key in attributes:
            content += """<owl:DatatypeProperty rdf:about="http://www.semanticweb.org/iiiiii/ontologies/2018/0/""" + \
                       ontology_name + """#""" + str(property_key) + """">\n""" + \
                       """\t<rdfs:subPropertyOf rdf:resource="http://www.w3.org/2002/07/owl#topDataProperty"/>\n""" + \
                       """\t<rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>\n""" + \
                       """</owl:DatatypeProperty>\n\n"""
        return content

    @staticmethod
    def create_object_properties(ontology_name, references):
        content = ""
        for property_key in references:
            content += """<owl:ObjectProperty rdf:about="http://www.semanticweb.org/iiiiii/ontologies/2018/0/""" + \
                       ontology_name + """#""" + property_key + """"/>\n\n"""
        return content


class Person(Base):
    def get_attributes(self):
        attributes = super().get_attributes()
        attributes["surname"] = self.surname
        attributes["sex"] = self.sex
        attributes["about_self"] = self.about_self
        attributes["activities"] = self.activities
        attributes["dateOfBirth"] = self.bdate
        attributes["books"] = self.books
        return attributes

    def get_references(self):
        return {"isStudy": [self.faculties, self.schools], "isLive": self.city, "isWork": self.organization}

    def create_owl_content(self, ontology_name):
        content = super().create_owl_content(ontology_name)
        if self.faculties:
            for faculty in self.faculties:
                content += "<" + str(list(self.get_references().keys())[0]) + \
                           """ rdf:resource="http://www.semanticweb.org/iiiiii/ontologies/2018/0/""" + \
                           ontology_name + "#" + str(faculty.id) + '"/>\n'

        if self.schools:
            for school in self.schools:
                content += "<" + str(list(self.get_references().keys())[0]) + \
                           """ rdf:resource="http://www.semanticweb.org/iiiiii/ontologies/2018/0/""" + \
                           ontology_name + "#" + str(school.id) + '"/>\n'

        if self.city is not None:
                content += "<" + str(list(self.get_references().keys())[1]) + \
                           """ rdf:resource="http://www.semanticweb.org/iiiiii/ontologies/2018/0/""" + \
                           ontology_name + "#" + str(self.city.id) + '"/>\n'
        if self.organization is not None:
                content += "<" + str(list(self.get_references().keys())[2]) + \
                           """ rdf:resource="http://www.semanticweb.org/iiiiii/ontologies/2018/0/""" + \
                           ontology_name + "#" + str(self.organization.id) + '"/>\n'

        content += """</owl:NamedIndividual>\n\n"""
        return content

    @staticmethod
    def get_class_name():
        return "Person"

    @staticmethod
    def get_parents():
        return ["Faculty", "City", "School", "Organization"]

    def __init__(self, id_person, name, surname, sex, about_self, activities, bdate, books,
                 faculties, city, organization, schools):
        """
        :param id_person: id человека в вк
        :param name: имя
        :param surname: фамилия
        :param sex: пол
        :param about_self: о себе (поле)
        :param activities: деятельность (поле)
        :param bdate: дата рождения
        :param books: любимые книги (поле)
        :param faculties: факультеты где обучался человек(Объект)
        :param city: город проэивания(Объект)
        :param organization: место работы
        :param schools: школа
        """
        super().__init__(id_person, name)
        self.surname = surname
        self.sex = sex
        self.about_self = about_self
        self.activities = activities
        self.bdate = bdate
        self.books = books
        self.faculties = faculties
        self.city = city
        self.organization = organization
        self.schools = schools


class Faculty(Base):
    def get_attributes(self):
        return super().get_attributes()

    def create_owl_content(self, ontology_name):
        content = super().create_owl_content(ontology_name)
        content += "<" + str(list(self.get_references().keys())[0]) + \
                   """ rdf:resource="http://www.semanticweb.org/iiiiii/ontologies/2018/0/""" + \
                   ontology_name + "#" + str(self.university.id) + '"/>\n'

        content += """</owl:NamedIndividual>\n\n"""
        return content

    def get_references(self):
        return {"isBelongs": self.university}

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
        if self.city:
            content += "<" + str(list(self.get_references().keys())[0]) + \
                       """ rdf:resource="http://www.semanticweb.org/iiiiii/ontologies/2018/0/""" + \
                       ontology_name + "#" + str(self.city.id) + '"/>\n'
        content += """</owl:NamedIndividual>\n\n"""
        return content

    def get_references(self):
        return {"isConsist": self.city}

    @staticmethod
    def get_class_name():
        return "University"

    @staticmethod
    def get_parents():
        return []

    def __init__(self, id_university, name, city):
        super().__init__(id_university, name)
        self.city = city


class Country(Base):
    def __init__(self, id_county, name):
        super().__init__(id_county, name)

    def get_attributes(self):
        return super().get_attributes()

    def get_references(self):
        return {}

    @staticmethod
    def get_parents():
        return []

    @staticmethod
    def get_class_name():
        return "Country"

    def create_owl_content(self, ontology_name):
        content = super().create_owl_content(ontology_name)
        content += """</owl:NamedIndividual>\n\n"""
        return content


class City(Base):
    @staticmethod
    def get_class_name():
        return "City"

    def __init__(self, id_city, name, country):
        super().__init__(id_city, name)
        self.country = country

    def get_attributes(self):
        return super().get_attributes()

    def get_references(self):
        return {"isIn": self.country}

    @staticmethod
    def get_parents():
        return ["Country"]

    def create_owl_content(self, ontology_name):
        content = super().create_owl_content(ontology_name)
        content += "<" + str(list(self.get_references().keys())[0]) + \
                   """ rdf:resource="http://www.semanticweb.org/iiiiii/ontologies/2018/0/""" + \
                   ontology_name + "#" + str(self.country.id) + '"/>\n'

        content += """</owl:NamedIndividual>\n\n"""
        return content


class Organization(Base):
    def get_attributes(self):
        return super().get_attributes()

    def get_references(self):
        return {}

    @staticmethod
    def get_class_name():
        return "Organization"

    @staticmethod
    def get_parents():
        return []

    def create_owl_content(self, ontology_name):
        content = super().create_owl_content(ontology_name)
        content += """</owl:NamedIndividual>\n\n"""
        return content


class School(Base):
    def __init__(self, id_school, name, city):
        super().__init__(id_school, name)
        self.city = city

    def create_owl_content(self, ontology_name):
        content = super().create_owl_content(ontology_name)
        if self.city is not None:
            content += "<" + str(list(self.get_references().keys())[0]) + \
                       """ rdf:resource="http://www.semanticweb.org/iiiiii/ontologies/2018/0/""" + \
                       ontology_name + "#" + str(self.city.id) + '"/>\n'
        content += """</owl:NamedIndividual>\n\n"""
        return content

    @staticmethod
    def get_parents():
        return []

    def get_references(self):
        return {"isIn": self.city}

    def get_attributes(self):
        return super().get_attributes()

    @staticmethod
    def get_class_name():
        return "School"
