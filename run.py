import random

from utils.vk_api import VKUtil
from settings import TOKEN, API_VERSION, ONTOLOGY_NAME
from utils.owl_lib import ProtegeParser, OntologyClass, OntologyIndividual
from utils.vk_adapter import *
from utils.vk_models import *
from create_owl_file import OwlCreator
# data_properties = ["first_name", "last_name", "id", "subscribers"]



vk_util = VKUtil(TOKEN, API_VERSION)
content = ""
parser = Parser()
print(vk_util.base_info(69128170))
owl = OwlCreator(ONTOLOGY_NAME)

for friend in vk_util.friends(69128170)["items"]:
    parser.parse_vk_response_base(vk_util.base_info(friend["id"])[0])
parser.parse_vk_response_base(vk_util.base_info(69128170)[0])

persons, faculties, universities, countries, cities, organizations, schools = parser.get_set_entities()
owl.create_owl_content_in_parser([persons, faculties, universities, countries, cities, organizations, schools])
content += owl.get_content()


protege = ProtegeParser(ONTOLOGY_NAME)
protege.create_owl("H:\MEGAClouds\Магистратура\\1 Семестр\ИТПИС\PeopleOntology\\", "my_friendsNEW.owl",
                   content)


