# -*- coding: utf-8 -*-

import os
import importlib
import logging

from vsdk import NUVSDSession, set_log_level
from printer import Printer
from utils import Utils

# TEMPORARY DATABASE
OBJECTS_MAPPING = {}


class VSDCLICommand(object):
    """ VSD CLI commands

    """
    @classmethod
    def execute(cls, args):
        """ Execute CLI command """

        func = getattr(cls, args.command)
        setattr(args, "name", getattr(args, args.command))
        del(args.command)
        func(args)

    ### Commands

    @classmethod
    def list(cls, args):
        """ List all objects

        """
        name = Utils.get_singular_name(args.name)
        instance = cls._get_vsdk_instance(name)
        session = cls._get_user_session(args)
        parent = cls._get_vsdk_parent(args.parent_infos, session)

        try:
            fetcher = getattr(parent, instance.get_fetcher_name())
        except:
            Printer.raiseError('%s failed fetching its %s' % (parent.get_remote_name(), instance.get_resource_name()))

        (fetcher, parent, objects, connection) = fetcher.fetch_objects()

        if objects is None:
            Printer.raiseError('Could not retrieve. Activate verbose mode for more information')

        Printer.success('%s %s have been retrieved' % (len(objects), instance.get_resource_name()))
        Printer.tabulate(objects)

    @classmethod
    def show(cls, args):
        """ Show object details

            Args:
                uuid: Identifier of the object to show
        """
        name = Utils.get_singular_name(args.name)
        instance = cls._get_vsdk_instance(name)
        instance.id = args.id
        cls._get_user_session(args)

        try:
            (instance, connection) = instance.fetch()
        except Exception, e:
            Printer.raiseError('Could not find %s with id `%s`. Activate verbose mode for more information:\n%s' % (name, args.id, e))

        Printer.success('%s with id %s has been retrieved' % (name, args.id))
        Printer.tabulate(instance)

    @classmethod
    def create(cls, args):
        """ Create an object

        """
        name = Utils.get_singular_name(args.name)
        instance = cls._get_vsdk_instance(name)
        session = cls._get_user_session(args)
        parent = cls._get_vsdk_parent(args.parent_infos, session)
        attributes = cls._get_attributes(args.params)

        cls._fill_instance_with_attributes(instance, attributes)

        try:
            (instance, connection) = parent.add_child_object(instance)
        except Exception, e:
            Printer.raiseError('Cannot create %s:\n%s' % (name, e))

        Printer.success('%s has been created with ID=%s' % (name, instance.id))
        Printer.tabulate(instance)

    @classmethod
    def update(cls, args):
        """ Update an existing object


        """
        name = Utils.get_singular_name(args.name)
        instance = cls._get_vsdk_instance(name)
        instance.id = args.id
        attributes = cls._get_attributes(args.params)

        cls._get_user_session(args)

        try:
            (instance, connection) = instance.fetch()
        except Exception, e:
            Printer.raiseError('Could not find %s with id `%s`. Activate verbose mode for more information:\n%s' % (name, args.id, e))

        cls._fill_instance_with_attributes(instance, attributes)

        try:
            (instance, connection) = instance.save()
        except Exception, e:
            Printer.raiseError('Cannot update %s:\n%s' % (name, e))

        Printer.success('%s with ID=%s has been updated' % (name, instance.id))
        Printer.tabulate(instance)

    @classmethod
    def delete(cls, args):
        """ Delete an existing object


        """
        name = Utils.get_singular_name(args.name)
        instance = cls._get_vsdk_instance(name)
        instance.id = args.id

        cls._get_user_session(args)

        try:
            (instance, connection) = instance.delete()
        except Exception, e:
            Printer.raiseError('Could not delete %s with id `%s`. Activate verbose mode for more information:\n%s' % (name, args.id, e))

        Printer.success('%s with ID=%s has been deleted' % (name, instance.id))

    ### General methods

    @classmethod
    def _get_user_session(cls, args):
        """ Get api key

            Args:
                username: username to get an api key
                password: password to get an api key
                api: URL of the API endpoint
                enterprise: Name of the enterprise to connect

            Returns:
                Returns an API Key if everything works fine
        """

        # # TODO-CS: Remove. For Development purpose only
        # os.environ["VSDCLI_USERNAME"] = u"csproot"
        # os.environ["VSDCLI_PASSWORD"] = u"csproot"
        # os.environ["VSDCLI_API_URL"] = u"https://135.227.220.152:8443"
        # os.environ["VSDCLI_ENTERPRISE"] = u"csp"
        # # End

        username = os.environ.get('VSDCLI_USERNAME', args.username)
        password = os.environ.get('VSDCLI_PASSWORD', args.password)
        api_url = os.environ.get('VSDCLI_API_URL', args.api)
        enterprise = os.environ.get('VSDCLI_ENTERPRISE', args.enterprise)

        if username is None:
            Printer.raiseError('Please provide a username using option --username or VSDCLI_USERNAME environment variable')

        if password is None:
            Printer.raiseError('Please provide a password using option --password or VSDCLI_PASSWORD environment variable')

        if api_url is None:
            Printer.raiseError('Please provide an API URL using option --api or VSDCLI_API_URL environment variable')

        if enterprise is None:
            Printer.raiseError('Please provide an enterprise using option --enterprise or VSDCLI_ENTERPRISE environment variable')

        session = NUVSDSession(username=username, password=password, enterprise=enterprise, api_url=api_url + '/nuage/api/v3_1')
        session.start()

        user = session.user

        if user.api_key is None:
            Printer.raiseError('Could not get a valid API key. Activate verbose mode for more information')

        return session

    @classmethod
    def _define_verbosity(cls, args):
        """ Defines verbosity

            Args:
                verbose: Boolean to activate or deactivate DEBUG mode
        """

        if args.verbose:
            set_log_level(logging.DEBUG)
        else:
            set_log_level(logging.ERROR)

    @classmethod
    def _load_vsdk_objects_mapping(cls):
        """ Load vsdk objects mapping

        """
        vsdk = importlib.import_module('vsdk')
        object_names = [name for name in dir(vsdk) if name.startswith('NU') and not name.endswith('Fetcher')]

        for object_name in object_names:
            obj = getattr(vsdk, object_name)
            OBJECTS_MAPPING[obj.get_remote_name()] = object_name

    @classmethod
    def _load_vsdk_objects(cls, name):
        """ Get VSDK object instance according to a given name

            Args:
                name: the name of the object

            Returns:
                A VSDK object or raise an exception
        """

        if len(OBJECTS_MAPPING) == 0:
            cls._load_vsdk_objects_mapping()

        if name in OBJECTS_MAPPING:
            classname = OBJECTS_MAPPING[name]

            vsdk = importlib.import_module('vsdk')
            klass = None
            try:
                vsdk = importlib.import_module('vsdk')
                klass = getattr(vsdk, classname)
            except:
                Printer.raiseError('Unknown class %s' % classname)

            return klass()

        Printer.raiseError('Unknown object named %s' % name)

    @classmethod
    def _get_vsdk_parent(cls, parent_infos, session):
        """ Get VSDK parent object if possible
            Otherwise it will take the user in session

            Args:
                parent_infos: a list composed of (parent_name, uuid)

            Returns:
                A parent if possible otherwise the user in session

        """
        if parent_infos and len(parent_infos) == 2:
            name = parent_infos[0]
            uuid = parent_infos[1]

            parent = cls._get_vsdk_instance(name)
            parent.id = uuid

            try:
                (parent, connection) = parent.fetch()
            except Exception, ex:
                Printer.raiseError('Failed fetching parent %s with uuid %s\n%s' % (name, uuid, ex))

            return parent

        return session.user

    @classmethod
    def _get_attributes(cls, params):
        """ Transforms a list of Key=Value
            to a dictionary of attributes

            Args:
                params: list of Key=Value

            Returns:
                A dict

        """
        attributes = dict()

        for param in params:
            infos = param.split('=')

            if len(infos) != 2:
                Printer.raiseError('Parameter %s is not in key=value format' % param)

            attribute_name = Utils.get_python_name(infos[0])
            attributes[attribute_name] = infos[1]

        return attributes

    @classmethod
    def _fill_instance_with_attributes(cls, instance, attributes):
        """ Fill the given instance with attributes

            Args:
                instance: the instance to fill
                attributes: the dictionary of attributes

            Returns:
                The instance filled or throw an exception

        """

        for attribute_name, attribute_value in attributes.iteritems():

            attribute = instance.get_attribute_infos(attribute_name)
            if attribute is None:
                Printer.raiseError('Attribute %s could not be found in %s' % (attribute_name, instance.get_remote_name()))

            try:
                value = attribute.attribute_type(attribute_value)
                setattr(instance, attribute_name, value)
            except Exception, e:
                Printer.raiseError('Attribute %s could not be set with value %s\n%s' % (attribute_name, attribute_value, e))

        # TODO-CS: Remove validation when we will have all attribute information from Swagger...
        # if not instance.validate():
        #     Printer.raiseError('Cannot validate %s for creation due to following errors\n%s' % (instance.get_remote_name(), instance.errors))
