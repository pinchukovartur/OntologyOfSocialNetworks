from utils.vk_models import University, Faculty, Person, Country, City, Organization, School


class Parser:
    def __init__(self):
        """
        Инициализация множест сущностей
        """
        self.persons = set()
        self.faculties = set()
        self.universities = set()
        self.countries = set()
        self.cities = set()
        self.organizations = set()
        self.schools = set()

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
        # создаем человека
        list_faculties, list_universities = self.parse_person_universities(dict_base)

        country = self.parse_country(dict_base)
        city = self.parse_city(dict_base, country)

        organization = self.parse_organization(dict_base)
        schools = self.parse_school(dict_base)
        person = self.parse_person_data(dict_base, list_faculties, city, organization, schools)

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

    def get_set_entities(self):
        return self.persons, self.faculties, self.universities, self.countries, self.cities, self.organizations, self.schools

    def parse_person_data(self, dict_base, faculties, city, organization, schools):
        if dict_base["sex"] == 1:
            sex = "женский"
        elif dict_base["sex"] == 2:
            sex = "мужской"
        else:
            sex = ""
        return Person(dict_base["id"], dict_base["first_name"], dict_base["last_name"], sex,
                      self.__check_dict_key("about", dict_base), self.__check_dict_key("activities", dict_base),
                      self.__check_dict_key("bdate", dict_base), self.__check_dict_key("books", dict_base),
                      faculties, city, organization, schools)

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
                print(university)
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
