# -*- coding: utf-8 -*-

import re


class Utils(object):
    """ Utils """

    @classmethod
    def get_python_name(cls, name):
        """ Transform a given name to python name """
        first_cap_re = re.compile('(.)([A-Z](?!s[A-Z])[a-z]+)')
        all_cap_re = re.compile('([a-z0-9])([A-Z])')

        def repl(matchobj):
            """ Replacement method """
            if matchobj.start() == 0:
                return matchobj.expand(r"\1\2")
            else:
                return matchobj.expand(r"\1_\2")

        s1 = first_cap_re.sub(repl, name)
        return all_cap_re.sub(r'\1_\2', s1).lower()

    @classmethod
    def get_singular_name(cls, plural_name):
        """ Returns the singular name of the plural name """

        if plural_name[-3:] == 'ies':
            return plural_name[:-3] + 'y'

        if plural_name[-1] == 's':
            return plural_name[:-1]

        return plural_name

    @classmethod
    def get_plural_name(cls, singular_name):
        """ Returns the plural name of the singular name """

        vowels = ['a', 'e', 'i', 'o', 'u', 'y']
        if singular_name[-1:] == 'y' and singular_name[-2] not in vowels:
            return singular_name[:-1] + 'ies'

        if singular_name[-1:] == 's':
            return singular_name

        return singular_name + 's'
