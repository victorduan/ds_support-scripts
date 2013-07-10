import requests, json

#youtube_link = "https://gdata.youtube.com/feeds/api/videos?author=ToyotaUSA&start-index=15001&v=2&alt=json&max-results=50"
#r = requests.get(youtube_link)

#print r.json()
run = True
index = 1
video_list = []

while run:
    youtube_url = "https://gdata.youtube.com/feeds/api/videos?author=ToyotaUSA&start-index={0}&v=2&alt=json&max-results=50&orderby=published".format(index)
    r = requests.get(youtube_url)
    
    try:
        for entry in r.json()['feed']['entry']:
            video_id = entry['media$group']['yt$videoid']['$t']
            video_list.append(video_id)
        index += 50
        print index
    except Exception, err:
        run = False
        
csdl = 'youtube.videolink contains_any "{0}"'.format(",".join(video_list))

print csdl