try:
    import cPickle as pickle
except ModuleNotFoundError:
    import pickle


class Comments():
    with open('youtube.pkl', 'rb') as input:
        youtube = pickle.load(input)
        youtubeC=pickle.load(input)
        
        
    def __init__(self, channelId, videoId,youtube_get_obj):
        self.top_comment=self.get_top_commment(videoId,self.youtubeC)
    
    def get_top_commment(self, videoId,youtubeC):
        request = youtubeC.commentThreads().list(
            part="snippet,replies",
            order="relevance",
            videoId=videoId
        )
        response = request.execute()
        
        if response['items']:
            return response['items'][0]['snippet']['topLevelComment']['snippet']['textOriginal']
        else:
            return ""
    
    def get_newst_commment(self, videoId,youtube_get_obj):
        request = youtube_get_obj.commentThreads().list(
            part="snippet,replies",
            order="time",
            videoId=videoId
        )
        response = request.execute()
        
        if response['items']:
            return response['items'][0]['snippet']['topLevelComment']['snippet']['textOriginal']
        else:
            return ""
    