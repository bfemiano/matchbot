class GenericResponder(object):
    def __init__(self, wrap_count):
        self.wrap_count = wrap_count

    def respond(self, line: str) -> str:
        r = "This is a response. Are you sure you like it?"
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