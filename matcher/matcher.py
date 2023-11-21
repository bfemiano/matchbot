import pickle

from os import path
from random import randint
from time import sleep

from gender.gender import Gender
from age.age import Age
from personality.personality import Personality
from personality.loaders import InterestLoader, TraitLoader
from responder.responder import PersonalityEchoResponder

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
        self.age = Age()
        self.trait_loader = TraitLoader()
        self.interest_loader = InterestLoader()
        self.personality = None

    def match(self, command):
        name, gender = self.gender.get_name(command)
        age = self.age.get_age(command)
        return name, age, gender

    def match_random(self):
        name, gender = self.gender.get_random_name()
        age = self.age.get_random_age()
        return name, age, gender

    def new_personality(self, name, years_old, gender):
        self.personality = Personality(name, years_old, gender, 
                                       disposition=50.0, possible_traits=self.trait_loader.possible_traits, 
                                       possible_interests=self.interest_loader.possible_interests)
        self.responder = self.set_responder()
        
    def save_personality(self):
        if self.personality is None:
            raise NoPersonalityException()

        with open("saved_personality.dat", "wb") as out_file:
            pickle.dump(self.personality, out_file)

    def load_personality(self):
        if not path.exists("saved_personality.dat"):
            raise NoPersonalityException()

        with open("saved_personality.dat", "rb") as in_file:
            self.personality = pickle.load(in_file)
        self.responder = self.set_responder()
        
    def personality_response(self, line: str):
        #slight_delay(self.personality)
        return self.responder.respond(line)
    
    def set_responder(self):
        return PersonalityEchoResponder(personality=self.personality)