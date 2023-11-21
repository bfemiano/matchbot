from personality.personality import Personality

class WrapperOutputResponder(object):
    def __init__(self, wrap_count=80):
        self.wrap_count = wrap_count

    def build_response_from_input(self, user_input: str) -> str:
        raise NotImplementedError

    def respond(self, user_input: str) -> str:
        r = self.build_response_from_input(user_input)
        response = [] 
        c = 0
        response.append("\t\t")
        for word in r.split(" "):
            if c >= self.wrap_count:
                c = 0
                response.append("\n\t\t")
            c += len(word) + 1 # space
            response.append(word)
        return " ".join(response)


class GenericResponder(WrapperOutputResponder):
    
    def build_response_from_input(self, user_input: str) -> str:
        return "This is a response from the Generic Responder."

class PersonalityEchoResponder(WrapperOutputResponder):

    def __init__(self, personality, *args, **kwargs):
        super(PersonalityEchoResponder, self).__init__(wrap_count=100, *args, **kwargs)
        self.personality = personality


    def build_response_from_input(self, user_input: str) -> str:
        return str(self.personality)


class GPTResponder(WrapperOutputResponder): # TODO. Fun part.
    pass