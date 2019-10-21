import os
import time
import requests
import json
from datetime import datetime 
from plexlibrary.config import ConfigParser
import sys

def add_show(title):
    
    # Add Missing to sonarr Work in Progress
    config = ConfigParser()

    imdbid = get_imdbid(title)
    print ("{}\t\t{}".format(title,imdbid))
    tvdbId = get_tvdbId(imdbid)
    if imdbid == "Not Found": return
    if tvdbId == "Not Found": return
    

    headers = {"Content-type": "application/json"}
    url = "{}/api/series/lookup?term=tvdb:{}&apikey={}".format(config['sonarr']['baseurl'], tvdbId , config['sonarr']['api_key'] )
    rsp = requests.get(url, headers=headers)
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
    data = json.loads(rsp.text)
    if rsp.status_code == 201:
        print("{} ({}) Added to sonarr\n".format(title,year))
    elif rsp.status_code == 400:
        if config['sonarr']['searchForShow'] == 'true':
            print("{} ({}) already Exists in sonarr, But Not Downloaded...".format(title, year))
            show_search(imdbid,title)
            return
        else:
            print("{} ({}) already Exists in sonarr, But Not Downloaded, Search not Enabled...\n".format(title, year))
            return
    else:
        print ("Did not add {} ({}) to Sonarr\n".format(title,year))


def show_search(imdbid, title):
    config = ConfigParser()
    if not os.path.exists('data.json'):
        headers = {"Content-type": "application/json", "X-Api-Key": "{}".format(config['sonarr']['api_key'])}
        url = "{}/api/series".format(config['sonarr']['baseurl'])
        rsp = requests.get(url, headers=headers)
        data = json.loads(rsp.text)
        with open('data.json', 'w') as json_file:  
            json.dump(data, json_file)
            data = json.load(json_file)
    else:
        with open('data.json') as json_file:
            data = json.load(json_file)

    for i in data:
        if str(i.get('imdbId','')) == imdbid:
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

def get_imdbid(title):
    headers = {"Content-type": "application/json",  "Authorization": "Bearer {}".format(get_token())}
    url = "https://api.thetvdb.com/search/series?name={}".format(title)
    rsp = requests.get(url, headers=headers)
    if rsp.status_code == 200:
        tmdb_data = json.loads(rsp.text)
        url = "https://api.thetvdb.com/series/{}".format(tmdb_data['data'][0]['id'])
        rsp = requests.get(url, headers=headers)
        if rsp.status_code == 200:
            data = json.loads(rsp.text)
            return data['data']['imdbId']
        elif rsp.status_code == 404:
            print("No IMDBiD found for {}\n".format(title))
            return "Not Found"
    elif rsp.status_code == 404:
        print("{}\t\tNo IMDBiD found\n".format(title))
        return "Not Found"
    else: 
        print("Failed with status {}\n".format(rsp.status_code))
        return "Not Found"

def get_tvdbId(imdbid):
    headers = {"Content-type": "application/json",  "Authorization": "Bearer {}".format(get_token())}
    url = "https://api.thetvdb.com/search/series?imdbId={}".format(imdbid)
    rsp = requests.get(url, headers=headers)

    if rsp.status_code == 200:
        tmdb_data = json.loads(rsp.text)
        return tmdb_data['data'][0]['id']
    elif rsp.status_code == 404:
        print("No TVDBid found...\n")
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

def main():
    with open(sys.argv[1]) as foo: count = len(foo.readlines())
    f=open(sys.argv[1], "r")
    if f.mode == 'r':
        f1 = f.readlines()
        print ("Adding {} TV Shows".format(count))
        time.sleep(1)
        print('\033c')
        for x in f1:
            add_show(x.rstrip())


if __name__ == "__main__":
    main()

