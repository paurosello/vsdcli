# -*- coding: utf-8 -*-

import importlib
import re
import pkg_resources

from printer import Printer


class Utils(object):
    """ Utils """

    INVARIANT_RESOURCES = ['qos', 'vrs']

    @classmethod
    def _clean_name(cls, string):
        """ String cleaning for specific cases

            This is very specific and is used to force
            some underscore while using get_python_name.

            Args:
                string: the string to clean

            Returns:
                Returns a clean string
        """
        rep = {
            "VPort": "Vport",
            "IPID": "IpID"
        }

        rep = dict((re.escape(k), v) for k, v in rep.iteritems())
        pattern = re.compile("|".join(rep.keys()))
        return pattern.sub(lambda m: rep[re.escape(m.group(0))], string)

    @classmethod
    def get_python_name(cls, name):
        """ Transform a given name to python name """
        first_cap_re = re.compile('(.)([A-Z](?!s([A-Z])*)[a-z]+)')
        all_cap_re = re.compile('([a-z0-9])([A-Z])')

        s1 = first_cap_re.sub(r'\1_\2', Utils._clean_name(name))
        return all_cap_re.sub(r'\1_\2', s1).lower()

    @classmethod
    def get_singular_name(cls, plural_name):
        """ Returns the singular name of the plural name """

        if plural_name in Utils.INVARIANT_RESOURCES:
            return plural_name

        if plural_name[-3:] == 'ies':
            return plural_name[:-3] + 'y'

        if plural_name[-1] == 's':
            return plural_name[:-1]

        return plural_name

    @classmethod
    def get_plural_name(cls, singular_name):
        """ Returns the plural name of the singular name """

        if singular_name in Utils.INVARIANT_RESOURCES:
            return singular_name

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
    IGNORED_RESOURCES = ['me']

    @classmethod
    def get_all_objects(cls):
        """ Returns all objects from the VSD

        """
        if len(VSDKUtils.OBJECTS_MAPPING) == 0:
            cls._load_vsdk_objects_mapping()

        resources = VSDKUtils.OBJECTS_MAPPING.keys()
        resources = [Utils.get_plural_name(name) for name in resources if name not in VSDKUtils.IGNORED_RESOURCES]

        return resources

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

    @classmethod
    def get_installed_version(cls):
        """ Get VSDK version

        """
        return pkg_resources.get_distribution("vsdk").version
