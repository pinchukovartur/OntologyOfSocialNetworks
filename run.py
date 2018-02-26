# my libs
from utils.vk_api import VKUtil
from utils.owl_lib import OWLFileManager
from utils.vk_adapter import VkParser

from settings import TOKEN, API_VERSION, ONTOLOGY_NAME, MAIN_USER_ID
from create_owl_file import OwlCreator

# create vk lib
vk_util = VKUtil(TOKEN, API_VERSION)
# create owl lib
owl = OwlCreator(ONTOLOGY_NAME)
# create vk parser
parser = VkParser()


# start download vk data
# download all info from main user friends
for friend in vk_util.friends(MAIN_USER_ID)["items"]:
    vk_response = vk_util.base_info(friend["id"])[0]
    parser.parse_vk_response_base(vk_response)

# parse main user
parser.parse_vk_response_base(vk_util.base_info(MAIN_USER_ID)[0])
# get parser data
persons = parser.get_persons()
faculties = parser.get_faculties()
universities = parser.get_universities()
countries = parser.get_countries()
cities = parser.get_cities()
organizations = parser.get_organizations()
schools = parser.get_schools()

# create owl file content
content = owl.create_owl_content_in_parser([persons, faculties, universities, countries, cities, organizations, schools])

# create file
protege = OWLFileManager(ONTOLOGY_NAME)
protege.create_owl_file("D:\\", "VkUsers.owl", content)


