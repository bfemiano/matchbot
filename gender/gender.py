from nltk.corpus import names
from random import randint

class UnsupportedGenderCommandException(Exception):
    def __init__(self):
        self.msg = "Must be either m, f, or n (nonbinary)"
        

class Gender:

    def __init__(self):
        self.gender_types = ["f", "n", "b"]
        self.male_names = names.words('male.txt')
        self.female_names = names.words('female.txt')
        self.nonbinary_names = []
        with open("data/nonbinary_names.txt", 'r') as nonbinary_names:
            for line in nonbinary_names.readlines():
                self.nonbinary_names.append(line.strip("\n"))

    def get_name(self, command):
        parts = command.split(" ")
        if len(parts) < 2:
            raise UnsupportedGenderCommandException()
        return self._get_name(parts[1])

    def get_random_name(self):
        return self._get_name(self.gender_types[randint(0, len(self.gender_types) - 1)])

    def _get_name(self, gender:str) -> str:
        if gender == "f":
            return self.female_names[randint(0, len(self.female_names) - 1)], gender
        elif gender == "m":
            return self.male_names[randint(0, len(self.male_names) - 1)], gender
        elif gender == "n":
            return self.nonbinary_names[randint(0, len(self.nonbinary_names) - 1)], gender
        else:
            raise UnsupportedGenderCommandException()