import os
import time
import requests
import json
from datetime import datetime 
from config import ConfigParser
import sys

def add_movie(imdbid,title):
    
    # Add Missing to Radarr Work in Progress
    config = ConfigParser()
    headers = {"Content-type": "application/json"}
    url = "{}/api/movie/lookup/imdb?imdbId={}&apikey={}".format(config['radarr']['baseurl'], imdbid, config['radarr']['api_key'] )
    rsp = requests.get(url, headers=headers)
    if rsp.status_code != 200:
        print ("Failed to connect to Radarr.")
        return
    if rsp.status_code == 404:
        print ("Movie Not Found...")
        return 
    if rsp.text == "":
        title = title.replace(":","")
        url = "{}/api/movie/lookup?term={}&apikey={}".format(config['radarr']['baseurl'], title, config['radarr']['api_key'] )
        rsp = requests.get(url, headers=headers)
        if rsp.status_code != 200:
            print ("Failed to connect to Radarr.")
            return
        if rsp.status_code == 404:
            print ("Movie Not Found...")
            return
        if rsp.text == "[]":
            print ("Movie Not Found...")
            return
        data = json.loads(rsp.text)
        tmdbid = data[0]["tmdbId"]
        title = data[0]["title"]
        year = data[0]["year"]
        images = json.loads(json.dumps(data[0]["images"]))
        titleslug = data[0]["titleSlug"] 
        if year > datetime.now().year: 
            print("{} ({}) not releasd yet not added to Radarr..".format(title,year))
            return
    else:
        data = json.loads(rsp.text)
        tmdbid = data["tmdbId"]
        title = data["title"]
        year = data["year"]
        images = json.loads(json.dumps(data["images"]))
        titleslug = data["titleSlug"] 
        if year > datetime.now().year: 
            print("{} ({}) not releasd yet not added to Radarr..".format(title,year))
            return
    
    headers = {"Content-type": "application/json", "X-Api-Key": config['radarr']['api_key']}
    data = json.dumps({
        "title": title ,
        "qualityProfileId": '6' ,
        "year": year ,
        "tmdbId": tmdbid ,
        "titleslug":titleslug,
        "monitored": 'true' ,
        "minimumAvailability": "released",
        "rootFolderPath": config['radarr']['rootfolderpath'] ,
        "images": images,
        "addOptions" : {"searchForMovie" : config['radarr']['searchForMovie']}
        })
    
    url = '{}/api/movie'.format(config['radarr']['baseurl'])
    rsp = requests.post(url, headers=headers, data=data)
    if rsp.status_code == 201:
        print("{} ({}) Added to Radarr..".format(title,year))

    elif rsp.status_code == 400:
        if config['radarr']['searchForMovie'] == 'true':
            print("{} ({}) already Exists in Radarr, But Not Downloaded...".format(title, year)) 
            movie_search(imdbid)
            return
        else:
            print("{} ({}) already Exists in Radarr, But Not Downloaded, Search not Enabled...".format(title, year))
            return

def movie_search(imdbid):
    
    config = ConfigParser()
    if not os.path.exists('data.json'):
        headers = {"Content-type": "application/json", "X-Api-Key": "{}".format(config['radarr']['api_key'])}
        url = "{}/api/movie".format(config['radarr']['baseurl'])
        rsp = requests.get(url, headers=headers)
        data = json.loads(rsp.text)
        with open('data.json', 'w') as json_file: json.dump(data, json_file)
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