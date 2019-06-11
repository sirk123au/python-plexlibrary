import requests
import json
from datetime import datetime 


headers = {"Content-type": "application/json", "X-Api-Key": "a6db7a0ddf18311f7b97d78ee6d8806ff"}
url = "https://cloud.kdata.net.au/radarr/api/movie"
rsp = requests.get(url, headers=headers)
data = json.loads(rsp.text)

for i in data:
    if i['title'] == 'All Nighter':
		headers = {"Content-type": "application/json"}
		url = "https://cloud.kdata.net.au/radarr/api/command?apikey=a6db7a0ddf18311f7b97d78ee6d8806ff"
		RID = i['id']
		data = json.dumps({"name": "MoviesSearch", "movieIds": [RID]})
		rsp = requests.post(url, headers=headers , data=data)
		print("Searching For {}".format(i['title']))
		print(data)
		print(rsp.text)

# headers = {"Content-type": "application/json", "X-Api-Key": "a6db7a0ddf18311f7b97d78ee6d8806ff"}
# url = "https://cloud.kdata.net.au/radarr/api/command"
# data = {'name': 'RefreshMovie' , 'movieId': "{}".format(tmdbid)}
# rsp = requests.get(url, headers=headers , data=data)

# headers = {"Content-type": "application/json"}
# params = (
# 			('api_key', '15337bf0d95e26b82af1172a6d910a32'), 
# 			('language', 'en-US'),
# 			('external_source', 'imdb_id'),
# 		 )
# url = "https://api.themoviedb.org/3/find/{}".format("tt0065214")
# rsp = requests.get(url, headers=headers, params=params)
# imdb_data = json.loads(rsp.text)
# if imdb_data["movie_results"]: 
# 	tmdbid = imdb_data["movie_results"][0]["id"]
# 	title = imdb_data["movie_results"][0]["title"]
# 	str = imdb_data["movie_results"][0]["release_date"]
# 	if str == "": str = "2019-12-30"
# 	x = datetime.strptime(str, '%Y-%m-%d')  
# 	year = x.strftime('%Y')

# 	poster = "https://image.tmdb.org/t/p/original{0}".format(imdb_data["movie_results"][0]["poster_path"])
# 	slug = "{0}-{1}".format(title.lower() , tmdbid)
# 	headers = {"Content-type": "application/json", "X-Api-Key": "a6db7a0ddf18311f7b97d78ee6d8806ff"}
# 	data = json.dumps({
# 		"title": "{}".format(title) ,
# 		"qualityProfileId": '6' ,
# 		"year": "{}".format(year) ,
# 		"tmdbId": "{}".format(tmdbid) ,
# 		"titleslug":"{}".format(slug),
# 		"monitored": 'true' ,
# 		"rootFolderPath": '/home/hd15/sirk123au/mnt/gdrive/Media/Movies/' ,
# 		"images": [{
# 					"covertype": "poster", 
# 					"url": "https://image.tmdb.org/t/p/original/iVpNb776SBRslpXBd20G38i9oBy.jpg"
# 				   }]
# 		})

# 	url = "https://cloud.kdata.net.au/radarr/api/movie"
# 	rsp = requests.post(url, headers=headers, data=data)


# 	print(rsp.text)
# else:
# 	print ("No Data returned from themoviedb")