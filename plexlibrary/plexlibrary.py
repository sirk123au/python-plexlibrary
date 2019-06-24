#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Automated Plex library utility

This utility creates or maintains a Plex library
based on a configuration recipe.

Disclaimer:
    Use at your own risk! I am not responsible
    for damages to your Plex server or libraries.

Credit:
    Originally based on
    https://gist.github.com/JonnyWong16/f5b9af386ea58e19bf18c09f2681df23
    by /u/SwiftPanda16
"""
import os
import argparse
import sys

import recipes
from recipe import Recipe


def list_recipes(directory=None):
    print("Available recipes:")
    for name in recipes.get_recipes(directory):
        print("    {}".format(name))


def main():
    sys.stdout = Logger()
    parser = argparse.ArgumentParser(
        prog='plexlibrary',
        description=("This utility creates or maintains a Plex library "
                     "based on a configuration recipe."),
        usage='%(prog)s [options] [<recipe>]',
    )
    parser.add_argument('recipe', nargs='?',
                        help='Create a library using this recipe')
    parser.add_argument(
        '-l', '--list-recipes', action='store_true',
        help='list available recipes')
    parser.add_argument(
        '-s', '--sort-only', action='store_true', help='only sort the library')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    if args.list_recipes:
        list_recipes()
        sys.exit(0)

    if args.recipe not in recipes.get_recipes():
        print("Error: No such recipe")
        list_recipes()
        sys.exit(1)

    r = Recipe(args.recipe)
    r.run(args.sort_only)
    if os.path.exists('data.json'): os.remove('data.json')
    print("Done!")


if __name__ == "__main__":
    main()

class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("plexlibrary.log", "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)  

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass    