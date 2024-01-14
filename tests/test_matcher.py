import pytest
from matcher.matcher import Matcher, UnmatchedException
from personality.personality import GPTBackstoryPersonality
from responder.responder import EchoResponder

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
    return GPTBackstoryPersonality(years_old=25, gender='m', disposition=50.0)


@pytest.fixture
def low_personality(possible_interests, possible_traits):
    return GPTBackstoryPersonality(years_old=25, gender='m', disposition=10.0)


def test_personality_response(personality):
    matcher = Matcher()
    matcher.responder = EchoResponder()
    matcher.personality = personality
    response = matcher.personality_response("well hey there").replace("\t", '').strip()
    assert response == "well hey there"

def test_unmatch(low_personality):
    matcher = Matcher()
    matcher.responder = EchoResponder()
    matcher.personality = low_personality
    try:
        matcher.personality_response("hey")
        assert False
    except UnmatchedException:
        pass