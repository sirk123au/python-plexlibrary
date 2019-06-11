import os
import time
import requests
import json
from datetime import datetime 
from config import ConfigParser

def add_movie(tmdbid , title):
    
    # Add Missing to Radarr Work in Progress
    config = ConfigParser()

    if not os.path.exists('data.json'):
        headers = {"Content-type": "application/json", "X-Api-Key": "{}".format(config['radarr']['api_key'])}
        url = "{}/api/movie".format(config['radarr']['api_key'])
        rsp = requests.get(url, headers=headers)
        data = json.loads(rsp.text)
        with open('data.json', 'w') as outfile: json.dump(data, outfile)
    else:
        with open('data.json') as json_file: data = json.load(json_file)

    for i in data:
        if i['title'] == title:
            tmdbid = i["tmdbId"]
            title = i["title"]
            year = i["year"]
            poster=i["images"][0]['url']
            titleslug = i["titleSlug"]
            hasfile = i["hasFile"]
        else:
            headers = {"Content-type": "application/json"}
            url = "{}/api/movie/lookup/imdb?imdbId={}&apikey={}"
            .format(config['radarr']['baseurl'], tmdbid , config['radarr']['api_key'] )
            rsp = requests.get(url, headers=headers)
            data = json.loads(rsp.text)
            print('{} ({}) already Exists in Radarr'.format(title,year))
            movie_search(title)
        
    if hasfile:
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
            "addOptions" : {"searchForMovie" : "true"}
            })

        url = '{}/api/movie'.format(config['radarr']['baseurl'])
        rsp = requests.post(url, headers=headers, data=data)
        print("{} ({}) Added to Radarr".format(title,year))
    else:
            print('Problem with the request. Exiting.')
            exit()


def movie_search(title):
    
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
        if i['title'] == title:
            headers = {"Content-type": "application/json"}
            url = "{}/api/command?apikey={}".format(config['radarr']['baseurl'], config['radarr']['api_key'])
            data = json.dumps({"name": "MoviesSearch", "movieIds": [i['id']]})
            rsp = requests.post(url, headers=headers , data=data)
            print("Searching For {} ({})".format(i['title'],i['year']))
