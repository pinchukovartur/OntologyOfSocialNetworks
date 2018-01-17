from utils import owl_lib


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
