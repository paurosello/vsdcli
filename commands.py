# -*- coding: utf-8 -*-

import os
import logging

from vsdk import NUVSDSession
from vsdk.utils import set_log_level
from printer import Printer
from utils import Utils, VSDKUtils


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
        instance = VSDKUtils.get_vsdk_instance(name)
        session = cls._get_user_session(args)
        parent = VSDKUtils.get_vsdk_parent(args.parent_infos, session.user)

        try:
            fetcher = getattr(parent, instance.get_fetcher_name())
        except:
            Printer.raise_error('%s failed fetching its %s' % (parent.get_remote_name(), instance.get_resource_name()))

        (fetcher, parent, objects, connection) = fetcher.fetch_objects()

        if objects is None:
            Printer.raise_error('Could not retrieve. Activate verbose mode for more information')

        Printer.success('%s %s have been retrieved' % (len(objects), instance.get_resource_name()))
        Printer.output(objects, args.json)

    @classmethod
    def show(cls, args):
        """ Show object details

            Args:
                uuid: Identifier of the object to show
        """
        name = Utils.get_singular_name(args.name)
        instance = VSDKUtils.get_vsdk_instance(name)
        instance.id = args.id
        cls._get_user_session(args)

        try:
            (instance, connection) = instance.fetch()
        except Exception, e:
            Printer.raise_error('Could not find %s with id `%s`. Activate verbose mode for more information:\n%s' % (name, args.id, e))

        Printer.success('%s with id %s has been retrieved' % (name, args.id))
        Printer.output(instance, args.json)

    @classmethod
    def create(cls, args):
        """ Create an object

        """
        name = Utils.get_singular_name(args.name)
        instance = VSDKUtils.get_vsdk_instance(name)
        session = cls._get_user_session(args)
        parent = VSDKUtils.get_vsdk_parent(args.parent_infos, session.user)
        attributes = cls._get_attributes(args.params)

        cls._fill_instance_with_attributes(instance, attributes)

        try:
            (instance, connection) = parent.add_child_object(instance)
        except Exception, e:
            Printer.raise_error('Cannot create %s:\n%s' % (name, e))

        Printer.success('%s has been created with ID=%s' % (name, instance.id))
        Printer.output(instance, args.json)

    @classmethod
    def update(cls, args):
        """ Update an existing object


        """
        name = Utils.get_singular_name(args.name)
        instance = VSDKUtils.get_vsdk_instance(name)
        instance.id = args.id
        attributes = cls._get_attributes(args.params)

        cls._get_user_session(args)

        try:
            (instance, connection) = instance.fetch()
        except Exception, e:
            Printer.raise_error('Could not find %s with id `%s`. Activate verbose mode for more information:\n%s' % (name, args.id, e))

        cls._fill_instance_with_attributes(instance, attributes)

        try:
            (instance, connection) = instance.save()
        except Exception, e:
            Printer.raise_error('Cannot update %s:\n%s' % (name, e))

        Printer.success('%s with ID=%s has been updated' % (name, instance.id))
        Printer.output(instance, args.json)

    @classmethod
    def delete(cls, args):
        """ Delete an existing object


        """
        name = Utils.get_singular_name(args.name)
        instance = VSDKUtils.get_vsdk_instance(name)
        instance.id = args.id

        cls._get_user_session(args)

        try:
            (instance, connection) = instance.delete()
        except Exception, e:
            Printer.raise_error('Could not delete %s with id `%s`. Activate verbose mode for more information:\n%s' % (name, args.id, e))

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

        # TODO-CS: Remove. For Development purpose only
        os.environ["VSDCLI_USERNAME"] = u"csproot"
        os.environ["VSDCLI_PASSWORD"] = u"csproot"
        os.environ["VSDCLI_API_URL"] = u"https://135.227.220.152:8443"
        os.environ["VSDCLI_ENTERPRISE"] = u"csp"
        # End

        username = os.environ.get('VSDCLI_USERNAME', args.username)
        password = os.environ.get('VSDCLI_PASSWORD', args.password)
        api_url = os.environ.get('VSDCLI_API_URL', args.api)
        enterprise = os.environ.get('VSDCLI_ENTERPRISE', args.enterprise)

        if username is None:
            Printer.raise_error('Please provide a username using option --username or VSDCLI_USERNAME environment variable')

        if password is None:
            Printer.raise_error('Please provide a password using option --password or VSDCLI_PASSWORD environment variable')

        if api_url is None:
            Printer.raise_error('Please provide an API URL using option --api or VSDCLI_API_URL environment variable')

        if enterprise is None:
            Printer.raise_error('Please provide an enterprise using option --enterprise or VSDCLI_ENTERPRISE environment variable')

        session = NUVSDSession(username=username, password=password, enterprise=enterprise, api_url=api_url + '/nuage/api/v3_1')
        session.start()

        user = session.user

        if user.api_key is None:
            Printer.raise_error('Could not get a valid API key. Activate verbose mode for more information')

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
            infos = param.split('=', 1)

            if len(infos) != 2:
                Printer.raise_error('Parameter %s is not in key=value format' % param)

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
                Printer.raise_error('Attribute %s could not be found in %s' % (attribute_name, instance.get_remote_name()))

            try:
                value = attribute.attribute_type(attribute_value)
                setattr(instance, attribute_name, value)
            except Exception, e:
                Printer.raise_error('Attribute %s could not be set with value %s\n%s' % (attribute_name, attribute_value, e))

        # TODO-CS: Remove validation when we will have all attribute information from Swagger...
        # if not instance.validate():
        #     Printer.raise_error('Cannot validate %s for creation due to following errors\n%s' % (instance.get_remote_name(), instance.errors))
