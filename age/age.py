from random import randint 

class UnsupportedAgeCommandException(Exception):
    def __init__(self, msg):
        self.msg = msg

class Age():

    def get_age(self, command):
        parts = command.split(" ")
        if len(parts) < 3:
            age = randint(18, 100)
            return age
        lower, upper = self._parse(parts[2])
        age = self._random_age_from(lower, upper)
        return age

        
    def _parse(self, age_arg):
            parts = age_arg.split("-")
            if len(parts) < 2:
                return parts[0], parts[0]
            return parts[0], parts[1]
    
    def _random_age_from(self, lower, upper):
        try:
            lower = int(lower)
            upper = int(upper)
            if lower < 18:
                raise UnsupportedAgeCommandException("Age not supported because too young.")
            elif upper > 100:
                raise UnsupportedAgeCommandException("Ages greater than 100 not supported at this time.")
            return randint(lower, upper)
        except ValueError:
            raise UnsupportedAgeCommandException("Invalid age or age range. Supported examples: 25, 18-25.")
        