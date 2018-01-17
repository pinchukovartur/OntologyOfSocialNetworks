class OntologyClass:
    """
    Класс реализующий класс в системе protege
    """

    def __init__(self, name, subclasses):
        if type(subclasses) != list:
            raise NameError("Класс должен содержать лист подклассов")

        self.name = name
        self.subclasses = subclasses


class OntologyIndividual:
    def __init__(self, name, group, properties, descriptions):
        if type(name) != str:
            raise NameError("name должен быть типа str")
        if type(group) != list:
            raise NameError("group должен быть типа list")
        if type(properties) != dict:
            raise NameError("properties должен быть типа dict")
        if type(descriptions) != list:
            raise NameError("descriptions должен быть типа list")

        self.name = name
        self.group = group
        self.properties = properties
        self.descriptions = descriptions


class ProtegeParser:
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
            + self.ontology_name + """"/>\n"""
        self.footer = """\n</rdf:RDF>"""

        self.list_replaces = ["$", "&", "%", "#", "№", "@", "!", "*", "<", ">"]

    def create_owl(self, file_path, file_name, file_content):
        file = open(file_path + "/" + file_name, "w", encoding="utf8")
        file.write(self.header + file_content + self.footer)
        file.close()

    def create_individuals(self, individual):
        """
        Метод создает контекст с описанием сущностей
        """
        content = ""
        # парсим данные класса онтологии
        name = individual.name
        groups = individual.group
        properties = individual.properties
        descriptions = individual.descriptions

        # создаем класс
        content += """<owl:NamedIndividual rdf:about="http://www.semanticweb.org/iiiiii/ontologies/2018/0/""" \
                   + self.ontology_name + """#""" + self.__check_value(name) + """">\n"""

        # назначаем группу для сущности
        for group in groups:
            content += """<rdf:type rdf:resource="http://www.semanticweb.org/iiiiii/ontologies/2018/0/""" \
                       + self.ontology_name + """#""" + self.__check_value(str(group)) + """"/>\n"""

        # назначаем данные атрибутов
        for key, value in properties.items():
            content += '  <' + self.__check_value(str(key)) + '>' \
                       + self.__check_value(str(value)) + \
                       '</' + self.__check_value(str(key)) + '>\n'

        # если сущность не имеет описания, возвращаем что есть

        if descriptions == "":
            content += """</owl:NamedIndividual>\n"""
            return content + "\n"
        else:
            for desc in descriptions:
                content += "<" + str(
                    desc[1]) + """ rdf:resource="http://www.semanticweb.org/iiiiii/ontologies/2018/0/""" + \
                           self.ontology_name + "#" + str(desc[0]) + '"/>\n'

            content += """</owl:NamedIndividual>\n"""
            return content + "\n"

    def create_owl_class(self, class_name):
        """
        Метод создает контекст с описанием класса
        """

        content = """<owl:Class rdf:about="http://www.semanticweb.org/iiiiii/ontologies/2018/0/""" \
                  + self.ontology_name + """#""" + class_name + """"/>\n\n"""

        return content

    def create_subclass(self, class_parent, subclass_name):
        """
        Метод создает контекст с описанием додкласа
        """

        content = """<owl:Class rdf:about="http://www.semanticweb.org/iiiiii/ontologies/2018/0/""" \
                  + self.ontology_name + """#""" + subclass_name + """">\n""" + \
                  """\t<rdfs:subClassOf rdf:resource="http://www.semanticweb.org/iiiiii/ontologies/2018/0/""" \
                  + self.ontology_name + """#""" + class_parent + """"/>\n</owl:Class>\n\n"""

        return content

    def create_owl_data_properties(self, data_properties):
        """
        Метод создает контекст с описанием свойст данных
        :param data_properties: dict свойств
        :return: строку с даннывими
        """
        if type(data_properties) != set:
            raise NameError("data_properties должен быть типа list")

        content = ""
        for property_key in data_properties:
            content += """<owl:DatatypeProperty rdf:about="http://www.semanticweb.org/iiiiii/ontologies/2018/0/""" + \
                       self.ontology_name + """#""" + self.__check_value(str(property_key)) + """">\n""" + \
                       """\t<rdfs:subPropertyOf rdf:resource="http://www.w3.org/2002/07/owl#topDataProperty"/>\n""" + \
                       """\t<rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>\n""" + \
                       """</owl:DatatypeProperty>\n\n"""
        return content

    def create_object_properties(self, object_properties):
        if type(object_properties) != dict:
            raise NameError("object_properties must be dict")

        content = ""
        for key, value in object_properties.items():
            content += """<owl:ObjectProperty rdf:about="http://www.semanticweb.org/iiiiii/ontologies/2018/0/""" \
                       + self.ontology_name + """#""" + str(key) + '">\n'
            for properties_rel in value:
                content += """\t<rdf:type rdf:resource="http://www.w3.org/2002/07/owl#""" \
                           + self.__check_value(str(properties_rel)) + """"/>\n"""
            content += "</owl:ObjectProperty>\n\n"

        return content

    def __check_value(self, str_value):
        """
        Replace всех недопустимых символов для Protege
        :param str_value:
        :return:
        """
        for symbol in self.list_replaces:
            str_value = str(str_value).replace(symbol, " ")
        return str_value
