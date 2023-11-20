from gender.gender import Gender, UnsupportedGenderCommandException

def test_m_uses_male_names():
    gender = Gender()
    name = gender.get_name("/match m 20")
    assert name in gender.male_names
    assert name not in gender.female_names
    assert name not in gender.nonbinary_names

def test_w_uses_female_names():
    gender = Gender()
    name = gender.get_name("/match w 20")
    assert name not in gender.male_names
    assert name in gender.female_names
    assert name not in gender.nonbinary_names

def test_n_uses_nonbinary_names():
    gender = Gender()
    name = gender.get_name("/match n")
    assert name in gender.nonbinary_names

def test_malformed_throws_error():
    try:
        gender = Gender()
        gender.get_name("/match")
        assert False
    except UnsupportedGenderCommandException as e:
        pass