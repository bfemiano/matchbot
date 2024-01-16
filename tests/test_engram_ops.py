
from personality.personality import Personality
from personality.engram_ops import load_from_engram, save_as_engram

def test_save_engram():
    # 1. generate a personality object. 
    # 2. save to engram.
    # 3. load a personality from the engram and see if it matches field by field with the step 1 obj.
    personality = Personality(name='test_name',
                              years_old=20,
                              gender='n',
                              disposition=50.0,
                              possible_traits={}, possible_interests=[])
    personality.libido = 2
    personality.n_disposition_updates = 10
    personality.personality_traits = ['angry', 'interesting']
    personality.interests = ['table tennis', 'rowboating']
    personality.conversation_history = [('hey whats up?', 'nothing much')]
    engram = save_as_engram(personality)
    recovered = load_from_engram(engram)
    assert personality.name == recovered.name
    assert personality.years_old == recovered.years_old
    assert personality.gender == recovered.gender
    assert personality.disposition == recovered.disposition
    assert personality.libido == recovered.libido
    assert personality.n_disposition_updates == recovered.n_disposition_updates
    assert personality.personality_traits == recovered.personality_traits
    assert personality.interests == recovered.interests
    assert personality.conversation_history == recovered.conversation_history    