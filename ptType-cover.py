"""
This parses .py files to highlight functions without return types or python typing
arguments

Functions:
    * run
    * search_for_type_hints
    * search_func_def
"""

import ast
import re
import sys
from functools import reduce
import configparser
from configparser import ExtendedInterpolation
import logging
import os
from os import path

LOGGER = logging.getLogger(__name__)

def run(config:dict) -> None:
    """
    Main entrypoint function for running the script.

    Args:
        config (dict) : configuration settings for this run.
    
    Returns:
        None
    """
    LOGGER.info("Starting to check Python Type coverage")

    if config['python_type_coverage']['cover_file_or_directory'] == 'file':
        dir_path = config['python_type_coverage']['file_to_cover']
        if dir_path.endswith(".py"):
            opened_file = open(dir_path, "r")

            lines = opened_file.readlines()
            search_for_type_hints(lines, dir_path)

            opened_file.close()
    
    elif config['python_type_coverage']['cover_file_or_directory'] == 'dir':
        dir_path = config['python_type_coverage']['directory_to_cover']

        os.chdir(dir_path)

        if path.exists(dir_path):
            for root, _, files in os.walk(dir_path):
                for file_to_open in files:
                    if file_to_open.endswith(".py"):
                        file_to_open_path = os.path.join(root, file_to_open)

                        opened_file = open(file_to_open_path, "r")

                        lines = opened_file.readlines()
                        search_for_type_hints(lines, file_to_open)

                        opened_file.close()


def search_for_type_hints(lines: list, file_path:str) -> None:
    """
        Args:
            lines (list) : lines to search
            file_path (str) : file & path searched
        
        Returns:
            None
    """
    for idx, line in enumerate(lines):
        if re.search("def.*\(.*\).*:", line):

            search_func_def(line.rstrip(), file_path, idx)

            continue

        if re.search("def.*\(.", line):
            lst = []
            id = idx

            while True:
                    if re.search("(\"{3})|(\'{3})", lines[id]):
                        break
                    
                    lst.append(lines[id])

                    id += 1
                    if id == len(lines):
                        break

            f_def = reduce(lambda x, y: x.rstrip() + " " + y.lstrip(), lst)

            search_func_def(f_def.rstrip(), file_path, idx)

def search_func_def(line:str, file_path: str, idx:int) -> None:
    """
        Args:
            line (str) : line to search
            file_path (str) : file & path searched
            idx (int) : index line of file searched
        
        Returns:
            None
    """
    if "->" not in line:
        print(f"No return type defined on file {file_path} line {idx+1}")
    
    types = line.split(':')

    if len(types) == 2:
        test = False

        for s in types:
            if 'self' in s:
                test = True
        
        if test == False:
            print(f"Not python typing found on file {file_path} line {idx+1}")

if __name__ == "__main__":

    #Path to the config file for this run
    CONFIG_PATH = sys.argv[1]

    CONFIG = configparser.ConfigParser(
        interpolation=ExtendedInterpolation(),
        converters={"py": lambda x: ast.literal_eval(x)})

    CONFIG.read(CONFIG_PATH)

    run(CONFIG)