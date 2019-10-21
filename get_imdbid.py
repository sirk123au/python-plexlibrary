import os
import time
import requests
import json
from datetime import datetime 
import sys

def get_imdb_id(title,year):
    r = requests.get("http://www.omdbapi.com/?t={}&y={}&apikey=43a1c303".format(title,year))
    if r.status_code == 200:
        item = json.loads(r.text)
        return item.get('imdbID')
    else:
        return None

def main():
    if len(sys.argv)<2: 
        print ("No list Specified... Bye!!")
        exit()
    with open(sys.argv[1]) as foo: count = len(foo.readlines())
    f=open(sys.argv[1], "r")
    if f.mode == 'r':
        f1 = f.readlines()
        print('\033c')
        print ("Adding {} Movies...".format(count))

        for x in f1:
            title, year = x.split(',', 1)
            year = year.rstrip()
            print ("{}\t{}({})".format(get_imdb_id(title,year),title,year))


if __name__ == "__main__":
    main()

