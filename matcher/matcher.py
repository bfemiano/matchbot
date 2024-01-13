import pickle

from os import path
from time import sleep

from gender.gender import Gender
from age.age import Age
from personality.personality import Personality, GPTBackstoryPersonality
from responder.responder import PersonalityDetailsResponder, GPTResponder

class NoPersonalityException(Exception):
    pass

class UnmatchedException(Exception):
    pass

class UnableToFindMatchException(Exception):
    pass

class Matcher(object):

    def __init__(self):
        self.gender = Gender()
        self.age = Age()
        self.personality = None
        self.responder = None

    def match(self, command):
        gender = self.gender.get(command)
        age = self.age.get_age(command)
        return age, gender

    def match_random(self):
        gender = self.gender.get_random()
        age = self.age.get_random()
        return age, gender

    def new_personality(self, line):
        years_old, gender = self.match(line)
        self._new_personality(years_old, gender)
    
    def new_random_personality(self):
        (years_old, gender) = self.match_random()
        self._new_personality(years_old, gender)

    def _new_personality(self, years_old, gender):
        default_dispostion = 50.0 if gender == 'm' else 35.0
        self.personality = GPTBackstoryPersonality(years_old, gender, disposition=default_dispostion)
        max_attempts = 5
        i = 0
        done = False
        while i < max_attempts and not done:
            try:
                self.personality.load()
                done = True
            except Exception as e:
                i += 1
        if not done:
            raise UnableToFindMatchException()
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
        response = self.responder.respond(line)
        if self.personality.disposition < 20.0:
            raise UnmatchedException()
        return response
    
    def debug_personality_response(self, personality: Personality, line: str):
        return PersonalityDetailsResponder(personality).respond(line)
    
    def set_responder(self):
        responder = GPTResponder(personality=self.personality)
        responder.connect()
        return responder