from google.oauth2.credentials import Credentials
from apiclient.discovery import build
import os

import googleapiclient.discovery
credential = Credentials(
    None,
    refresh_token="1/tDLHevylia1lB56YL_ClIRDsg3kLFhE-DFYCnJjE0Ss",
    token_uri="https://accounts.google.com/o/oauth2/token",
    client_id="299112906847-sq47gf54fu77vfv9sdbvb4jjh6so623p.apps.googleusercontent.com",
    client_secret="okzo11GZoMhqphzI24bkxCVg"
)


#credential = Credentials(
#     None,
#     refresh_token="1/qbuoUY89hKM97-zHmS135-56jdcbgz5ndJDk37AADE6xvHcRptNoW2sqw8Obwz0j",
#     token_uri="https://accounts.google.com/o/oauth2/token",
#     client_id="160678406095-uk4sigeeaodndkf8h25phmjhu2gvvlb3.apps.googleusercontent.com",
#     client_secret="k-2oWbtwNsz55BZEgw_fGu6Q"
# )

# zelalem
# credential = Credentials(
#     None,
#     refresh_token="1/7iHPSeOuXhwgUe1BFKdQqB3cBsqerNuIqBHJpI3Ibi0",
#     token_uri="https://accounts.google.com/o/oauth2/token",
#     client_id="371021129033-7hpjcnijmpdapusvd2sd5hq3v2pa5a4l.apps.googleusercontent.com",
#     client_secret="N1wY4OcDeBVeSZIyO2pBeE62"
# )

#absolapso
# credential = Credentials(
#     None,
#     refresh_token="1/AWpIp5JShSop25_hZYrF7ZvNtHqwH-F7o55wE4kzgWY",
#     token_uri="https://accounts.google.com/o/oauth2/token",
#     client_id="521831242723-fagjjn62iuqslf50v2riu1tb941e58u3.apps.googleusercontent.com",
#     client_secret="NFlkPfQQmfjxfBX-gm50fkmf"
# )



youtube = build('youtube', 'v3', credentials=credential)


class Comment():
    def get_top_commment(self, videoId):
        try:
            api_service_name = "youtube"
            api_version = "v3"
            DEVELOPER_KEY = "AIzaSyDzZW4RaeAQaHLKyBnhOwZLOAyj4JEmvc0"

            self.youtube = googleapiclient.discovery.build(
                api_service_name, api_version, developerKey=DEVELOPER_KEY)

            request = youtube.commentThreads().list(
                part="snippet,replies",
                moderationStatus="published",
                order="time",
                videoId=videoId
            )

            response = request.execute()
            ret=""
            for val in response['items']:
                my=val['snippet']['topLevelComment']['snippet']['authorChannelId']['value']
                if  my !=  "UC2m94T3rlPgTQqZ1mx-x3sQ" and my != "UCxyR9oOn58cVYE3U_359e0g" and  my !=  "UCSWbUXldqBN4iu6603jL2xA" and my != "UCKyJzwkozJ8paOdfITQEUyA":
                    ret=val['snippet']['topLevelComment']['snippet']['textOriginal']
    #                print(val['snippet']['topLevelComment']['snippet']['authorChannelId']['value'])
                    break
            return ret
        except:
            print("exception")
            return



    def __init__(self, channelId, videoId, textOriginal):
        my_comment=str(textOriginal)+" "+ str(self.get_top_commment(videoId))
        self.request = youtube.commentThreads().insert(
            part="snippet",
            body={
                "snippet": {
                    "channelId": channelId,
                    "videoId": videoId,
                    "topLevelComment": {
                        "snippet": {
                            "textOriginal": my_comment
                        }
                    }
                }
            })
        print(my_comment)
        try:
            self.response = self.request.execute()
        except:print("exception")
        self.comment=my_comment
