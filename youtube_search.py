import json
import dot_dict
from apiclient.discovery import build


class YoutubeSearch():
    def __init__(self, CREDENTIALS_PATH, QUERY, MAX_RESULT, NEXT_PAGE_TOKEN, PUBLISHED_AFTER, PUBLISHED_BEFORE):
        try:
            with open(CREDENTIALS_PATH) as f:
                data = json.load(f)
                api = dot_dict.DotDict(data)
                DEVELOPER_KEY = api.developer_key
                YOUTUBE_API_SERVICE_NAME = api.youtube_api_service_name
                YOUTUBE_API_VERSION = api.youtube_api_version

                youtube = build(YOUTUBE_API_SERVICE_NAME,
                                YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

                if QUERY:
                    if NEXT_PAGE_TOKEN:
                        #                        self.search_response = youtube.search().list(q=QUERY, part="id,snippet,contentDetails,fileDetails,player,processingDetails,recordingDetails,statistics,status,suggestions,topicDetails", maxResults=MAX_RESULT,
                        #                                                                     order='date', pageToken=NEXT_PAGE_TOKEN ,publishedAfter=PUBLISHED_AFTER,publishedBefore=PUBLISHED_BEFORE).execute()

                        self.search_response = youtube.search().list(q=QUERY, part="id,snippet",
                                                                     maxResults=MAX_RESULT, pageToken=NEXT_PAGE_TOKEN, order='date').execute()
                        self.response = getData(self.search_response)

                        try:
                            NEXT_PAGE_TOKEN = NEXT_PAGE_TOKEN + \
                                self.search_response["nextPageToken"]
                        except:
                            pass

                        print("Requesting next page...")

                    else:
                        self.search_response = youtube.search().list(q=QUERY, part="id,snippet",
                                                                     maxResults=MAX_RESULT, order='date').execute()
                        try:
                            NEXT_PAGE_TOKEN = NEXT_PAGE_TOKEN + \
                                self.search_response["nextPageToken"]
                        except:
                            pass

                        self.response = getData(self.search_response)

                else:
                    print("Query Empty")

        except FileNotFoundError:
            print("File Not Found")


def getData(search_response):

    DATA = []
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":

            videoId = search_result["id"]["videoId"]

            channelId = search_result["snippet"]["channelId"]

            title = search_result["snippet"]["title"]

            channelTitle = search_result["snippet"]["channelTitle"]

            publishedAt = search_result["snippet"]["publishedAt"]

            thumbnails = search_result["snippet"]["thumbnails"]["high"]["url"]

            url = "https://www.youtube.com/watch?v="+videoId

            nextPageToken = search_response["nextPageToken"]

            row = {"videoId": videoId, "channelId": channelId, "title": title, "channelTitle": channelTitle,
                                       "publishedAt": publishedAt, "thumbnails": thumbnails, "url": url, 'nextPageToken': nextPageToken}
            DATA.append(row)
    return DATA
