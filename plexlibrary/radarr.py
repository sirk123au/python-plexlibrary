import os
import time
import requests
import json
from datetime import datetime 


def add_movie(tmdbid):

    # Add Missing to Radarr Work in Progress
    headers = {"Content-type": "application/json"}
    params = (
                ('api_key', '15337bf0d95e26b82af1172a6d910a32'), 
                ('language', 'en-US'),
                ('external_source', 'imdb_id'),
             )
    url = "https://api.themoviedb.org/3/find/{}".format(tmdbid)
    rsp = requests.get(url, headers=headers, params=params)
    imdb_data = json.loads(rsp.text)
    if imdb_data["movie_results"]: 
        tmdbid = imdb_data["movie_results"][0]["id"]
        title = imdb_data["movie_results"][0]["title"]
        str = imdb_data["movie_results"][0]["release_date"]
        if str == "": str = "2019-12-30"
        x = datetime.strptime(str, '%Y-%m-%d')  
        year = x.strftime('%Y')
        poster = "https://image.tmdb.org/t/p/original{0}".format(imdb_data["movie_results"][0]["poster_path"])
        slug = "{0}-{1}".format(title.lower() , tmdbid)
        headers = {"Content-type": "application/json", "X-Api-Key": "a6db7a0ddf18311f7b97d78ee6d8806ff"}
        data = json.dumps({
            "title": "{}".format(title) ,
            "qualityProfileId": '6' ,
            "year": "{}".format(year) ,
            "tmdbId": "{}".format(tmdbid) ,
            "titleslug":"{}".format(slug),
            "monitored": 'true' ,
            "minimumAvailability": "released",
            "rootFolderPath": '/home/hd15/sirk123au/mnt/gdrive/Media/Movies/' ,
            "images": [{
                        "covertype": "poster", 
                        "url": "{}".format(poster)
                       }],
            "addOptions" : {"searchForMovie" : "true"}
            })

        url = "https://cloud.kdata.net.au/radarr/api/movie"
        rsp = requests.post(url, headers=headers, data=data)

        if rsp.status_code == 400:
            print('{} ({}) already Exists in Radarr'.format(title,year))
            movie_search(title)
        elif rsp.status_code == 500:
            print('{} ({}) already Exists in Radarr'.format(title,year))
            movie_search(title)
        elif rsp.status_code == 201:
            print("{} ({}) Added to Radarr".format(title,year))
        elif rsp.status_code != 200:
            print('Status:', rsp.status_code, 'Problem with the request. Exiting.')
            exit()
    else:
        print ("No Data returned from themoviedb")


def movie_search(title):

    headers = {"Content-type": "application/json", "X-Api-Key": "a6db7a0ddf18311f7b97d78ee6d8806ff"}
    url = "https://cloud.kdata.net.au/radarr/api/movie"
    rsp = requests.get(url, headers=headers)
    data = json.loads(rsp.text)
    
    if not os.path.exists('data.json'):
        with open('data.json', 'w') as outfile:  
            json.dump(data, outfile)
            data = json.load(outfile)
    else:
        with open('data.json') as json_file:
            data = json.load(json_file)

    for i in data:
        if i['title'] == title:
            headers = {"Content-type": "application/json"}
            url = "https://cloud.kdata.net.au/radarr/api/command?apikey=a6db7a0ddf18311f7b97d78ee6d8806ff"
            RID = i['id']
            data = json.dumps({"name": "MoviesSearch", "movieIds": [RID]})
            rsp = requests.post(url, headers=headers , data=data)
            print("Searching For {} ({})".format(i['title'],i['year']))
