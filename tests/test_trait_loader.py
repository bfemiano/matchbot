import pytest
from personality.loaders import TraitLoader

class MockLemma(object):

    def __init__(self, trait_name, *args, **kwargs):
        self.trait_name = trait_name

    def name(self):
        return self.trait_name
    
    def antonyms(self):
        if self.trait_name == "happy":
            return [MockLemma("angry")]
        elif self.trait_name == "funny":
            return [MockLemma("boring")]
        elif self.trait_name == "angry":
            return [MockLemma("happy")]
        elif self.trait_name == "boring":
            return [MockLemma("funny")]
        else:
            return []
        
class MockWordnet:

    def __init__(self, trait):
        self.trait = trait

    def lemmas(self):
        if self.trait == "angry":
            return [MockLemma(trait) for trait in ["angry", "mad", "furious"]]
        elif self.trait == "furious":
            return [MockLemma(trait) for trait in ["angry", "mad", "furious"]]
        elif self.trait == "mad":
            return [MockLemma(trait) for trait in ["angry", "mad", "furious"]]
        elif self.trait == "happy" or self.trait == "funny" or self.trait == "boring":
            return [MockLemma(self.trait)]
        raise Exception("No wordnet found")


def mock_wordnet_syns_func(trait):
    return [MockWordnet(trait)]

@pytest.fixture
def loader():
    return TraitLoader()

def test_dedup_synonym_traits(loader):
    loader.raw_traits = set(["angry", "mad", "furious"])
    deduped = loader.dedup_synonyms(mock_wordnet_syns_func)
    assert len(deduped) == 1
    assert "mad" in deduped or "angry" in deduped or "furious" in deduped

def test_map_traits_to_incompatible_traits(loader):
    deduped_traits = set(["angry", "funny", "happy", "boring"])
    trait_to_incompatible_traits = loader.map_traits_to_incompatibile_traits(deduped_traits, mock_wordnet_syns_func)
    expected = {
        "angry": set(["happy"]),
        "funny": set(["boring"]),
        "happy": set(["angry"]),
        "boring": set(["funny"])
    }
    assert trait_to_incompatible_traits == expected