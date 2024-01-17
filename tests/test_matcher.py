import pytest
from matcher.matcher import Matcher, UnmatchedException
from personality.personality import Personality
from responder.responder import EchoResponder


class FakeAnalyzer():

    def polarity_scores(self, content):
        if content.strip() == "I hate you":
            return {'neg': 0.85, 'neu': 0.13, 'pos': 0.02}
        elif content.strip() == "I love you":
            return {'neg': 0.02, 'neu': 0.13, 'pos': 0.85}
        elif content.strip() == "I'm done":
            return {'neg': 0.99, 'neu': 0.01, 'pos': 0.00}
        else:
            return {'neg': 0.15, 'neu': 0.83, 'pos': 0.02}
    

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


def test_personality_response(personality, analyzer):
    matcher = Matcher()
    matcher.responder = EchoResponder()
    matcher.sentiment_analyzer = analyzer
    matcher.personality = personality
    response = matcher.personality_response("well hey there").replace("\t", '').strip()
    assert response == "well hey there"

def test_unmatch(low_personality, analyzer):
    matcher = Matcher()
    matcher.responder = EchoResponder()
    matcher.sentiment_analyzer = analyzer
    matcher.personality = low_personality
    try:
        matcher.personality_response("I'm done")
        assert False
    except UnmatchedException:
        pass


def test_get_neg_disposition(analyzer):
    matcher = Matcher()
    matcher.sentiment_analyzer = analyzer
    assert matcher.get_disposition("I hate you") == 15.0

def test_get_pos_disposition(analyzer):
    matcher = Matcher()
    matcher.sentiment_analyzer = analyzer
    assert matcher.get_disposition("I love you") == 85.0

def test_get_neu_disposition(analyzer):
    matcher = Matcher()
    matcher.sentiment_analyzer = analyzer
    assert matcher.get_disposition("Neutral comment") == 83.0

