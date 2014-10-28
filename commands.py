# -*- coding: utf-8 -*-

import os
import logging

from models import *
from models.utils import set_log_level
from printer import Printer


class VSDKCommands(object):
    """ VSDK CLI available commands
    """

    @classmethod
    def execute(cls, args):
        """docstring for execute"""

        func = getattr(cls, args.command)
        del(args.command)
        func(args)

    @classmethod
    def list_enterprises(cls, args):
        """ List all enterprises of the user
        """

        session = cls._get_user_session(args)

        if session is not None:
            user = session.user
            (fetcher, user, enterprises, connection) = user.fetch_enterprises()

            if enterprises is None:
                Printer.error('Could not retrieve enterprises. Activate verbose mode for more information')
            else:
                Printer.success('%s enterprises found' % len(enterprises))
                Printer.tabulate(enterprises)

    @classmethod
    def show_enterprise(cls, args):
        """ Show enterprise information

            Args:
                id: Identifier of the enterprise
        """

        session = cls._get_user_session(args)

        if session is not None:
            enterprise = NUEnterprise()
            enterprise.id = args.id

            (enterprise, connection) = enterprise.fetch()

            if connection.response.status_code >= 300:
                Printer.error('Could not find enterprise with id `%s`. Activate verbose mode for more information' % args.id)
            else:
                Printer.success('Information about enterprise `%s`' % args.id)
                Printer.tabulate(enterprise)

    # General methods

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

        username = os.environ.get('VSDK_USERNAME', args.username)
        password = os.environ.get('VSDK_PASSWORD', args.password)
        api_url = os.environ.get('VSDK_API_URL', args.api)
        enterprise = os.environ.get('VSDK_ENTERPRISE', args.enterprise)

        session = NUVSDSession(username=username, password=password, enterprise=enterprise, api_url=api_url)
        session.start()

        user = session.user

        if user.api_key is None:
            Printer.error('Could not get a valid API key. Activate verbose mode for more information')
            return None

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