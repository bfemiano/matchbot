import pytest
from age.age import Age, UnsupportedAgeCommandException

def test_no_age_arg_succeeds():
    age = Age()
    age = age.get_age("/match m")
    assert age >= 18
    assert age <= 100

def test_single_arg_succeeds():
    age = Age()
    age = age.get_age("/match m 18")
    assert age == 18

def test_range_with_dash_no_space_succeeds():
    age = Age()
    age = age.get_age("/match w 20-25")
    assert age >= 20
    assert age <= 25

def test_range_same_value():
    age = Age()
    age = age.get_age("/match m 40-40")
    assert age == 40

def test_bad_range_separation():
    try:
        age = Age()
        age = age.get_age("/match m 30to50")
        assert False
    except UnsupportedAgeCommandException as e:
        assert e.msg == "Invalid age or age range. Supported examples: 25, 18-25."

def test_bad_lower():
    try:
        age = Age()
        age = age.get_age("/match m 30FAIL-50")
        assert False
    except UnsupportedAgeCommandException as e:
        assert e.msg == "Invalid age or age range. Supported examples: 25, 18-25."

def test_bad_upper():
    try:
        age = Age()
        age = age.get_age("/match m 30-50FAIL")
        assert False
    except UnsupportedAgeCommandException as e:
        assert e.msg == "Invalid age or age range. Supported examples: 25, 18-25."

def test_lower_too_young():
    try:
        age = Age()
        age = age.get_age("/match w 13-50")
        assert False
    except UnsupportedAgeCommandException as e:
        assert e.msg == "Age not supported because too young."

def test_upper_too_old():
    try:
        age = Age()
        age = age.get_age("/match w 20-120")
        assert False
    except UnsupportedAgeCommandException as e:
        assert e.msg == "Ages greater than 100 not supported at this time."