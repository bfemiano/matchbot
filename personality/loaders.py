from nltk.corpus import wordnet

class TraitLoader(object):
    """
        Reads personality traits from file.

        Operations supported over traits.
        1. Detect similiar/duplicate traits in a list.
        2. For a list of traits, figure out which other traits cannot coexist with that list. 
        I.E happy vs. sad.
    """

    def __init__(self):
        self.raw_traits = set()
        with open('data/personality_traits.txt', 'r') as traits_in:
            for line in traits_in.readlines():
                self.raw_traits.add(line.strip('\n').lower())
        deduped_traits = self.dedup_synonyms()
        self.possible_traits = self.map_traits_to_incompatibile_traits(deduped_traits)
        
    def dedup_synonyms(self, syns_func=wordnet.synsets):
        '''
            remove any traits that are symantically the same
        '''
        dups = set()
        for trait in self.raw_traits:
            if trait not in dups:
                for syn in syns_func(trait):
                    for l in syn.lemmas():
                        if l.name().lower() in self.raw_traits and l.name().lower() != trait:
                            dups.add(l.name().lower())
        return self.raw_traits - dups

    
    def map_traits_to_incompatibile_traits(self, deduped_traits: list, syns_func=wordnet.synsets):
        '''
            for each trait, figure out which traits a person would not also have with it (I.E cautious -> risk-taker)
            return a map of trait -> set_of_incompatible_traits
        '''
        trait_to_incompatible_traits = {}
        for trait in deduped_traits:
            if trait not in trait_to_incompatible_traits:
                trait_to_incompatible_traits[trait] = set()
            for syn in syns_func(trait):
                for l in syn.lemmas():
                    if l.antonyms():
                        opposite = l.antonyms()[0].name().lower()
                        if opposite in deduped_traits:
                            trait_to_incompatible_traits[trait].add(opposite)
        return trait_to_incompatible_traits


class InterestLoader(object):
    """
        Randomly generate some interests from preset data.
    """
    def __init__(self):
        with open('data/interests.txt', 'r') as interests_in:
            self.possible_interests = [l.strip('\n') for l in interests_in.readlines()]