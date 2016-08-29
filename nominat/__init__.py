import itertools
import os
import random
import re

SPLIT_BOUNDARIES = re.compile(r'[A-Za-z0-9]+')
SPLIT_CASED_WORDS = re.compile(r'(^[a-z]+|[A-Z]+(?![a-z])|[A-Z][a-z]+|[0-9]+)')


class Nominator(object):
    def __init__(self, replacements, no_replace=None):
        """Initializes Nominator based on a replacements list.

        Also accepts an iterable of words not to replace as `no_replace`.
        """
        self.cache = {}
        self.replacements = list(read_words(replacements))
        self._no_replace = set(read_words(no_replace or []))

    def __call__(self, word):
        """Convenience call function for `replace_combined`."""
        return self.replace_combined(word)

    def replace_combined(self, word):
        """Returns a string with each sub-word replaced.

        Splits a variable name on underscores and case differences and then
        replaces each individual word. The case style for each replaced word
        is kept the same as the original.
        """
        return SPLIT_BOUNDARIES.sub(self._process_cased_words, word)

    def replace_single(self, word):
        """Returns the replaced word in the same case style.

        Expects words to be of a detectable case: `lower`, `upper` or `title`.
        If a mixed case-style word is provided, a ValueError is raised instead.
        """
        if word.islower() or word.isdigit():
            return self._replace(word)
        elif word.isupper():
            return self._replace(word.lower()).upper()
        elif word.istitle():
            return self._replace(word.lower()).title()
        raise ValueError('Unable to detect/reproduce case of %r.' % word)

    def _process_cased_words(self, match):
        """Replace the words within a single phrase portion."""
        cased_word = match.group(0)
        return ''.join(itertools.imap(
            self.replace_single, split_replace_by_case(cased_word)))

    def _replace(self, word):
        """Replaces the given word with a random pick from the replacements

        Once a replacement has been picked, this choice will be cached and
        re-used for all following offers for replacement.
        """
        if word in self._no_replace:
            return word
        if word in self.cache:
            return self.cache[word]
        replacement = self.cache[word] = random.choice(self.replacements)
        return replacement


def read_words(source):
    """Read words from a file, list or other iterable."""
    for line in source:
        for word in line.split():
            word = word.strip()
            if word:
                yield word.lower()


def split_replace_by_case(word):
    """Yields chunks of word that are separated by case usage."""
    for match in SPLIT_CASED_WORDS.finditer(word):
        yield match.group(0)


def nominator():
    word_file = os.path.join(os.path.dirname(__file__), 'words.txt')
    return Nominator(file(word_file), no_replace=['id'])
