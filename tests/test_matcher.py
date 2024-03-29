import pytest
from matcher.matcher import Matcher, UnmatchedException
from personality.personality import Personality
from responder.responder import EchoResponder

class FakeResponder(EchoResponder):

    def get_disposition(self, comment):
        if comment.strip().find("well hey there") >= 0:
            return 30.0
        elif comment.strip().find("I'm done") >= 0:
            return 1.0
        else:
            raise Exception()

@pytest.fixture
def possible_traits():
    return  {
        'happy': set(['sad']),
        'sad': set(['happy']),
        'smart': set()
    }


@pytest.fixture
def possible_interests():
    return ['swimming', 'fishing', 'hiking']


@pytest.fixture
def personality(possible_interests, possible_traits):
    return Personality(name='test_name', years_old=25, gender='m', disposition=50.0,
                       possible_traits=possible_traits, 
                       possible_interests=possible_interests, 
                       n_traits=2, n_interests=2)


@pytest.fixture
def low_personality(possible_interests, possible_traits):
    return Personality(name='test_name', years_old=25, gender='m', disposition=10.0,
                       possible_traits=possible_traits, 
                       possible_interests=possible_interests, 
                       n_traits=2, n_interests=2)

@pytest.fixture
def analyzer():
    return FakeAnalyzer()


def test_personality_response(personality):
    matcher = Matcher()
    matcher.responder = FakeResponder()
    matcher.personality = personality
    response = matcher.personality_response("well hey there").replace("\t", '').strip()
    assert response == "well hey there"

def test_unmatch(low_personality):
    matcher = Matcher()
    matcher.responder = FakeResponder()
    matcher.personality = low_personality
    try:
        matcher.personality_response("I'm done")
        assert False
    except UnmatchedException:
        pass

