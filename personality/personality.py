
from personality.responder import GenericResponder, GPTResponder, PersonalityEchoResponder
from random import randint

class UnableToAssignTraitsException(Exception):
    def __init__(self, num_traits, n_traits_to_select):
        self.msg = """
            The program found %s number of traits, but so many were incompatible it could not randomly assign %s"""\
            % (num_traits, n_traits_to_select)

class Personality():

    def __init__(self, name, possible_traits, possible_interests, n_traits=5, n_interests=5):
        self.name = name
        self.libido = randint(1, 10)
        self.personality_traits = self.assign_random_traits(possible_traits, n_select=n_traits)
        self.interests = self.assign_random_interests(possible_interests, n_select=n_interests)
        self.responder = PersonalityEchoResponder(name, self.libido, self.interests, self.personality_traits)

    def __str__(self):
        return self.name

    def respond(self, line):
        return self.responder.respond(line)

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