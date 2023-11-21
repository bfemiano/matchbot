import pickle

from os import path
from random import randint
from time import sleep

from gender.gender import Gender
from age.age import Age
from personality.personality import Personality
from personality.loaders import InterestLoader, TraitLoader
from responder.responder import PersonalityEchoResponder, GPTResponder

class NoPersonalityException(Exception):
    pass

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
        return self.responder.respond(line)
    
    def debug_personality_response(self, personality: Personality, line: str):
        return PersonalityEchoResponder(personality).respond(line)
    
    def set_responder(self):
        return GPTResponder(personality=self.personality)