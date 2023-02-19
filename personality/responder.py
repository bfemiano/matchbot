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
        return "This is a response. Are you sure you like it?"

class PersonalityEchoResponder(WrapperOutputResponder):

    def __init__(self, name, libido, interests, personality_traits, *args, **kwargs):
        super(PersonalityEchoResponder, self).__init__(wrap_count=180, *args, **kwargs)
        self.name = name
        self.libido = libido
        self.interests = interests
        self.personality_traits = personality_traits

    def build_response_from_input(self, user_input: str) -> str:
        return """
            My name is {name} and I have the following characteristics {interests} {personality_traits} {libido}
        """.format(name=self.name, interests=self.interests, 
                   personality_traits=self.personality_traits, libido=self.libido)


class GPTResponder(WrapperOutputResponder):
    pass