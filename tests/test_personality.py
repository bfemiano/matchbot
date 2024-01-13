from personality.personality import GPTBackstoryPersonality
import pytest


@pytest.fixture
def personality():
    personality = GPTBackstoryPersonality(years_old=25, gender='m', disposition=50.0)
    return personality


def test_disposition_after_2_measurements(personality):
    disposition2 = 60.0
    personality.update_disposition(disposition2)
    actual = round(personality.disposition, 2)
    assert actual == 56.67

def test_disposition_after_3_measurements(personality):
    disposition2 = 60.0
    disposition3 = 70.0
    personality.update_disposition(disposition2)
    personality.update_disposition(disposition3)
    actual = round(personality.disposition, 2)
    assert actual ==  63.33