# -*- coding: utf-8 -*-

import json
from colorama import init
init()
from colorama import Fore, Style
from tabulate import tabulate


class Printer(object):
    """ Print output for VSD-CLI

    """
    @classmethod
    def colorprint(cls, message, color=''):
        """ Print a messsage in a specific color

            Args:
                color: the color of the message
                message: the message to print

        """
        print(color + message + Style.RESET_ALL)

    @classmethod
    def raise_error(cls, message):
        """ Print an error message

            Args:
                message: the message to print

        """
        raise Exception('\033[91m[Error] %s\033[0m' % message)

    @classmethod
    def success(cls, message):
        """ Print a succcess message

            Args:
                message: the message to print

        """
        cls.colorprint('[Success] %s' % message, Fore.GREEN)

    @classmethod
    def warn(cls, message):
        """ Print a warning message

            Args:
                message: the message to print
        """

        cls.colorprint('[WARNING] %s' % message, Fore.YELLOW)

    @classmethod
    def info(cls, message):
        """ Print a log message

            Args:
                message: the message to print
        """

        cls.colorprint('[INFO] %s' % message, Fore.CYAN)

    @classmethod
    def output(cls, data, json=False):
        """ Print either json or tabulate data

            Args:
                data: the data to display

        """
        if json:
            cls.json(data)
        else:
            cls.tabulate(data)

    ### PRINTING METHODS

    @classmethod
    def json(cls, data):
        """ Print a json version of data

            Args:
                data: something to display

        """
        if isinstance(data, str):
            print(data)

        elif isinstance(data, dict):
            print(json.dumps(data, indent=4))

        elif isinstance(data, list):
            results = []
            for obj in data:
                results.append(obj.to_dict())
            print(json.dumps(results, indent=4))

        else:
            print(json.dumps(data.to_dict(), indent=4))

    @classmethod
    def tabulate(cls, data):
        """ Prints a tabulate version of data

            Args:
                data: something to disply

        """
        if isinstance(data, str):
            print tabulate([[data]])

        elif isinstance(data, dict):
            print tabulate([data], headers={})

        elif isinstance(data, list):
            results = []

            for obj in data:
                results.append(obj.to_dict())

            print tabulate(results, headers={})

        else:
            print tabulate([data.to_dict()], headers={})
