import os
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import sys

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "secret_key.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.playlistItems().list(
        part="snippet",
        maxResults=300,
        playlistId=sys.argv[1]
    )
    response = request.execute()
    run = False
    if "nextPageToken" in response.keys():
        pageToken = response["nextPageToken"]
        run = True
    
    videoIds = []
    
    i = 0
    for item in response["items"]:
        videoIds.append(item["snippet"]["resourceId"]["videoId"])
        i += 1
        print(i)
    
    
    while run:
        request = youtube.playlistItems().list(
            part="snippet",
            maxResults=300,
            playlistId=sys.argv[1],
            pageToken= pageToken
        )
        response = request.execute()
        if "nextPageToken" in response.keys():
            pageToken = response["nextPageToken"]
        else:
            run = False
        for item in response["items"]:
            videoIds.append(item["snippet"]["resourceId"]["videoId"])
            i += 1
            print(i)
    link = "https://www.youtube.com/watch?v="
    videoLinks = [link + id for id in videoIds]
    with open(sys.argv[2], "w") as file:
        file.writelines('\n'.join(videoLinks)+'\n')
    

if __name__ == "__main__":
    main()