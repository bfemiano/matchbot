
from personality.responder import GenericResponder, GPTResponder, PersonalityEchoResponder
from random import randint

class UnableToAssignTraitsException(Exception):
    def __init__(self, num_traits, n_traits_to_select):
        self.msg = """
            The program found %s number of traits, but so many were incompatible it could not randomly assign %s"""\
            % (num_traits, n_traits_to_select)

class Personality():

    def __init__(self, name, possible_traits, possible_interests):
        self.name = name
        self.libido = randint(1, 10)
        self.personality_traits = self.assign_random_traits(possible_traits)
        self.interests = self.assign_random_interests(possible_interests)
        self.responder = PersonalityEchoResponder(name, self.libido, self.interests, self.personality_traits)

    def __str__(self):
        return self.name

    def respond(self, line):
        return self.responder.respond(line)

    def assign_random_traits(self, possible_traits, n_traits_to_select=5):
        # TODO write unit test for this.
        random_traits = set()
        trait_keys = set(possible_traits.keys())
        attempt = 1
        num_traits = len(trait_keys)
        i = 0
        while i < n_traits_to_select and attempt < num_traits:
            random_trait = list(trait_keys)[randint(0, len(trait_keys))]
            has_trait_conflict = False
            for incompatible_trait in possible_traits[random_trait]:
                if incompatible_trait in random_traits: # have we already assigned a trait to which this newly selected trait is incompatible with?
                    trait_keys.remove(incompatible_trait) # prevent known incompatible from random selection in future iterations.
                    has_trait_conflict = True
            if not has_trait_conflict:
                random_traits.add(random_trait)
                i += 1
            trait_keys.remove(random_trait)
            attempt += 1
        if attempt == num_traits:
            raise UnableToAssignTraitsException(num_traits, n_traits_to_select)
        return list(random_traits)

    def weight_each_trait(self, traits):
        # assign each trait a random number between 1 - 100 of how much it dominates their personality.  Subtract that number from 100, then repeat again
        # with the new upper-bound. Do this until the last trait. 
        # so let's say with ['ambitious', 'cautious'] it generates between 1 - 100 an ambitious =30, for cautius it will not generate between 1 - 70,
        # rinse,repeat until there is only 1 left.

        # TODO write unit test for this.
        pass

    def assign_random_interests(self, possible_interests, n_interests=5):
        #TODO just pick a few at random. No need to dedup.
        return []