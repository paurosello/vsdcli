# -*- coding: utf-8 -*-

import os
import logging

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
    def error(cls, message):
        """ Print an error message

            Args:
                message: the message to print
        """
        cls.colorprint('[Error] %s' % message, Fore.RED)


    @classmethod
    def success(cls, message):
        """ Print a succcess message

            Args:
                message: the message to print
        """

        cls.colorprint('[Success] %s' % message, Fore.GREEN)

    @classmethod
    def tabulate(cls, data):
        """ Prints a tabulate version of data

            Args:
                data: a list of objects to print
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