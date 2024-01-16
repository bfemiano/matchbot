from random import randint 

class UnsupportedAgeCommandException(Exception):
    def __init__(self, msg):
        self.msg = msg

class Age():
    """
        Parse age from the match command. Supports randomly generating an age within a range.
        If the user enters an age outside the allowable range then an error occurs.
    """

    def get_age(self, command: str):
        parts = command.split(" ")
        if len(parts) < 3:
            return self._random_age_from(18, 100)
        lower, upper = self._parse(parts[2])
        return self._random_age_from(lower, upper)

    def get_random(self):
        return self._random_age_from(18, 100)
        
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
        