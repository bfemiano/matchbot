import pytest
from responder.responder import GPTResponder

@pytest.fixture
def responder():
    return GPTResponder(personality=None)

def test_get_disposition_directly_placed(responder):
    content = """
    Hey there! 🙋‍♀️ Not much, just chilling and browsing this app. How about you? Any exciting plans for the day? 
    🌟 By the way, I'm really into makeup and volunteering. 
    What about you? 😊 Let's chat and see if we have similar interests! 💄💖🌟
    Disposition: 60.0
    """
    disposition = responder.get_disposition(content)
    assert disposition == 60.0


def test_get_disposition_naturally_placed(responder):
    content = """
    Hey there! 🙋‍♀️ Not much, just chilling and browsing this app. How about you? Any exciting plans for the day? 
    🌟 By the way, I'm really into makeup and volunteering. 
    What about you? 😊 Let's chat and see if we have similar interests! 💄💖🌟
    On a scale of 1 to 100 I rate this conversation at 35.0
    """
    disposition = responder.get_disposition(content)
    assert disposition == 35.0


def test_not_disposition_found(responder):
    content = """
    Hey there! 🙋‍♀️ Not much, just chilling and browsing this app. How about you? Any exciting plans for the day? 
    🌟 By the way, I'm really into makeup and volunteering. 
    What about you? 😊 Let's chat and see if we have similar interests! 💄💖🌟
    """
    disposition = responder.get_disposition(content)
    assert disposition == None


def test_strip_disposition(responder):
    content = """
    Hey there! 🙋‍♀️ Not much, just chilling and browsing this app. How about you? Any exciting plans for the day? 
    🌟 By the way, I'm really into makeup and volunteering. 
    What about you? 😊 Let's chat and see if we have similar interests! 💄💖🌟
    Disposition: 60.0
    """

    expected = """
    Hey there! 🙋‍♀️ Not much, just chilling and browsing this app. How about you? Any exciting plans for the day? 
    🌟 By the way, I'm really into makeup and volunteering. 
    What about you? 😊 Let's chat and see if we have similar interests! 💄💖🌟
    """

    updated = responder.strip_disposition(content)
    assert expected == updated