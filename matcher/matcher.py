import pickle

from os import path
from random import randint
from time import sleep

from gender.gender import Gender
from personality.personality import Personality

class NoPersonalityException(Exception):
    pass

def slight_delay(name): # TODO abstract this away
    delay = randint(1, 2)
    print("\t\t<%s has received your message>" % name)
    sleep(delay)
    delay = randint(5, 10)
    print("\t\t<%s is thinking of what to say>" % name)
    sleep(delay)
    delay = randint(3, 5)
    print("\t\t<%s is responding>" % name)
    sleep(delay)

class Matcher(object):

    def __init__(self):
        self.gender = Gender()
        self.personality = None

    def match(self, command):
        return self.gender.get_name(command)

    def match_random(self):
        return self.gender.get_random_name()

    def new_personality(self, name):
        self.personality = Personality(name)

    def save_personality(self):
        if self.personality is None:
            raise NoPersonalityException()

        with open("personality.dat", "wb") as out_file:
            pickle.dump(self.personality, out_file)

    def load_personality(self):
        if not path.exists("personality.dat"):
            raise NoPersonalityException()

        with open("personality.dat", "rb")as in_file:
            self.personality = pickle.load(in_file)
        
    def personality_response(self, line: str):
        slight_delay(self.personality)
        return self.personality.respond(line)