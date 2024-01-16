import json
from random import randint
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff


def expontential_moving_average(current, new_reading, n):
    g1 = 2 / (1 + n)
    g2 = 1 - g1
    return (g1 * new_reading) + (g2 * current) 

class PersonalityEngram():
    """
        For saving/loading. That way if behavior is changed/added in GPTPersonality
        previous personalities can still be reloaded. 
    """
    def __init__(self, years_old: int, gender: str, disposition: float, libido: int, 
                 name: str, personality_traints: list, interests: list, memories: list,
                 conversation_history: list):
        self.years_old = years_old
        self.gender = gender
        self.disposition = disposition
        self.libido = libido
        self.name = name
        self.personality_traits = personality_traints
        self.interests = interests
        self.memories = memories
        self.conversation_history = conversation_history

class GPTBackstoryPersonality():
    """
        Try out using OpenAI to randomly create a backstory, personality traits, and interests.
    """
    def __init__(self, years_old: int, gender: str, disposition: float):
        self.years_old = years_old
        self.gender = gender
        self.disposition = disposition
        self.libido = randint(1, 10)
        self.n_disposition_updates = 1 # init to 1 based on default disposition.
        self.n_traits = randint(2, 5)
        self.n_interests = randint(2, 7)
        self.conversation_history = []

    def update_disposition(self, disposition):
        self.n_disposition_updates += 1
        self.disposition = expontential_moving_average(self.disposition, disposition, self.n_disposition_updates)
        return self.disposition
    
    def get_generation_prompt(self):
        prompt = f"""
            Randomly generate {self.n_traits} personality traits that a person would have. Make
            the traits and assortment of both positive and negative qualities.

            Randomly generate a name that matches a {self.years_old} person who identifies
            as a {self.gender}. The name should be first name only. Never include a last name.
            
            Make sure the personality traits do not conflict with each other. 
            For example a person cannot be both 'cautious' and 'careless'.

            Make sure the personality traits are not duplicative of each other.
            For example a person cannot be both 'angry' and 'mad'.
             
            Also randomly generate {self.n_interests} interests that a {self.years_old} person would
            reasonably have given their age. Pick a few interests that are a eclectic and interesting.

            For this person, take into account the fact that they are a {self.years_old} person who identifies
            as a {self.gender} and also their personality traits and interests to 
            create several memories they have accumulated throughout life. A few should be positive
            memories a few negative memories where a life lesson was learned.

            Generate the memories in the first person.

            Respond only with a JSON object containing the above. Make the keys
            name, p_traits where p_traints is an array, interests where interests are an array, 
            and memories where memories contains an array of memories.
        """
        return prompt
    
    def get_welcome_back_prompt(self):
        prompt = f"""
            Reply back in a manner that indicates how excited you are
            to talk to this person after not hearing from them for awhile. 

            If you know their name from the conversation chat history, include it in the response.
        """
        if randint(1, 10) > 7:
            prompt += " Include a random number of emojis"
        return prompt
    
    @retry(wait=wait_random_exponential(max=60), stop=stop_after_attempt(6))
    def complete(self, client, prompt: str, use_json=True):
        messages = [{"role": "system", "content": prompt}]
        for user_comment, bot_response in self.conversation_history:
            messages.append({ "role": "user", "content": user_comment })
            messages.append({ "role": "assistant", "content": bot_response })
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" } if use_json else None,
            messages=messages,
            )
        return completion.choices[0].message.content
    
    def load(self):
        from openai import OpenAI
        client = OpenAI()
        data = json.loads(self.complete(client, self.get_generation_prompt()))
        self.name = data['name']
        self.personality_traits = data['p_traits']
        self.interests = data['interests']
        self.memories = data['memories']

    def greeting_msg(self):
        from openai import OpenAI
        client = OpenAI()
        return self.complete(client, self.get_welcome_back_prompt(), use_json=False)
    
    def remember_comment(self, comment):
        self.conversation_history.append(comment)
    
    def __str__(self):
        l1 = f"{self.name}. {self.years_old} years old. Identifes as {self.gender}. "
        l2 = f"My libido on a scale of 1 - 10 is {self.libido}. "
        l3 = f"I am {', '.join(self.personality_traits)}. "
        l4 = f"I like {', '.join(self.interests)} "
        l5 = f"disposition: {self.disposition} "
        l6 = "memories:"
        return l1 + l2 + l3 + l4 + l5 + '\n'.join(self.memories)
    
def load_from_engram(engram: PersonalityEngram):
    personality = GPTBackstoryPersonality(years_old=engram.years_old, gender=engram.gender, disposition=engram.disposition)
    personality.libido = engram.libido
    personality.name = engram.name
    personality.personality_traits = engram.personality_traits
    personality.interests = engram.interests
    personality.memories = engram.memories
    personality.conversation_history = engram.conversation_history
    return personality

def save_as_engram(personality: GPTBackstoryPersonality):
    return PersonalityEngram(
        years_old=personality.years_old, 
        gender=personality.gender, 
        disposition=personality.disposition, 
        name=personality.name,
        libido=personality.libido,
        personality_traints=personality.personality_traits, 
        interests=personality.interests,
        memories=personality.memories,
        conversation_history=personality.conversation_history)