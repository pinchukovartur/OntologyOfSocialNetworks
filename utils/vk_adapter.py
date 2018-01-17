from utils.vk_models import University, Faculty, Person


class Parser:
    def __init__(self):
        """
        Инициализация множест сущностей
        """
        self.persons = set()
        self.faculties = set()
        self.universities = set()


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

        person = None
        faculty = None
        university = None

        # создаем университет
        if "universities" in dict_base.keys():
            for university_dict in dict_base["universities"]:
                # создаем университет
                university = University(university_dict["id"], university_dict["name"])
                # создаем факультет
                if "faculty" in university_dict.keys():
                    faculty = Faculty(university_dict["faculty"], university_dict["faculty_name"], university)

        # создаем человека
        person = Person(dict_base["id"], dict_base["first_name"], dict_base["last_name"], faculty)

        if not person.is_consist_in(self.persons) and person is not None:
            self.persons.add(person)
        if not faculty.is_consist_in(self.faculties) and faculty is not None:
            self.faculties.add(faculty)
        if not university.is_consist_in(self.universities) and university is not None:
            self.universities.add(university)



        return self.persons, self.faculties, self.universities
