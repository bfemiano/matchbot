from random import randint

from personality.personality import Personality

from nltk.tokenize import sent_tokenize, word_tokenize

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

    
class EchoResponder(WrapperOutputResponder):
    
    def build_response_from_input(self, user_input: str) -> str:
        return user_input

class PersonalityDetailsResponder(WrapperOutputResponder):

    def __init__(self, personality, *args, **kwargs):
        super(PersonalityDetailsResponder, self).__init__(wrap_count=100, *args, **kwargs)
        self.personality = personality


    def build_response_from_input(self, user_input: str) -> str:
        return str(self.personality)


class GPTResponder(WrapperOutputResponder):
    def __init__(self, personality, *args, **kwargs):
        super(GPTResponder, self).__init__(wrap_count=100, *args, **kwargs)
        self.personality = personality
        self.system_prompt = f"""
            You are a {self.personality.years_old} years old person named {self.personality.name} 
            talking to someone using an online dating app who identifies as {self.personality.gender}. 

            You are never to break character and let them know you're an AI. 

            Your interests include {', '.join(self.personality.interests)} and your personality traits include
            {', '.join(self.personality.personality_traits)}.

            On a scale of 1 to 100 your current disposition of this person is {self.personality.disposition}.
        """

    def connect(self):
        from openai import OpenAI
        self.client = OpenAI()

    def build_prompt(self, user_input: str, num_sentances: int, include_emojis: bool):

        prompt =  f"""
            The person you're talking to using the online dating app has just sent you the following message '{user_input}'.

            Respond back using between 1 and {num_sentances} sentances in a manner that reflects your age and
            is consistent with someone talking in an online dating app,
            and also reflects your current disposition to them and your above personality traits and interests.
            The last sentance of your reply should be a single number between 0 and 100,
            where 100 is the happiest and 0 is the saddest, how you felt about the 
            statement the person you're chatting with just made to you.
        """
        if include_emojis:
            prompt += " Include lots of emojis"
        return prompt

    def build_done_prompt(self, user_input, num_sentances, include_emojis):
        prompt = f"""   
            You're talking to a person using the online dating app.

            Let the person you're talking to know you're not interested in carrying on the conversation any longer.

            Use {num_sentances} and your personality traits to formulate the response.
        """
        if include_emojis:
            prompt += " Include lots of emojis"
        return prompt

    def build_wanna_meetup_prompt(self, user_input, num_sentances, include_emojis):
        prompt = f"""
            Let the person you're talking to know you'd be very much interested in meeting up with them for a date.

            Use {num_sentances} and your personality traits to formulate the response.
        """
        if include_emojis:
            prompt += " Include lots of emojis"
        return prompt

    def build_response_from_input(self, user_input: str) -> str:
        if self.personality.disposition >= 30.0:
            prompt_func = self.build_prompt
            if self.personality.disposition >= 80.0:
                prompt_func = self.build_wanna_meetup_prompt
            response = self._completion(prompt_func, user_input)
            disposition, index = self.get_disposition(response)
            if disposition is not None:
                self.personality.update_disposition(disposition)
                self.response_minus_disposition(response, index)
            return response
        else:
            response = self._completion(self.build_done_prompt, user_input)
            disposition = randint(0, 19)
            so_youre_saying_theres_a_chance = randint(0, 100) < 10 # small chance of recovery
            if so_youre_saying_theres_a_chance:
                self.personality.update_disposition(35)
            else:
                self.personality.update_disposition(disposition)
            return response

    def _completion(self, prompt_func, user_input):
        num_sentances = randint(2, 6)
        use_emojies = randint(1, 10) < 4 # 30% of the time it works, every time.
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt_func(user_input, num_sentances, use_emojies)}
                ]
            )
        return completion.choices[0].message.content
        
    def get_disposition(self, content):
        sentances = sent_tokenize(content)
        disposition = None
        for i, s in enumerate(reversed(sentances)):
            words = word_tokenize(s)
            for word in words:
                try:
                    if word.endswith(".0") or word.endswith(".0."):
                        word = word[0:-1]
                        disposition = int(float(word))
                        return disposition, (len(sentances)-1) - i
                except ValueError:
                    pass
        return disposition, -1

    def response_minus_disposition(self, content, index):
        sentances = sent_tokenize(content)
        return ' '.join([s for i, s in enumerate(sentances) if i != index])