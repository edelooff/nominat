#!/usr/bin/python

import io

import pytest

import nominat


@pytest.fixture
def empty():
    """Plain and empty Nominat instance."""
    return nominat.Nominator([])


@pytest.fixture
def chicken():
    """Everything except 'id' transforms to 'chicken'."""
    return nominat.Nominator(['chicken'], no_replace=['id'])


@pytest.fixture
def spam():
    """Partially pre-filled cache, but otherwise spam."""
    spammer = nominat.Nominator(['spam'])
    spammer.cache.update(foo='egg', bar='bacon', baz='sausage')
    return spammer


def test_single_word(spam):
    """Test single word replacement and cache functionality."""
    assert spam('wonderful') == 'spam'
    assert 'wonderful' in spam.cache
    assert spam.cache['wonderful'] == 'spam'


def test_missing_word_nopicks(empty):
    """Assure that without replacement list, cache hits produce errors."""
    with pytest.raises(IndexError):
        empty('anykey')


def test_case_preservation(spam):
    """Test case-insensitiveness and -preservation."""
    assert spam('wonderful') == 'spam'
    assert spam('Wonderful') == 'Spam'
    assert spam('WONDERFUL') == 'SPAM'


def test_lower_with_under(spam):
    """Test multiple words with underscores."""
    assert spam('foo_bar') == 'egg_bacon'
    assert spam('foo_baz_bar') == 'egg_sausage_bacon'
    assert spam('FOO_QUUX') == 'EGG_SPAM'
    assert spam('foo_bar_QUUX') == 'egg_bacon_SPAM'
    assert spam('foo_BAR_BAZ_quux') == 'egg_BACON_SAUSAGE_spam'
    assert spam('that_bar_baz_QUUX') == 'spam_bacon_sausage_SPAM'
    # This is getting too silly..


def test_variable_length_underscores(chicken):
    """Test runs of multiple underscores in variable names."""
    assert chicken('x__x') == 'chicken__chicken'
    assert chicken('x_x__x___x') == 'chicken_chicken__chicken___chicken'


def test_case_based_separation(chicken, spam):
    """Test detection of words in camelCase/PascalCase names."""
    assert spam('fooBaz') == 'eggSausage'
    assert spam('FooBar') == 'EggBacon'
    assert spam('FOOBarBaz') == 'EGGBaconSausage'
    assert chicken('simpleHTTPRequestMethod') == 'chickenCHICKENChickenChicken'


def test_mixed_case_underscore(chicken, spam):
    """Test detection of words in mixed case/underscore names."""
    assert spam('foo__barBazQUUX') == 'egg__baconSausageSPAM'
    chicken_result = 'chicken_ChickenChicken_chicken_chickenChicken'
    assert chicken('some_PascalCase_and_camelCase') == chicken_result


def test_replace_numerals(chicken, empty):
    """Numbers are also replaced, with lowercase replacement words."""
    assert chicken('Summer69') == 'Chickenchicken'
    empty.cache.update({'version': 'plane', '3': 'fan'})
    assert empty('VERSION_3') == 'PLANE_fan'


def test_word_boundaries(chicken):
    """Everything that is not text to be replaced is preserved."""
    expected = 'Chicken (chicken) chicken:chicken'
    assert chicken('This (super) neat:thing') == expected

def test_no_replace(chicken, spam):
    """Test that provided 'safe' words are not replaced."""
    assert chicken('table_id') == 'chicken_id'
    assert chicken('tableId') == 'chickenId'
    assert chicken('tableID') == 'chickenID'
    assert chicken('IDTable') == 'IDChicken'

    # But only for instances that have this configured
    assert spam('table_id') == 'spam_spam'


def test_default_nominator_has_words_and_no_replace():
    """Test default nominator has word list and no-replace entry."""
    default = nominat.nominator()
    assert len(default.replacements) != 0
    assert default('spam') != 'spam'
    assert 'spam' in default.cache

    # 'id' should be ignored by default
    assert default('id') == 'id'
    assert 'id' not in default.cache


def test_words_from_file():
    """Test initialization of word list from a file."""
    words = io.BytesIO('one two\nthree\tfour')
    nom = nominat.Nominator(words)
    assert nom.replacements == ['one', 'two', 'three', 'four']


def test_words_from_iterables():
    """Test initialization of word list from iterables."""
    words = 'one two', 'three\t  four'
    expected = ['one', 'two', 'three', 'four']

    # Create word list from tuple and iterator
    assert nominat.Nominator(words).replacements == expected
    assert nominat.Nominator(iter(words)).replacements == expected

    # Create word list from a set
    set_based = nominat.Nominator(set(words))
    assert sorted(set_based.replacements) == sorted(expected)
