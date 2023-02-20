from nltk.corpus import names
from random import randint 

class UnsupportedGenderCommandException(Exception):
    def __init__(self):
        self.msg = "Must be either 'woman', 'man', or 'nonbinary'"
        

class Gender:

    def __init__(self):
        self.gender_types = ["woman", "man", "nonbinary"]
        self.male_names = names.words('male.txt')
        self.female_names = names.words('female.txt')
        self.nonbinary_names = []
        with open("data/nonbinary_names.txt", 'r') as nonbinary_names:
            for line in nonbinary_names.readlines():
                self.nonbinary_names.append(line.strip("\n"))

    def get_name(self, gender_command):
        parts = gender_command.split(" ")
        if len(parts) <= 1:
            raise UnsupportedGenderCommandException()
        return self._get_name(parts[1])

    def get_random_name(self):
        return self._get_name(self.gender_types[randint(0, 2)])

    def _get_name(self, gender:str) -> str:
        if gender == "woman":
            return self.female_names[randint(0, len(self.female_names))]
        elif gender == "man":
            return self.male_names[randint(0, len(self.male_names))]
        elif gender == "nonbinary":
            return self.nonbinary_names[randint(0, len(self.nonbinary_names))]
        else:
            raise UnsupportedGenderCommandException()