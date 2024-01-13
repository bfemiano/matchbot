from gender.gender import Gender, UnsupportedGenderCommandException

def test_m_uses_male_names():
    genderObj = Gender()
    gender = genderObj.get("/match m 20")
    assert gender == 'm'

def test_w_uses_female_names():
    genderObj = Gender()
    gender = genderObj.get("/match f 20")
    assert gender == 'f'

def test_n_uses_nonbinary_names():
    genderObj = Gender()
    gender = genderObj.get("/match n")
    assert gender == 'n'

def test_malformed_throws_error():
    try:
        gender = Gender()
        gender.get("/match")
        assert False
    except UnsupportedGenderCommandException as e:
        pass