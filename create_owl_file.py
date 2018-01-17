from utils import owl_lib



class OwlCreator:
    def __init__(self, ontology_name, entity_sets):

        if type(entity_sets) != list:
            print("bbbbbbbbbbbbbb", type(entity_sets))
        if len(entity_sets) < 1:
            print("aaaaaaaaaaa")

        self.ontology_name = ontology_name
        self.entities = entity_sets
        self.content = "\n"

    def create_classes(self):
        # проходим по всем сетам с сущностями
        for entity_set in self.entities:
            # пытаемся создать их классы
            if len(entity_set) > 0:
                self.content += list(entity_set)[0].create_owl_class(self.ontology_name)
                self.content += list(entity_set)[0].create_data_properties(self.ontology_name)
                self.content += list(entity_set)[0].create_object_properties(self.ontology_name)
            for entity in entity_set:
                self.content += entity.create_owl_content(self.ontology_name)
        return self.content

"""
def create_classes(vk_models):
    content = ""
    owl_creator = owl_lib.ProtegeParser("my_ontology")
    for vk_model in vk_models:
        parents = vk_model.get_parents()
        if len(parents) == 0:
            content += owl_creator.create_owl_class(vk_model.get_class_name())
        else:
            for parent in parents:
                content += owl_creator.create_subclass(parent, vk_model.get_class_name())

    return content


def create_individuals(entities, ontology_name):
    content = ""
    attributes = set()
    for entity in entities:
        content += entity.create_owl_content(ontology_name)
        for attrib in entity.get_attributes():
            attributes.add(attrib)
    content = ""
    owl_creator = owl_lib.ProtegeParser("my_ontology")
    content += owl_creator.create_owl_data_properties(attributes)
    return content
"""