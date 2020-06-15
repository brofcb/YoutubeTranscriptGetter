import json
import re
import urllib.request
import requests
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi


API_KEY = "AIzaSyD32jTMAOgRKs9Ao4wn9Px-IF94CunvWyo"

#This class holds all the video data
class YoutubeStats:
    def __init__(self, url, id):
        self.respose = requests.get(url)
        self.data = json.loads(self.respose.text)
        self.captionData = YouTubeTranscriptApi.get_transcript(id)

    def printData(self):
        print(self.data)

    def getVideoTitle(self):
        return self.data["items"][0]["snippet"]["title"]

    def getVideoDescription(self):
        return self.data["items"][0]["snippet"]["description"]

    def downloadVideo(self, url, title):
        YouTube(url).streams.first().download(filename=title)
    
    def getVideoTranscript(self):
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
    
                    
#This function create a file for every video
#and it assigns the file name to the title of
#that video. It then writes the title, description 
#and the transcript to the file
def writeToVideoFile(videoIds, urls):
    for i, id in enumerate(videoIds):
        url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={id}&key={API_KEY}"
        
        yt_stats = YoutubeStats(url, videoIds[i])
        title = yt_stats.getVideoTitle()
        description = yt_stats.getVideoDescription()
        transcript = yt_stats.getVideoTranscript()
        print("Finshed: " + str(i+1))
        with open(f"{title}.txt", "w") as file:
            file.write("Title\n\n"+ title)
            file.write("\n--------------------------------------------------------------------\n")
            file.write("\nDescription\n\n"+ description)
            file.write("\n\n--------------------------------------------------------------------\n")
            file.write("\nTranscript\n\n" + transcript)
            file.write("\n--------------------------------------------------------------------\n")


#Reads a list of URLs from a given file 
#and parses them to video IDs.
#Returns a list of URLs and video IDs 
def readFile():
    fileName = input("Enter the input file: ")
    videoIds = []
    urls = []
    with open(fileName, "r") as file:
        for line in file:
            videoIds.append(line.split("=", 1)[1].strip())
            urls.append(line.strip())
    return videoIds, urls


#Helper function to rename the file
def reNameTitle(title):
    title = re.sub('[\W_]+', "_", title)
    return title.lower()


#A driver function to run the script
def main():
    videoIds, urls = readFile()
    writeToVideoFile(videoIds, urls)    

if __name__ == "__main__":
    main()
