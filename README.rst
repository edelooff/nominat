Nominat
#######

Nominat is a Python library that renames identifiers (variable names, class names etc.) that it is given. Identifiers consisting of several words, separated either by underscores (``pet_names``) or case (``errorMessage``) are separated into their constituent words, which are then replaced.

To allow the anonymized names to still make some sense in relation to each other, once a replacement for a word has been chosen, it will consistently be reused. In addition, `nominat` is case-insensitive but also case-preserving. This looks like this:

.. code-block:: python

    >>> nom = nominat.nominator()
    >>> nom('pet_names')
    'brilliant_failure'
    >>> nom('friendNames')
    'programFailure'
    >>> nom('ERROR_MESSAGE')
    'SECTOR_PRIEST'
    
