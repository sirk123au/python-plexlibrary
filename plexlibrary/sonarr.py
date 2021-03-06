import os
import time
import requests
import json
from datetime import datetime 
from config import ConfigParser
import sys

def add_show(imdbid, title):
    
    # Add Missing to sonarr Work in Progress
    config = ConfigParser()

    if imdbid is None: imdbid = title
    tvdbId = get_tvdbId(imdbid)
    if tvdbId == "Not Found":
        print("TVDBId {} Not found".format(title))
        return
    headers = {"Content-type": "application/json"}
    url = "{}/api/series/lookup?term=tvdb:{}&apikey={}".format(config['sonarr']['baseurl'], tvdbId , config['sonarr']['api_key'] )
    rsp = requests.get(url, headers=headers)
    if rsp.text == "": 
        print("No imdb info Found...\n")
        return
    data = json.loads(rsp.text)
    tvdbId = data[0]["tvdbId"]
    title = data[0]["title"]
    year = data[0]["year"]
    images = json.loads(json.dumps(data[0]["images"]))
    titleslug = data[0]["titleSlug"] 
    seasons = json.loads(json.dumps(data[0]["seasons"]))
    
    headers = {"Content-type": "application/json", "X-Api-Key": "{}".format(config['sonarr']['api_key'])}
    data = json.dumps({
        "title": title ,
        "year": year ,
        "tvdbId": tvdbId ,
        "titleslug": titleslug,
        "monitored": 'true' ,
        "seasonFolder": 'true',
        "qualityProfileId": '6',
        "rootFolderPath": config['sonarr']['rootfolderpath'] ,
        "images": images,
        "seasons": seasons,
        "addOptions":
                    {
                      "ignoreEpisodesWithFiles": "true",
                      "ignoreEpisodesWithoutFiles": "false",
                      "searchForMissingEpisodes": config['sonarr']['searchForShow']
                    }

        }) 
    url = '{}/api/series'.format(config['sonarr']['baseurl'])
    rsp = requests.post(url, headers=headers, data=data)
    if rsp.status_code == 201:
        print("{} ({}) Added to sonarr\n".format(title,year))
    elif rsp.status_code == 400:
        if config['sonarr']['searchForShow'] == 'true':
            print("{} ({}) already Exists in sonarr, But Not Downloaded...".format(title, year))
            show_search(imdbid)
            return
        else:
            print("{} ({}) already Exists in sonarr, But Not Downloaded, Search not Enabled... \n".format(title, year))
            return
    else:
        print ("Did not add {} ({}) to Sonarr\n".format(title,year))


def show_search(imdbid):
    
    config = ConfigParser()
    if not os.path.exists('data.json'):
        headers = {"Content-type": "application/json", "X-Api-Key": "{}".format(config['sonarr']['api_key'])}
        url = "{}/api/series".format(config['sonarr']['baseurl'])
        rsp = requests.get(url, headers=headers)
        data = json.loads(rsp.text)
        with open('data.json', 'w') as json_file: json.dump(data, json_file)
    else:
        with open('data.json') as json_file:
            data = json.load(json_file)

    for i in data:
        if i.get('imdbId','') == imdbid:
            ID = i['id']
            headers = {"Content-type": "application/json"}
            url = "{}/api/command?apikey={}".format(config['sonarr']['baseurl'], config['sonarr']['api_key'])
            data = json.dumps({"name": "SeriesSearch", "seriesId": ID})
            rsp = requests.post(url, headers=headers , data=data)
            print("Searching For {} ({})\n".format(i['title'],i['year']))
        elif title in i['title']:
            ID = i['id']
            headers = {"Content-type": "application/json"}
            url = "{}/api/command?apikey={}".format(config['sonarr']['baseurl'], config['sonarr']['api_key'])
            data = json.dumps({"name": "SeriesSearch", "seriesId": ID})
            rsp = requests.post(url, headers=headers , data=data)
            print("Searching For {} ({})\n".format(i['title'],i['year']))

def get_tvdbId(imdbid):
    headers = {"Content-type": "application/json",  "Authorization": "Bearer {}".format(get_token())}
    if imdbid.find("tt") == -1:
       url = "https://api.thetvdb.com/search/series?name={}".format(imdbid)
    else:
       url = "https://api.thetvdb.com/search/series?imdbId={}".format(imdbid)
    rsp = requests.get(url, headers=headers)
    if rsp.status_code == 200:
        tmdb_data = json.loads(rsp.text)
        return tmdb_data['data'][0]['id']
    elif rsp.status_code == 404:
        return "Not Found"
    else: 
        print("Failed with status {}\n".format(rsp.status_code))
        return "Not Found"

def get_token():
    config = ConfigParser()
    data = {
        "apikey": "{}".format(config['tvdb']['api_key']),
        "userkey": "{}".format(config['tvdb']['user_key']), 
        "username": "{}".format(config['tvdb']['username']) 
        }
    url = "https://api.thetvdb.com/login"
    rsp = requests.post(url, json=data)
    data = json.loads(rsp.text)
    return data['token']
