import os
import time
import requests
import json
from datetime import datetime 
from config import ConfigParser
import sys

def add_movie(imdbid):
    
    # Add Missing to Radarr Work in Progress
    config = ConfigParser()

      
    if not os.path.exists('data.json'):
        headers = {"Content-type": "application/json", "X-Api-Key": "{}".format(config['radarr']['api_key'])}
        url = "{}/api/movie".format(config['radarr']['baseurl'])
        rsp = requests.get(url, headers=headers)
        data = json.loads(rsp.text)
        with open('data.json', 'w') as json_file: json.dump(data, json_file)
    else:
        with open('data.json') as json_file: data = json.load(json_file)

    for i in data:
        if i.get('imdbId','') == imdbid:
            tmdbid = i.get('tmdbId','')
            title = i["title"]
            year = i["year"]
            poster = i["images"][0]['url']
            titleslug = i["titleSlug"]

            if not i["isAvailable"]:
                print('{} ({}) Has not been released yet...\n'.format(title,year))
                return
            if i["hasFile"]:
                print('{} ({}) already Exists in Radarr...\n'.format(title,year))               
                return
            else:
                if config['radarr']['searchForMovie'] == 'true':
                    print("{} ({}) already Exists in Radarr, But Not Downloaded...".format(title, year)) 
                    movie_search(imdbid)
                else:
                    print("{} ({}) already Exists in Radarr, But Not Downloaded, Search not Enabled... \n".format(title, year))

                return
    headers = {"Content-type": "application/json"}
    url = "{}/api/movie/lookup/imdb?imdbId={}&apikey={}".format(config['radarr']['baseurl'], imdbid, config['radarr']['api_key'] )
    rsp = requests.get(url, headers=headers)
    if rsp.text == "": 
        print("No imdb info Found...\n")
        time.sleep(0.5)
        return
    data = json.loads(rsp.text)
    tmdbid = data["tmdbId"]
    title = data["title"]
    year = data["year"]
    poster=data["images"][0]['url']
    titleslug = data["titleSlug"] 

    headers = {"Content-type": "application/json", "X-Api-Key": "{}".format(config['radarr']['api_key'])}
    data = json.dumps({
        "title": "{}".format(title) ,
        "qualityProfileId": '6' ,
        "year": "{}".format(year) ,
        "tmdbId": "{}".format(tmdbid) ,
        "titleslug":"{}".format(titleslug),
        "monitored": 'true' ,
        "minimumAvailability": "released",
        "rootFolderPath": '{}'.format(config['radarr']['rootfolderpath']) ,
        "images": [{
                    "covertype": "poster", 
                    "url": "{}".format(poster)
                   }],
        "addOptions" : {"searchForMovie" : "{}".format(config['radarr']['searchForMovie'])}
        })
    
    url = '{}/api/movie'.format(config['radarr']['baseurl'])
    rsp = requests.post(url, headers=headers, data=data)
    print("{} ({}) Added to Radarr\n".format(title,year))


def movie_search(imdbid):
    
    config = ConfigParser()
    if not os.path.exists('data.json'):
        headers = {"Content-type": "application/json", "X-Api-Key": "{}".format(config['radarr']['api_key'])}
        url = "{}/api/movie".format(config['radarr']['baseurl'])
        rsp = requests.get(url, headers=headers)
        data = json.loads(rsp.text)
        with open('data.json', 'w') as json_file:  
            json.dump(data, json_file)
            data = json.load(json_file)
    else:
        with open('data.json') as json_file:
            data = json.load(json_file)

    for i in data:
        if i.get('imdbId','') == imdbid:
            headers = {"Content-type": "application/json"}
            url = "{}/api/command?apikey={}".format(config['radarr']['baseurl'], config['radarr']['api_key'])
            data = json.dumps({"name": "MoviesSearch", "movieIds": [i['id']]})
            rsp = requests.post(url, headers=headers , data=data)
            print("Searching For {} ({})\n".format(i['title'],i['year']))