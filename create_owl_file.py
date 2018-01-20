from utils.vk_models import Base


class OwlCreator:
    def __init__(self, ontology_name, ):
        self.ontology_name = ontology_name
        self.content = "\n"
        self.data_properties = set()
        self.references = set()

    def create_owl_content_in_parser(self, entity_sets):
        # проходим по всем сетам с сущностями
        for entity_set in entity_sets:
            # пытаемся создать их классы
            self.create_class(entity_set)
            for entity in entity_set:
                self.add_data_properties(entity.get_attributes().keys())
                self.add_references(entity.get_references().keys())
                self.content += entity.create_owl_content(self.ontology_name)
                print(entity.name, entity.id)

    def get_content(self):
        self.content += Base.create_data_properties(self.ontology_name, self.data_properties)
        self.content += Base.create_object_properties(self.ontology_name, self.references)
        return self.content

    def add_data_properties(self, list_properties):
        for property in list_properties:
            self.data_properties.add(property)

    def add_references(self, list_references):
        for ref in list_references:
            self.references.add(ref)

    def create_class(self, set_entity):
        if len(set_entity) > 0:
            self.content += list(set_entity)[0].create_owl_class(self.ontology_name)