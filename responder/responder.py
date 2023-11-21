from personality.personality import Personality

from openai import OpenAI

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


class GPTResponder(WrapperOutputResponder):
    def __init__(self, personality, *args, **kwargs):
        super(GPTResponder, self).__init__(wrap_count=100, *args, **kwargs)
        self.personality = personality
        self.client = OpenAI()

    def build_prompt(self, user_input: str):
        return f"""
            You are a {self.personality.years_old} years old person named {self.personality.name} 
            talking to someone using an online dating app who identifies as {self.personality.gender}. 

            You are never to break character and let them know you're an AI. 

            Your interests include {', '.join(self.personality.interests)} and your personality traits include
            {', '.join(self.personality.personality_traits)}.

            The person you're talking to using the online dating app has just sent you the following message '{user_input}'

            Respond back in less than 3 sentances in a manner that is consistent with someone talking in an online dating app,
            and also reflects your currenet disposition to them and your above personality traits and interests.
            In the last sentance of your reply, indicate on a scale of 1.0 - 10.0, where 10.0 is the happiest and 1.0 is the saddest, how you felt
            about the statement the person you're chatting with just made to you.
        """

    def build_response_from_input(self, user_input: str) -> str:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.build_prompt()}
                ]
            )
        return completion['choices'][0]['message']['content']