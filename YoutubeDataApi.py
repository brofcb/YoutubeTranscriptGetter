import json
import re
import os
import sys
import urllib.request
import requests
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from moviepy.editor import *
from bs4 import BeautifulSoup 
import requests 

API_KEY = None

# This class holds all the video data
class YoutubeStats:
    def __init__(self, url, id, API_KEY):
        
        #You can use the youtube data api v3 by uncommenting the following 3 lines and passing an API key to the class 
        #callUrl = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={id}&key={API_KEY}"
        #self.respose = requests.get(callUrl)
        #self.data = json.loads(self.respose.text)
        self.captionData = YouTubeTranscriptApi.get_transcript(id)
        self.url = url
        self.id = id

    def printData(self):
        print(self.data)

    def getURL(self):
        return self.url
    
    def getID(self):
        return self.id
    # Returns the video title
    def getVideoTitle(self):
        source = requests.get(self.url).text
        soup = BeautifulSoup(source,'html.parser')
        Title = soup.title.text
        print(Title)
        Title = Title[:-10] 
        return Title

    # Returns the video description as a string
    def getVideoDescription(self):
        return self.data["items"][0]["snippet"]["description"]

    # Downloads the video from youtube with 360p resolution
    # given the video URL nad the name of the file
    def downloadVideo(self, url, title):
        path = os.getcwd() + '/videos'
        title = reNameTitle(title)
        YouTube(url).streams.first().download(output_path=path, filename=title)

    # Coverts video from mp4 to mp3 given the name of
    # the file and the type of the output file eg: mp3, wav
    def convertVideoToSound(self, title, type):
        VideoPath = os.getcwd() + '/videos/'
        path = os.getcwd() + '/audio/'
        title = reNameTitle(title)
        video = VideoFileClip(VideoPath + title + '.mp4')
        video.audio.write_audiofile(path + title + '.' + type)

    # Returns the video transcript as a dictionary with times
    def getVideoTranscript(self):
        return self.captionData

    # Return the video transcript as a string
    def getVideoTranscriptString(self):
        transcript = ""
        addNewLine = False
        for caption in self.captionData:
            if addNewLine:
                transcript += str(caption["text"] + "\n")
                addNewLine = False
            else:
                transcript += str(caption["text"])
                addNewLine = True
        return transcript



# This function create a file for every video
# and it assigns the file name to the title of
# that video. It then writes the title, description
# and the transcript to the file
def writeToVideoFile(youtubeStats):
    path = createDirectory('video_scripts')
    i = 0
    for stats in youtubeStats:
        title = stats.getVideoTitle()
        #description = stats.getVideoDescription()
        transcript = stats.getVideoTranscriptString()
        print("{0} Writing to file...".format(i+1))
        i+=1
        with open(path + '/'f"{reNameTitle(title)}.txt", "w") as file:
            file.write("Title\n\n" + title)
            file.write(
                "\n--------------------------------------------------------------------\n")
            #file.write("\nDescription\n\n" + description)
            #file.write(
            #    "\n\n--------------------------------------------------------------------\n")
            file.write("\nTranscript\n\n" + transcript)
            file.write(
                "\n--------------------------------------------------------------------\n")

def writeToJsonFile(youtubeStats):
    path = createDirectory('Json_scripts')
    i = 0
    for stats in youtubeStats:
        title = stats.getVideoTitle()
        transcript = stats.getVideoTranscript()
        print("{0} Writing to json file...".format(i+1))
        i+=1
        with open(path + '/'f"{reNameTitle(title)}.json", "w") as file:
            json.dump(transcript, file)
            
#download all the videos in the input file
def downloadAllVideos(youtubeStats):
    createDirectory('videos')   
    i = 0
    for stats in youtubeStats:
        print("{0} Downloading...".format(i+1))
        i+=1
        stats.downloadVideo(stats.getURL(), stats.getVideoTitle())        

def convertAllVideosToSound(youtubeStats):
    createDirectory('audio')
    for stats in youtubeStats:
        stats.convertVideoToSound(stats.getVideoTitle(), 'wav')


# Helper function to rename the file
def reNameTitle(title):
    title = re.sub('[\W_]+', "_", title)
    return title.lower()

# Helper function to create a directory
def createDirectory(name):
    path = os.getcwd() + '/'+ name
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)
    return path

# Reads a list of URLs from a given file
# and parses them to video IDs.
# Returns a list of URLs and video IDs
def readFile():
    #fileName = input("Enter the input file: ")
    videoIds = []
    urls = []
    fileName = sys.argv[1]
    with open(fileName, "r") as file:
        for line in file:
            videoIds.append(line.split("=", 1)[1].strip())
            urls.append(line.strip())
    return videoIds, urls




# A driver function to run the script
def main():
    
    #Uncomment if you want to use the Youtube data API
    #ApiFile = open("API_KEY.txt", "r")
    #API_KEY = ApiFile.readline()
    
    #Reading all the urls from the file
    videoIds, urls = readFile()
    youtubeStats = []
    #Populating the objects with the data
    for i, id in enumerate(videoIds):
        youtubeStats.append(YoutubeStats(urls[i], id, API_KEY))
    
    downloadAllVideos(youtubeStats)
    writeToVideoFile(youtubeStats)
    writeToJsonFile(youtubeStats)
    convertAllVideosToSound(youtubeStats)

if __name__ == "__main__":
    main()