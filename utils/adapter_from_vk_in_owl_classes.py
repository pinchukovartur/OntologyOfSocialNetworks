from utils.owl_lib import OntologyClass, OntologyIndividual
from utils.vk_api import *
from settings import API_VERSION, TOKEN


class CreteOWLModels:
    def __init__(self, TOKEN, API_VERSION):
        self.vk_utilita = VKUtil(TOKEN, API_VERSION)
        self.groups_entity = list()
        self.users_entity = list()
        self.data_properties = list()
        self.flag = 0

        self.dict_friend = dict()

    def create_friend_ref(self, user_id, nesting):
        first_individ = self.create_individual_by_user_id(str(user_id))
        checked_list = list()
        # self.check_friends(first_individ, checked_list, nesting)
        self.get_friend_dict(self.vk_utilita.base_info(user_id)[0], nesting)
        print("len dict = ", len(self.dict_friend))
        self.add_friend()
        # print(len(self.dict_friend))

        return self.groups_entity, self.users_entity, self.data_properties

    def add_friend(self):
        for key, friend in self.dict_friend.items():
            ontology_first = self.get_individual_by_id(key)
            ontology_second = self.get_individual_by_id(friend[0]["id"])
            if ontology_second is None:
                # ontology_second = self.create_individual_by_user_dict(friend[0])
                continue
            if ontology_first is None:
                # ontology_first = self.create_individual_by_user_id(key)
                continue

            if not self.check_friend_in_individual(ontology_first, ontology_second.name) and \
                    not self.check_friend_in_individual(ontology_second, ontology_first.name):
                print("add", ontology_first.name, " in ", ontology_second.name)
                ontology_first.descriptions.append([ontology_second.name, "isFriend"])

    def check_friend_in_individual(self, individual, friend_id):
        for description in individual.descriptions:
            if description[0] == friend_id:
                return True
        return False

    def get_friend_dict(self, main_curr, nesting):
        if nesting > 0:
            try:

                if main_curr["id"] not in self.dict_friend.keys():
                    friends = self.vk_utilita.friends(str(main_curr["id"]))["items"]
                    self.dict_friend[main_curr["id"]] = friends
                    self.create_individual_by_user_dict(friends[0])
                    #print("add ", main_curr["first_name"], " ", main_curr["last_name"])
                    nesting -= 1
                    for friend in friends:
                        self.get_friend_dict(friend, nesting)
            except Exception as err:
                print(err)

    def check_friends(self, main_individual, checked_list, level):
        if level > 0:
            level -= 1
            friends = self.vk_utilita.friends(main_individual.name)["items"]
            for friend in friends:
                if friend["id"] not in checked_list:
                    checked_list.append(friend["id"])
                    individ = self.create_individual_by_user_dict(friend)
                    individ.descriptions.append(["isFriend", main_individual.name])
                    self.flag += 1
                    print(self.flag)
                    self.check_friends(individ, checked_list, level)

    def add_friends(self):
        for user_id in range(len(self.users_entity)):
            friends = self.vk_utilita.friends(self.users_entity[str(user_id)].name)["items"]
            for friend in friends:
                self.create_individual_by_user_id(friend["id"])

    def create_individual_by_user_id(self, user_id):
        main_user = self.vk_utilita.base_info(str(user_id))[0]
        # print("add - " + str(main_user["first_name"] + "_" + str(main_user["last_name"])))
        individ = OntologyIndividual(str(main_user["id"]),
                                     ["Person"],
                                     main_user,
                                     self.get_group_description(main_user["id"]))
        self.users_entity.append(individ)
        return individ

    def create_individual_by_user_dict(self, user_info):
        main_user = dict()
        main_user["first_name"] = user_info["first_name"]
        main_user["last_name"] = user_info["last_name"]
        main_user["id"] = user_info["id"]
        main_user["photo"] = user_info["photo"]

        # print("add - " + str(main_user["first_name"] + "_" + str(main_user["last_name"])))
        individ = OntologyIndividual(str(main_user["id"]),
                                     ["Person"],
                                     main_user,
                                     self.get_group_description(main_user["id"]))
        self.users_entity.append(individ)
        return individ

    def get_group_description(self, user_id):
        try:
            groups = self.vk_utilita.subscriptions(str(user_id))['items']
            if len(groups) == 0:
                return list()
            groups_description_list = list()

            self.__add_data_properties(
                ["is_closed", "screen_name", "name", "id", "type", "photo_50", "photo_100", "photo_200"])

            for group in groups:
                group_data = {"is_closed": group["is_closed"],
                              "screen_name": group["screen_name"],
                              "name": group["name"],
                              "id": group["id"],
                              "type": group["is_closed"],
                              "photo_50": group["photo_50"],
                              "photo_100": group["photo_100"],
                              "photo_200": group["photo_200"],
                              }
                group_ontology = OntologyIndividual(str(group["id"]), ["Group"], group_data, [])
                if group_ontology not in self.groups_entity:
                    self.groups_entity.append(group_ontology)

                groups_description_list.append([group["id"], "isConsist", ])
            return groups_description_list
        except Exception as error:
            print(error)
            return list()

    def __add_data_properties(self, list_property):
        for prop in list_property:
            if prop not in self.data_properties:
                self.data_properties.append(prop)

    def get_individual_by_id(self, id):
        for individual in self.users_entity:
            if individual.name == str(id):
                return individual
