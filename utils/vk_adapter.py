from utils.vk_models import University, Faculty, Person, Country, City, Organization, School, Photo, Military, Group


class VkParser:
    def __init__(self):
        self.persons = set()
        self.faculties = set()
        self.universities = set()
        self.countries = set()
        self.cities = set()
        self.organizations = set()
        self.schools = set()
        self.photos = set()
        self.military = set()
        self.groups = set()

    @staticmethod
    def _find_by_id_in_set(id_entity, set_entities):
        for entity in set_entities:
            if entity.id == id_entity:
                return entity
        return None

    def parse_vk_response_base(self, dict_base):
        """
        Парсинг метода base вк api
        :param dict_base:
        :return:
        """
        print(dict_base)
        # создаем человека

        # first lvl
        organization = self.parse_organization(dict_base)
        country = self.parse_country(dict_base)
        self.parse_groups(dict_base)

        # second level
        city = self.parse_city(dict_base, country)
        self.parse_military(dict_base)

        # third level
        schools = self.parse_school(dict_base)
        list_faculties, list_universities = self.parse_person_universities(dict_base)

        # forth level
        person = self.parse_person_data(dict_base, list_faculties, city, organization, schools)

        # fifth level
        self.parse_photos(dict_base)

        if organization:
            if not organization.is_consist_in(self.organizations) and organization is not None:
                self.organizations.add(organization)
        if schools:
            for school in schools:
                if not school.is_consist_in(self.schools) and school is not None:
                    self.schools.add(school)

        # добавляем все в массивы с сущностями
        if not person.is_consist_in(self.persons) and person is not None:
            self.persons.add(person)
        if list_faculties:
            for faculty in list_faculties:
                if not faculty.is_consist_in(self.faculties) and faculty is not None:
                    self.faculties.add(faculty)
        if list_universities:
            for university in list_universities:
                if not university.is_consist_in(self.universities) and university is not None:
                    self.universities.add(university)
        if country:
            if not country.is_consist_in(self.countries) and country is not None:
                self.countries.add(country)
        if city:
            if not city.is_consist_in(self.cities) and city is not None:
                self.cities.add(city)

    def parse_groups(self, dict_base):
        if "groups" in dict_base.keys():
            for group in dict_base["groups"]:
                if "id" in group.keys() and "name" in group.keys():
                    self.groups.add(Group(group["id"], group["name"]))

    def parse_military(self, dict_base):
        if "military" in dict_base.keys() and len(dict_base["military"]) > 0:
            for military in dict_base["military"]:
                self.military.add(Military(military["unit_id"], military["unit"], self.get_entity_by_id(military["country_id"])))

    def parse_photos(self, dict_base):

        if "photo_50" in dict_base.keys():
            self.photos.add(Photo(dict_base["photo_50"], "photo_50", self.get_entity_by_id(dict_base["id"])))
        if "photo_100" in dict_base.keys():
            self.photos.add(Photo(dict_base["photo_100"], "photo_100", self.get_entity_by_id(dict_base["id"])))
        if "photo_200" in dict_base.keys():
            self.photos.add(Photo(dict_base["photo_200"], "photo_200", self.get_entity_by_id(dict_base["id"])))
        if "photo_max" in dict_base.keys():
            self.photos.add(Photo(dict_base["photo_max"], "photo_max", self.get_entity_by_id(dict_base["id"])))
        if "photo_200_orig" in dict_base.keys():
            self.photos.add(Photo(dict_base["photo_200_orig"], "photo_200_orig", self.get_entity_by_id(dict_base["id"])))


    def parse_school(self, dict_base):
        list_schools = list()
        if "schools" in dict_base.keys():
            for school in dict_base["schools"]:
                list_schools.append(School(school["id"], school["name"], self.get_entity_by_id(
                    school["city"])))
        return list_schools

    def parse_country(self, dict_base):
        """
        'country': {'id': 3, 'title': 'Беларусь'},
        """
        if "country" in dict_base.keys():
            return Country(dict_base["country"]["id"], dict_base["country"]["title"])

    def parse_organization(self, dict_base):
        if "career" in dict_base.keys():
            if len(dict_base["career"]) > 0:
                if "company" in dict_base["career"][0]:
                    return Organization(dict_base["career"][0]["company"], dict_base["career"][0]["company"])

    def parse_city(self, dict_base, country):
        """
        'city': {'id': 282, 'title': 'Минск'},
        """
        if "city" in dict_base.keys():
            return City(dict_base["city"]["id"], dict_base["city"]["title"], country)

    def parse_person_data(self, dict_base, faculties, city, organization, schools):
        if dict_base["sex"] == 1:
            sex = "женский"
        elif dict_base["sex"] == 2:
            sex = "мужской"
        else:
            sex = ""

        military = None
        if "military" in dict_base.keys() and len(dict_base["military"]) > 0:
            military = self.get_entity_by_id(dict_base["military"][0]["unit_id"])

        set_groups = set()
        if "groups" in dict_base.keys() and len(dict_base["groups"]) > 0:
            for group in dict_base["groups"]:
                if "id" in group.keys() and "name" in group.keys():
                    set_groups.add(Group(group["id"], group["name"]))

        return Person(dict_base["id"], dict_base["first_name"], dict_base["last_name"], sex,
                      self.__check_dict_key("about", dict_base), self.__check_dict_key("activities", dict_base),
                      self.__check_dict_key("bdate", dict_base), self.__check_dict_key("books", dict_base),
                      faculties, city, organization, schools, military, set_groups)

    def __check_dict_key(self, dict_key, dict_base):
        if dict_key in dict_base.keys():
            return dict_base[dict_key]
        else:
            return ""

    def parse_person_universities(self, dict_base):
        # создаем университет
        list_universities = list()
        list_faculties = list()
        if "universities" in dict_base.keys():
            # создаем университет
            for university in dict_base["universities"]:
                list_universities.append(
                    University(university["id"], university["name"], self.get_entity_by_id(university["city"])))
                # создаем факультет
                if "faculty" in university.keys():
                    list_faculties.append(Faculty(university["faculty"],
                                                  university["faculty_name"], University(university["id"],
                                                                                         university["name"],
                                                                                         self.get_entity_by_id(
                                                                                             university["city"]))))
        return list_faculties, list_universities

    def get_entity_by_id(self, id):
        for person in self.persons:
            if person.id == id:
                return person
        for faculty in self.faculties:
            if faculty.id == id:
                return faculty
        for university in self.universities:
            if university.id == id:
                return university
        for country in self.countries:
            if country.id == id:
                return country
        for city in self.cities:
            if city.id == id:
                return city
        for organization in self.organizations:
            if organization.id == id:
                return organization
        return None

    """
    GETERS
    """

    def get_persons(self):
        return self.persons

    def get_faculties(self):
        return self.faculties

    def get_universities(self):
        return self.universities

    def get_countries(self):
        return self.countries

    def get_cities(self):
        return self.cities

    def get_organizations(self):
        return self.organizations

    def get_schools(self):
        return self.schools

    def get_photos(self):
        return self.photos

    def get_military(self):
        return self.military

    def get_groups(self):
        return self.groups
