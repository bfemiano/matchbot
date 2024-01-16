from personality.personality import Personality

class PersonalityEngram():
    """
        For saving and recovering personality instances with convo history. 
        
        This is preferrable to persisting instance of Personality objects, since
        those are subject to code changes that can engrams backwards incompatible when
        loading.
    """
    def __init__(self, name: str, years_old: int, gender: str, disposition: float, libido: int, 
                 n_disposition_updates: int, personality_traits: list, 
                 interests: list, conversation_history: list):
        self.name = name
        self.years_old = years_old
        self.gender = gender
        self.disposition = disposition
        self.libido = libido
        self.n_disposition_updates = n_disposition_updates
        self.personality_traits = personality_traits
        self.interests = interests
        self.conversation_history = conversation_history

def load_from_engram(engram: PersonalityEngram):
    personality = Personality(name=engram.name,
                              years_old=engram.years_old,
                              gender=engram.gender,
                              disposition=engram.disposition,
                              possible_traits={}, possible_interests=[])
    personality.libido = engram.libido
    personality.n_disposition_updates = engram.n_disposition_updates
    personality.personality_traits = engram.personality_traits
    personality.interests = engram.interests
    personality.conversation_history = engram.conversation_history
    return personality

def save_as_engram(personality: Personality):
    return PersonalityEngram(
        name=personality.name,
        years_old=personality.years_old,
        gender=personality.gender,
        disposition=personality.disposition,
        n_disposition_updates=personality.n_disposition_updates,
        libido=personality.libido,
        personality_traits=personality.personality_traits,
        interests=personality.interests,
        conversation_history=personality.conversation_history)