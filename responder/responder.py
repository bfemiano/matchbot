from random import randint

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

class WrapperOutputResponder(object):
    """
        Base class that can take any response and format it properly on the command line. 
        subclasses much implement how to build a response.
    """
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
    """
        Simply returns the user input back.
    """
    def build_response_from_input(self, user_input: str) -> str:
        return user_input

class PersonalityDetailsResponder(WrapperOutputResponder):
    """
        Used for debug commands.
    """
    def __init__(self, personality, *args, **kwargs):
        super(PersonalityDetailsResponder, self).__init__(wrap_count=100, *args, **kwargs)
        self.personality = personality


    def build_response_from_input(self, user_input: str) -> str:
        return str(self.personality)


class GPTResponder(WrapperOutputResponder):
    """
        Build a prompt programatically based on the personality attributes.
    """
    def __init__(self, personality, *args, **kwargs):
        super(GPTResponder, self).__init__(wrap_count=100, *args, **kwargs)
        self.personality = personality

    def connect(self):
        from openai import OpenAI
        self.client = OpenAI()

    def build_prompt(self, user_input: str, num_sentances: int, include_emojis: bool):
        '''
            Generate a prompt that creates interesting responses to the user input. 
            Take into account age, gender, interests and how the personality currently
            feels about the user (disposition). Personality libido also plays a random role.
        '''
        traits = self.personality.personality_traits
        prompt = f"""
            You are a {self.personality.years_old} years old person named {self.personality.name} 
            talking to someone using an online dating app.
             
            Your gender identity is {self.personality.gender}.

            You are never to break character and let them know you're an AI. 

            If a few messages have passed between the two of you and you don't know their name, 
            then ask them their name.

            If the last couple messages have been the same, tell the person they're starting to bore you.

            Your interests include {', '.join(self.personality.interests)}.

            On a scale of 0.0 to 100.0, your current disposition of the person you're talking to is {self.personality.disposition}.

            Your replies are not to include as the first sentance the below variations or similiar:
            1. 'Hey there'.
            2. 'Hi'
            3. 'Hey'
            4. 'Hi there'
        """

        if include_emojis:
            prompt += " Include a random number of emojis"
        libido_threshold = randint(1, 10)
        if libido_threshold <= self.personality.libido:
            prompt += \
            """
            Respond in a manner that indicates you are very horny. 
            You are allowed to make suggestive and sexual comments.
            """
        else:
            prompt += \
            f"""
            Respond in a way that is {traits[randint(0, len(traits) -1)]} 
            and reflects your age and is consistent with 
            someone talking using an online dating app.
            """

        prompt += \
        f"""
            Your response back is between 1 and {num_sentances} sentances.
        """
        return prompt

    def build_done_prompt(self, user_input, num_sentances, include_emojis):
        '''
            This prompt function get invoked when the personality is more or less sick of talking to the user.
        '''
        traits = self.personality.personality_traits
        prompt = f"""   
            You are a {self.personality.years_old} years old person named {self.personality.name} 
            talking to someone using an online dating app.
             
            Your gender identity is {self.personality.gender}. 

            You are never to break character and let them know you're an AI. 

            You respond in a way that is {traits[randint(0, len(traits) -1)]} and reflects your age and is consistent with someone
            talking using an online dating app.

            Your replies are not to include as the first sentance the below variations or similiar:
            1. 'Hey there'.
            2. 'Hi'
            3. 'Hey'
            4. 'Hi there'

            You respond back between 1 and {num_sentances}.

            Let the person you're talking to know you're not interested in carrying on the conversation any longer.
        """
        if include_emojis:
            prompt += " Include a random number of emojis."
        return prompt

    def build_wanna_meetup_prompt(self, user_input, num_sentances, include_emojis):
        '''
            This prompt function is invoked when the personality is very fond of the user.
        '''
        traits = self.personality.personality_traits
        prompt = f"""   
            You are a {self.personality.years_old} years old person named {self.personality.name} 
            talking to someone using an online dating app.
             
            Your gender identity is {self.personality.gender}. 

            You are never to break character and let them know you're an AI. 

            You respond in a way that is {traits[randint(0, len(traits) -1)]} and reflects your age and is consistent with someone
            talking using an online dating app.

            Your replies are not to include as the first sentance the below variations or similiar:
            1. 'Hey there'.
            2. 'Hi'
            3. 'Hey'
            4. 'Hi there'

            You respond back between 1 and {num_sentances}.

            Let the person you're talking to know you'd be very much interested in meeting up with them for a date.
            If they have recently responded that they would like to go out with you, don't keep asking them. Remind
            them that they need to setup a date with you.
        """
        if include_emojis:
            prompt += " Include a random number of emojis"
        libido_threshold = randint(1, 10)
        if libido_threshold <= self.personality.libido:
            prompt += " Respond in a manner that indicates you are very horny. You are allowed to talk dirty and make suggestive comments."
        return prompt

    def build_response_from_input(self, user_input: str) -> str:
        if self.personality.disposition >= 30.0:
            prompt_func = self.build_prompt
            if self.personality.disposition >= 80.0:
                prompt_func = self.build_wanna_meetup_prompt
        else:
            prompt_func = self.build_done_prompt
        return self._completion(prompt_func, user_input)

    @retry(wait=wait_random_exponential(max=60), stop=stop_after_attempt(6))
    def _completion(self, prompt_func, user_input):
        num_sentances = randint(1, 4)
        use_emojies = randint(1, 10) < 4 # 30% of the time it works, every time.
        messages = [{"role": "system", "content": prompt_func(user_input, num_sentances, use_emojies)}]
        # disable convo history on responses for now. Rate limiting kicks in quick.
        for user_comment, bot_response in self.personality.conversation_history:
            messages.append({ "role": "user", "content": user_comment })
            messages.append({ "role": "assistant", "content": bot_response })
        messages.append({ "role": "user", "content": user_input })
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages
            )
        return completion.choices[0].message.content