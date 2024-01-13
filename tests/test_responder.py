import pytest
from personality.personality import Personality
from responder.responder import GPTResponder


class FakeGPTResponder(GPTResponder):

    def __init__(self, personality, *args, **kwargs):
        super(FakeGPTResponder, self).__init__(personality, *args, **kwargs)

    def _completion(self, prompt_func, user_input):
        response = prompt_func(user_input, 1, False)
        if response.strip().endswith("you're chatting with just made to you.") > 0:
            return "hey! My disposition to you is 60.0"
        elif response.strip().find("not interested in carrying on the conversation any longer.") > 0:
            return "im done"
        elif response.strip().find("very much interested in meeting up") > 0:
            return "lets hang out. My disposition to you is 90.0"
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

    return FakeGPTResponder(personality=personality)

def test_get_int_easily_converted(responder):
    content = """
    test. 60.0
    """
    disposition, index = responder.get_disposition(content)
    assert disposition == 60

def test_get_disposition_directly_placed(responder):
    content = """
    Hey there! 🙋‍♀️ Not much, just chilling and browsing this app. How about you? Any exciting plans for the day? 
    🌟 By the way, I'm really into makeup and volunteering. 
    What about you? 😊 Let's chat and see if we have similar interests! 💄💖🌟
    Disposition: 60.0
    """
    disposition, index  = responder.get_disposition(content)
    assert disposition == 60


def test_get_disposition_naturally_placed(responder):
    content = """
    Let's chat and see if we have similar interests! 💄💖🌟
    On a scale of 1 to 100 I rate this conversation at 35.0
    """
    disposition, index = responder.get_disposition(content)
    assert disposition == 35


def test_not_disposition_found(responder):
    content = """
        What about you?
    """
    disposition, index = responder.get_disposition(content)
    assert disposition == None

def test_disposition_parsed_from_end(responder):
    content = """
    Hey there! Not much. On a scale of 1 - 100 you are at a 50.0
    """
    disposition, index = responder.get_disposition(content)
    assert disposition == 50.0
    assert index == 2

def test_disposition_handled_as_int_ok(responder):
    content = """
    Hey there! Not much. On a scale of 1 - 100 you are at a 50
    """
    disposition, index = responder.get_disposition(content)
    assert disposition == 50.0
    assert index == 2

def test_disposition_found_at_end(responder):
    content = """
    Hey there! Not much. 50.0
    """
    disposition, index = responder.get_disposition(content)
    assert disposition == 50.0
    assert index == 2

def test_disposition_found_at_end_trailing_period(responder):
    content = """
    Hey there! Not much. By the way my disposition to you is 50.0.
    """
    disposition, index = responder.get_disposition(content)
    assert disposition == 50.0
    assert index == 2


def test_strip_last_sentance_statement(responder):
    content = "Hi. Disposition: 60.0"
    expected = "Hi."

    updated = responder.response_minus_disposition(content, 1)
    assert expected == updated

def test_strip_last_sentance_question(responder):
    content = "Hey what's up? Disposition: 60.0"
    expected = "Hey what's up?"

    updated = responder.response_minus_disposition(content, 1)
    assert expected == updated

def test_build_response_from_input(responder):
    input = "hey"
    response = responder.build_response_from_input(input)
    assert response == "hey!"

def test_build_response_from_low_disposition(low_disposition_responder):
    input = "hey"
    response = low_disposition_responder.build_response_from_input(input)
    assert response == "im done"

def test_build_response_from_high_disposition(high_disposition_responder):
    input = "hey"
    response = high_disposition_responder.build_response_from_input(input)
    assert response == "lets hang out."

