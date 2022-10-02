
from personality.responder import GenericResponder

class Personality():

    def __init__(self, name):
        self.name = name
        self.responder = GenericResponder(wrap_count=80)

    def __str__(self):
        return self.name

    def respond(self, line):
        return self.responder.respond(line)