from personality.personality import Personality, UnableToAssignTraitsException
import pytest


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

def test_assign_random_traits_avoids_conflicts(possible_traits, personality):
    assigned_random_traits = personality.assign_random_traits(possible_traits, n_select=2)
    if 'sad' in assigned_random_traits:
        assert 'happy' not in assigned_random_traits
    elif 'happy' in assigned_random_traits:
        assert 'sad' not in assigned_random_traits
    assert 'smart' in assigned_random_traits


def test_assign_random_traits_gives_up_after_too_many_incompatible_attempts(possible_traits, possible_interests):
    try:
        Personality(name='test_name', years_old=25, gender='f', disposition=50.0,
                    possible_traits=possible_traits, possible_interests=possible_interests, 
                    n_traits=3, n_interests=2)
        pytest.fail("select should have failed")
    except UnableToAssignTraitsException:
        pass

def test_assign_random_interests(possible_interests, personality):
    interests = sorted(personality.assign_random_interests(possible_interests, n_select=3))
    expected = ['fishing', 'hiking', 'swimming']
    assert interests == expected


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