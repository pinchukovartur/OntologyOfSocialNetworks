import random

from utils.vk_api import VKUtil
from settings import TOKEN, API_VERSION, ONTOLOGY_NAME
from utils.owl_lib import ProtegeParser, OntologyClass, OntologyIndividual
from utils.adapter_from_vk_in_owl_classes import CreteOWLModels
from utils.vk_adapter import *
from utils.vk_models import *
from create_owl_file import create_classes
# data_properties = ["first_name", "last_name", "id", "subscribers"]



vk_util = VKUtil(TOKEN, API_VERSION)

parser = Parser()
tmp1, tmp2, tmp3 = parser.parse_vk_response_base(vk_util.base_info(69128170)[0])
#print(next(iter(tmp1)).name, next(iter(tmp2)).name, next(iter(tmp3)).name)
#print(vk_util.base_info(69128170)[0])
content = create_classes([University, Faculty, Person])
#exit()

protege = ProtegeParser(ONTOLOGY_NAME)

classes_content = \
    """
    <!-- 
    ///////////////////////////////////////////////////////////////////////////////////////
    //
    // Classes
    //
    ///////////////////////////////////////////////////////////////////////////////////////
     -->
"""

ontology_classes = OntologyClass("VKontakte",
                                 [OntologyClass("Organization", []),
                                  OntologyClass("Group",
                                                [OntologyClass("Person", [])
                                                 ]),
                                  OntologyClass("OnlineAccount", []),
                                  OntologyClass("Document",
                                                [OntologyClass("Image", []),
                                                 OntologyClass("PersonDocument", [])
                                                 ])
                                  ])

#classes_content += protege.create_owl_class(ontology_classes)

data_properties_content = \
    """
    <!-- 
    ///////////////////////////////////////////////////////////////////////////////////////
    //
    // Data properties
    //
    ///////////////////////////////////////////////////////////////////////////////////////
     -->
"""

#individuals_ontology = CreteOWLModels(TOKEN, API_VERSION)
#groups_entity, users_entity, data_properties = individuals_ontology.create_friend_ref(194641487, 3) #194641487

#data_properties_content += protege.create_owl_data_properties(data_properties)

# individuals_content = protege.create_individuals(vk_util.friends(194641487)["items"], "person_", "Person")


object_properties_content = \
    """
    <!-- 
    ///////////////////////////////////////////////////////////////////////////////////////
    //
    // Object Properties
    //
    ///////////////////////////////////////////////////////////////////////////////////////
     -->
"""

object_properties = {"isConsist": ["AsymmetricProperty", "IrreflexiveProperty"],
                     "isFriend": ["SymmetricProperty", "IrreflexiveProperty"]}

#object_properties_content += protege.create_object_properties(object_properties)

individuals_content = \
    """
    <!-- 
    ///////////////////////////////////////////////////////////////////////////////////////
    //
    // Individuals
    //
    ///////////////////////////////////////////////////////////////////////////////////////
     -->
"""

#for individual in list(sum([groups_entity, users_entity], [])):
#    individuals_content += protege.create_individuals(individual)

protege.create_owl("H:\MEGAClouds\Магистратура\\1 Семестр\ИТПИС\PeopleOntology\\", "my_friends123.owl",
                   content)


