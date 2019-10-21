import os
import time
import requests
import json
from datetime import datetime 
import sys

# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

api_key = 'a6db7a0ddf18311f7b97d78ee6d8806ff'
baseurl = 'http://cloud.kdata.net.au/radarr'
rootfolderpath = '/home/hd15/sirk123au/mnt/gdrive/Media/Movies/'
searchForMovie = "True"

def add_movie(title, year):
    imdbid = get_imdb_id(title,year)
    headers = {"Content-type": "application/json", 'Accept':'application/json'}
    url = "{}/api/movie/lookup/imdb?imdbId={}&apikey={}".format(baseurl, imdbid, api_key)
    rsp = requests.get(url, headers=headers)
    if rsp.status_code == 200:
        if rsp.text == "":
            url = "{}/api/movie/movie/lookup?term={}&apikey={}".format(baseurl, title.replace(" ","%20"), api_key)
            rsp = requests.get(url, headers=headers)
            data = json.loads(rsp.text)
            if data['message'] == "NotFound" :
                print ("\033[1;31;40m{} ({}) Not found, Not added to Radarr..".format(title,year))
                return
            tmdbid = data["tmdbId"]
            title = data["title"]
            year = data['year']
            images = json.loads(json.dumps(data["images"]))
            titleslug = data["titleSlug"]
            Rdata = json.dumps({
                "title": title , 
                "qualityProfileId": '6' , 
                "year": year ,
                "tmdbId": tmdbid ,
                "titleslug":titleslug, 
                "monitored": 'true' , 
                "minimumAvailability": "released",
                "rootFolderPath": rootfolderpath ,
                "images": images,
                "addOptions" : {"searchForMovie" : searchForMovie}
                })
                
        else:
            data = json.loads(rsp.text)
            tmdbid = data["tmdbId"]
            title = data["title"]
            year = data['year']
            images = json.loads(json.dumps(data["images"]))
            titleslug = data["titleSlug"]
            Rdata = json.dumps({
                "title": title , 
                "qualityProfileId": '6' , 
                "year": year ,
                "tmdbId": tmdbid ,
                "titleslug":titleslug, 
                "monitored": 'true' , 
                "minimumAvailability": "released",
                "rootFolderPath": rootfolderpath ,
                "images": images,
                "addOptions" : {"searchForMovie" : searchForMovie}})

    elif rsp.status_code == 404:
        print ("Movie Not Found...")
        return 
    elif rsp.status_code == 500:
        print ("Unauthorized Access..")
        return
    else:
        print ("Failed to connect to Radarr.")
        return
    
    headers = {"Content-type": "application/json", 'Accept':'application/json', "X-Api-Key": api_key}
    url = '{}/api/movie'.format(baseurl)
    rsp = requests.post(url, headers=headers, data=Rdata)
    if rsp.status_code == 201:
        print("\033[1;32;40m{} ({}) Added to Radarr, \033[1;35;40mNow Searching...".format(title,year))
    elif rsp.status_code == 400:
        if searchForMovie ==  "True":
            movie_search(imdbid)
            return
        else:
            print("\033[1;32;40m{} ({}) already Exists in Radarr, \033[1;31;40mSearch Disabled...".format(title,year))
            return

def get_imdb_id(title,year):
    headers = {"Content-type": "application/json", 'Accept':'application/json'}
    r = requests.get("http://www.omdbapi.com/?t={}&y={}&apikey=43a1c303".format(title,year), headers=headers)
    if r.status_code == 200:
        item = json.loads(r.text)
        return item.get('imdbID')
    else:
        return None

def movie_search(imdbid):
    
    if not os.path.exists('data.json'):
        headers = {"Content-type": "application/json", "X-Api-Key": api_key }
        url = "{}/api/movie".format(baseurl)
        rsp = requests.get(url, headers=headers)
        data = json.loads(rsp.text)
        with open('data.json', 'w') as json_file: json.dump(data, json_file)
    else:
        with open('data.json') as json_file:
            data = json.load(json_file)
 
    for i in data:
            if i.get('imdbId','') == imdbid:
                if i['downloaded'] == False:
                    headers = {"Content-type": "application/json"}
                    url = "{}/api/command?apikey={}".format(baseurl, api_key)
                    data = json.dumps({"name": "MoviesSearch", "movieIds": [i['id']]})
                    rsp = requests.post(url, headers=headers , data=data)
                    print("\033[1;34;40m{} ({}) already Exists in Radarr, But Not Downloaded \033[1;35;40mNow Searching...".format(i['title'],i['year']))
                else:
                    print("\033[1;32;40m{} ({}) already Exists in Radarr and has been Downloaded...".format(i['title'], i['year'])) 
                    return

def main():
    if len(sys.argv)<2: 
        print ("No list Specified... Bye!!")
        exit()
    os.remove('data.json')
    with open(sys.argv[1]) as foo: count = len(foo.readlines())
    f=open(sys.argv[1], "r")
    if f.mode == 'r':
        f1 = f.readlines()
        print('\033c')
        print ("Adding {} Movies... \033[1;33;40m:)".format(count))
        for x in f1:
            title, year = x.split(',', 1)
            year = year.rstrip()
            add_movie(title, year)
        print ("\033[1;37;40mDone...")


if __name__ == "__main__":
    main()

