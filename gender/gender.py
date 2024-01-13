from random import randint

class UnsupportedGenderCommandException(Exception):
    def __init__(self):
        self.msg = "Gender must be either m (male), f (female), or n (nonbinary)"
        

class Gender:

    def __init__(self):
        self.gender_types = ['f', 'n', 'm']

    def get(self, command):
        parts = command.split(" ")
        if len(parts) < 2:
            raise UnsupportedGenderCommandException()
        if parts[1] not in set(self.gender_types):
            raise UnsupportedGenderCommandException()
        return parts[1]

    def get_random(self):
        return self.gender_types[randint(0, len(self.gender_types) - 1)]