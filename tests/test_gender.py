from gender.gender import Gender, UnsupportedGenderCommandException

def test_m_uses_male_names():
    genderObj = Gender()
    name, gender = genderObj.get_name("/match m 20")
    assert gender == 'm'
    assert name in genderObj.male_names

def test_w_uses_female_names():
    genderObj = Gender()
    name, gender = genderObj.get_name("/match f 20")
    assert gender == 'f'
    assert name in genderObj.female_names

def test_n_uses_nonbinary_names():
    genderObj = Gender()
    name, gender = genderObj.get_name("/match n")
    assert gender == 'n'
    assert name in genderObj.nonbinary_names

def test_malformed_throws_error():
    try:
        gender = Gender()
        gender.get_name("/match")
        assert False
    except UnsupportedGenderCommandException as e:
        pass