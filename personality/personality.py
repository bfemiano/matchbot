import json
from random import randint
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

class UnableToAssignTraitsException(Exception):
    def __init__(self, num_traits, n_traits_to_select):
        self.msg = """
            The program found %s number of traits, but so many were incompatible it could not randomly assign %s"""\
            % (num_traits, n_traits_to_select)

def expontential_moving_average(current, new_reading, n):
    g1 = 2 / (1 + n)
    g2 = 1 - g1
    return (g1 * new_reading) + (g2 * current) 


class Personality():

    def __init__(self, name: str, years_old: int, gender: str, disposition: float, 
                 possible_traits: list(), possible_interests: list(), n_traits=5, n_interests=5):
        self.name = name
        self.years_old = years_old
        self.gender = gender
        self.disposition = disposition
        self.n_disposition_updates = 1 # init to 1 based on default disposition.
        self.personality_traits = self.assign_random_traits(possible_traits, n_select=n_traits)
        self.interests = self.assign_random_interests(possible_interests, n_select=n_interests)
        self.memories = []

    def __str__(self):
        l1 = f"{self.name}. {self.years_old} years old. Identifes as {self.gender}. "
        l2 = f"I am {', '.join(self.personality_traits)}. "
        l3 = f"I like {', '.join(self.interests)} "
        l4 = f"disposition: {self.disposition} "
        return l1 + l2 + l3 + l4
        

    def assign_random_traits(self, possible_traits, n_select):
        '''
            Select 'n' number of random traits based on n_select. Return as a list
            Once a trait has been selected, avoid any traits listed as incompatible with it, 
            and do not count an incompatible trait towards the n_selected total random trait count. 

            If we run out of available traits before reaching n_selected total random traits,
            raise an error.
        '''
        random_traits = set()
        trait_keys = set(possible_traits.keys())
        starting_num_trait_keys = len(trait_keys)
        i = 0
        while i < n_select:
            random_trait = list(trait_keys)[randint(0, len(trait_keys) - 1)]
            has_trait_conflict = False
            for incompatible_trait in possible_traits[random_trait]:
                if incompatible_trait in random_traits:
                    if incompatible_trait in trait_keys:
                        trait_keys.remove(incompatible_trait) 
                    has_trait_conflict = True
            if not has_trait_conflict:
                random_traits.add(random_trait)
                i += 1
            trait_keys.remove(random_trait)
            if len(trait_keys) == 0 and i < n_select:
                raise UnableToAssignTraitsException(starting_num_trait_keys, n_select)
        return list(random_traits)

    def assign_random_interests(self, possible_interests, n_select=5):
        '''s
            Select 'n' number of random interests from possible_interests.
        '''
        random_interests = []
        cur_available_set= set(possible_interests)
        for i in range(n_select):
            cur_available = list(cur_available_set)
            r_interest = cur_available[randint(0, len(cur_available) - 1)]
            cur_available_set.remove(r_interest)
            random_interests.append(r_interest)
        return random_interests

    def update_disposition(self, disposition):
        self.n_disposition_updates += 1
        self.disposition = expontential_moving_average(self.disposition, disposition, self.n_disposition_updates)
        return self.disposition


class GPTBackstoryPersonality():
    """
        Try out using OpenAI to randomly create a backstory, personality traits, and interests.
    """
    def __init__(self, years_old: int, gender: str, disposition: float):
        self.years_old = years_old
        self.gender = gender
        self.disposition = disposition
        self.n_disposition_updates = 1 # init to 1 based on default disposition.
        self.n_traits = randint(2, 5)
        self.n_interests = randint(2, 7)

    def update_disposition(self, disposition):
        self.n_disposition_updates += 1
        self.disposition = expontential_moving_average(self.disposition, disposition, self.n_disposition_updates)
        return self.disposition
    
    def get_prompt(self):
        prompt = f"""
            Randomly generate {self.n_traits} personality traits that a person would have. Make
            the traits and assortment of both positive and negative qualities.

            Randomly generate a name that matches a {self.years_old} person who identifies
            as a {self.gender}. The name should be first name only. Never include a last name.
            
            Make sure the personality traits do not conflict with each other. 
            For example a person cannot be both 'cautious' and 'careless'.

            Make sure the personality traits are not duplicative of each other.
            For example a person cannot be both 'angry' and 'mad'.
             
            Also randomly generate {self.n_interests} interests that a a {self.years_old} person would
            reasonably have given their age.

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
    
    @retry(wait=wait_random_exponential(max=60), stop=stop_after_attempt(6))
    def complete(self, client):
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": self.get_prompt()}
                ]
            )
        return completion.choices[0].message.content
    
    def load(self):
        from openai import OpenAI
        client = OpenAI()
        data = json.loads(self.complete(client))
        self.name = data['name']
        self.personality_traits = data['p_traits']
        self.interests = data['interests']
        self.memories = data['memories']

    def __str__(self):
        l1 = f"{self.name}. {self.years_old} years old. Identifes as {self.gender}. "
        l2 = f"I am {', '.join(self.personality_traits)}. "
        l3 = f"I like {', '.join(self.interests)} "
        l4 = f"disposition: {self.disposition} "
        l5 = f"memories: {self.memories} "
        return l1 + l2 + l3 + l4 + l5