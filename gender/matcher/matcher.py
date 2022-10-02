from gender.gender import Gender

class Matcher(object):

    def __init__(self):
        self.gender = Gender()

    def match(self, command):
        return self.gender.get_name(command)

    def match_random(self):
        return self.gender.get_random_name()
        
    def respond(self):
        pass