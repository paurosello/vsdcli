# -*- coding: utf-8 -*-

import importlib
import re
from printer import Printer


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


class VSDKUtils(object):
    """ Utils to access VSDK objects

    """
    # TEMPORARY DATABASE
    OBJECTS_MAPPING = {}

    @classmethod
    def _load_vsdk_objects_mapping(cls):
        """ Load vsdk objects mapping

        """
        vsdk = importlib.import_module('vsdk')
        object_names = [name for name in dir(vsdk) if name != 'NUVSDSession' and name.startswith('NU') and not name.endswith('Fetcher')]

        for object_name in object_names:
            obj = getattr(vsdk, object_name)
            VSDKUtils.OBJECTS_MAPPING[obj.rest_name] = object_name

    @classmethod
    def get_vsdk_instance(cls, name):
        """ Get VSDK object instance according to a given name

            Args:
                name: the name of the object

            Returns:
                A VSDK object or raise an exception
        """
        if len(VSDKUtils.OBJECTS_MAPPING) == 0:
            cls._load_vsdk_objects_mapping()

        if name in VSDKUtils.OBJECTS_MAPPING:
            classname = VSDKUtils.OBJECTS_MAPPING[name]

            vsdk = importlib.import_module('vsdk')
            klass = None
            try:
                vsdk = importlib.import_module('vsdk')
                klass = getattr(vsdk, classname)
            except:
                Printer.raise_error('Unknown class %s' % classname)

            return klass()

        Printer.raise_error('Unknown object named %s' % name)

    @classmethod
    def get_vsdk_parent(cls, parent_infos, user):
        """ Get VSDK parent object if possible
            Otherwise it will take the user

            Args:
                parent_infos: a list composed of (parent_name, uuid)

            Returns:
                A parent if possible otherwise the user in session

        """
        if parent_infos and len(parent_infos) == 2:
            name = parent_infos[0]
            uuid = parent_infos[1]

            parent = VSDKUtils.get_vsdk_instance(name)
            parent.id = uuid

            try:
                (parent, connection) = parent.fetch()
            except Exception, ex:
                Printer.raise_error('Failed fetching parent %s with uuid %s\n%s' % (name, uuid, ex))

            return parent

        return user
