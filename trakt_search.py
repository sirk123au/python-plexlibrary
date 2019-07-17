import requests
import json
from datetime import datetime 
import os
import sys
import argparse

headers = {
  'Content-Type': 'application/json',
  'trakt-api-version': '2',
  'trakt-api-key': 'aa6b79a0ed7c3f75e29b529290268f8ad734fa71e3c07f86ba695e343d1ffcc3'
}

parser = argparse.ArgumentParser("Trakt User List Search")
parser.add_argument('search' , help='Search Trakt for User Lists')
parser.add_argument('-l', dest='limit', const=10, default=30, action='store', nargs='?', type=int, help='Only print the head of the output')

args = parser.parse_args()

if args.search:
	request = requests.get('https://api.trakt.tv/search/list?query={}&limit={}'.format(args.search,args.limit), headers=headers)
	data = json.loads(request.text)
	#print(json.dumps(data, indent=4, sort_keys=True))

	for i in data:
		username = i['list']['user']['username']
		slug = i['list']['ids']['slug']
		print("- 'https://trakt.tv/users/{}/lists/{}'".format(username,slug))



# headers = {"Content-type": "application/json"}
# url = "https://cloud.kdata.net.au/radarr/api/movie/lookup/imdb?imdbId=tt0096639&apikey=a6db7a0ddf18311f7b97d78ee6d8806ff"
# rsp = requests.get(url, headers=headers)
# if rsp.text == "": exit()
# data = json.loads(rsp.text)
# print(json.dumps(data, indent=4, sort_keys=True))


# if not os.path.exists('data.json'):
# 	headers = {"Content-type": "application/json", "X-Api-Key": "a6db7a0ddf18311f7b97d78ee6d8806ff"}
# 	url = "https://cloud.kdata.net.au/radarr/api/movie"
# 	rsp = requests.get(url, headers=headers)
# 	data = json.loads(rsp.text)
# 	with open('data.json', 'w') as outfile: json.dump(data, outfile)
# else:
# 	with open('data.json') as json_file:
# 		data = json.load(json_file)

# for i in data:
# 	tmdbid = i["tmdbId"]
# 	title = i["title"]
# 	year = i["year"]
# 	poster=i["images"][0]['url']
# 	titleslug = i["titleSlug"]
# 	hasfile = i["hasFile"]
# 	ID = i["id"]
# 	#if not i["imdbId"] is None:	
# 	imdbId = i.get('imdbId','')
# 	print(u"{} {} \t {} \t {}".format(ID, tmdbid,imdbId,title))
	#print(json.dumps(i, indent=4, sort_keys=True))

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