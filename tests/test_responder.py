import pytest
from personality.personality import Personality
from responder.responder import GPTResponder


class FakeGPTResponder(GPTResponder):

    def __init__(self, personality, *args, **kwargs):
        super(FakeGPTResponder, self).__init__(personality, *args, **kwargs)

    def complete(self, prompt_func, user_input, use_history=False, use_json=False):
        response = prompt_func(1, False)
        if response.strip().find("Respond in a way that is") > 0:
            return "hey!"
        elif response.strip().find("Respond in a manner that indicates you are very horny") > 0:
            return "horny!"
        elif response.strip().find("not interested in carrying on the conversation any longer.") > 0:
            return "im done"
        elif response.strip().find("very much interested in meeting up") > 0:
            return "lets hang out."
        raise Exception()

@pytest.fixture
def low_disposition_responder():
    possible_traits = {
        'happy': set(['sad']),
        'sad': set(['happy']),
        'smart': set()
    }
    personality = Personality(name='test_name', years_old=25, gender='m', disposition=21.0,
                       possible_traits=possible_traits, 
                       possible_interests=['swimming', 'fishing', 'hiking'], 
                       n_traits=2, n_interests=2)
    personality.libido = 0

    return FakeGPTResponder(personality=personality)

@pytest.fixture
def responder():
    possible_traits = {
        'happy': set(['sad']),
        'sad': set(['happy']),
        'smart': set()
    }
    personality = Personality(name='test_name', years_old=25, gender='m', disposition=50.0,
                       possible_traits=possible_traits, 
                       possible_interests=['swimming', 'fishing', 'hiking'], 
                       n_traits=2, n_interests=2)
    personality.libido = 0

    return FakeGPTResponder(personality=personality)

@pytest.fixture
def high_libido_responder():
    possible_traits = {
        'happy': set(['sad']),
        'sad': set(['happy']),
        'smart': set()
    }
    personality = Personality(name='test_name', years_old=25, gender='m', disposition=50.0,
                       possible_traits=possible_traits, 
                       possible_interests=['swimming', 'fishing', 'hiking'], 
                       n_traits=2, n_interests=2)

    personality.libido = 10

    return FakeGPTResponder(personality=personality)

@pytest.fixture
def high_disposition_responder():
    possible_traits = {
        'happy': set(['sad']),
        'sad': set(['happy']),
        'smart': set()
    }
    personality = Personality(name='test_name', years_old=25, gender='m', disposition=85.0,
                       possible_traits=possible_traits, 
                       possible_interests=['swimming', 'fishing', 'hiking'], 
                       n_traits=2, n_interests=2)

    personality.libido = 0

    return FakeGPTResponder(personality=personality)

def test_build_response_from_input(responder):
    input = "hey"
    response = responder.build_response_from_input(input)
    assert response == "hey!"

def test_does_not_include_libido_response(responder):
    input = "hey"
    response = responder.build_response_from_input(input)
    assert not response.find("horny!") > 0

def test_includes_libido_response(high_libido_responder):
    input = "hey"
    response = high_libido_responder.build_response_from_input(input)
    assert response == "horny!"

def test_build_response_from_low_disposition(low_disposition_responder):
    input = "hey"
    response = low_disposition_responder.build_response_from_input(input)
    assert response == "im done"

def test_build_response_from_high_disposition(high_disposition_responder):
    input = "hey"
    response = high_disposition_responder.build_response_from_input(input)
    assert response == "lets hang out."

