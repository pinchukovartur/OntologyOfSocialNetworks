from abc import abstractmethod


class Base:
    def __init__(self, id_entity, name):
        self.name = name
        self.id = id_entity

    def is_consist_in(self, entity_set):
        for entity in entity_set:
            if entity.id == self.id:
                return True
        return False

    @staticmethod
    @abstractmethod
    def get_parents():
        pass

    @staticmethod
    @abstractmethod
    def get_class_name():
        pass


class Person(Base):
    @staticmethod
    def get_class_name():
        return "Person"

    @staticmethod
    def get_parents():
        return ["Faculty"]

    def __init__(self, id_person, name, surname, faculty):
        super().__init__(id_person, name)
        self.surname = surname
        self.faculty = faculty


class Faculty(Base):
    @staticmethod
    def get_class_name():
        return "Faculty"

    @staticmethod
    def get_parents():
        return ["University"]

    def __init__(self, id_faculty, name, university):
        super().__init__(id_faculty, name)
        self.university = university


class University(Base):
    @staticmethod
    def get_class_name():
        return "University"

    @staticmethod
    def get_parents():
        return []

    def __init__(self, id_university, name):
        super().__init__(id_university, name)
