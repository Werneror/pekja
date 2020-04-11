import os
import inspect
import pkgutil
import importlib

from .parser import Parser


def get_parse_class_list():
    pkg_path = os.path.dirname(__file__)
    parse_class_list = list()
    for _, file, _ in pkgutil.iter_modules([pkg_path]):
        module = importlib.import_module('parse.src.' + file)
        parse_class_list += [m[0] for m in inspect.getmembers(module, inspect.isclass)
                             if issubclass(m[1], Parser) and m[0] != 'Parser']
    return parse_class_list


def get_parse_class(class_name):
    pkg_path = os.path.dirname(__file__)
    for _, file, _ in pkgutil.iter_modules([pkg_path]):
        module = importlib.import_module('parse.src.' + file)
        for m in inspect.getmembers(module, inspect.isclass):
            if issubclass(m[1], Parser) and m[0] == class_name:
                return m[1]
