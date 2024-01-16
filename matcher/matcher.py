import pickle

from os import path
from time import sleep

from gender.gender import Gender
from age.age import Age
from personality.personality import Personality
from personality.engram_ops import save_as_engram, load_from_engram
from personality.loaders import InterestLoader, TraitLoader
from responder.responder import EchoResponder, PersonalityDetailsResponder, GPTResponder

class NoPersonalityException(Exception):
    pass

class UnmatchedException(Exception):
    pass

class UnableToFindMatchException(Exception):
    pass

class Matcher(object):
    """
        Allows for seperation of concerns between the personality and responder operations.
        Also allows the user interaction with the shell to be abstracted away from the personality
        directly. This mimics the dating app platform itself in a sense. 

        Primary operations
            1. Parsing match commands and constructing a personality instance.
            2. Save/Load operations around personality engrams for persistence.
            3. Forwarding user input to the personality and returning the response. Also unmatching 
            if the personality's disposition to the user is low enough.
            4. Debug commands.
    """

    def __init__(self):
        self.gender = Gender()
        self.age = Age()
        self.trait_loader = TraitLoader()
        self.interest_loader = InterestLoader()
        self.personality = None
        self.responder = None

    def match(self, command: str):
        name, gender = self.gender.get_name(command)
        age = self.age.get_age(command)
        return name, age, gender

    def match_random(self):
        items = self.gender.get_random()
        age = self.age.get_random()
        return items[0], age, items[1]

    def new_personality(self, line):
        name, years_old, gender = self.match(line)
        self._new_personality(name, years_old, gender)
    
    def new_random_personality(self):
        (name, years_old, gender) = self.match_random()
        self._new_personality(name, years_old, gender)

    def _new_personality(self, name, years_old, gender):
        default_dispostion = 50.0 if gender == 'm' else 35.0
        self.personality = Personality(name, years_old, gender, 
                                       disposition=default_dispostion, possible_traits=self.trait_loader.possible_traits,
                                       possible_interests=self.interest_loader.possible_interests)
        self.responder = self.set_responder()
        
    def save_personality(self):
        if self.personality is None:
            raise NoPersonalityException()

        with open("saved_personality.dat", "wb") as out_file:
            pickle.dump(save_as_engram(self.personality), out_file)

    def load_personality(self):
        if not path.exists("saved_personality.dat"):
            raise NoPersonalityException()

        with open("saved_personality.dat", "rb") as in_file:
            engram = pickle.load(in_file)
            self.personality = load_from_engram(engram)
        self.responder = self.set_responder()

    def welcome_back(self):
        #print("\t\tHi there! This is %s. It's great to see you again!" % matcher.personality.name)
        return EchoResponder().respond(self.personality.greeting_msg())
        
    def personality_response(self, line: str):
        response = self.responder.respond(line)
        self.personality.remember_exchange((line.strip(), response.strip()))
        if self.personality.disposition < 20.0:
            raise UnmatchedException()
        return response
    
    def debug_personality_response(self, personality: Personality, line: str):
        return PersonalityDetailsResponder(personality).respond(line)
    
    def set_responder(self):
        responder = GPTResponder(personality=self.personality)
        responder.connect()
        return responder