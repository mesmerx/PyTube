#!/usr/bin/python3

import vlc
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

class yb:
    def __init__(self):
        self.key = "AIzaSyDHdsYtk_RsyDjsu7vuTANB2KCRsZKdEJE"
        self.name = "youtube"
        self.version = "v3"
        self.instance = vlc.Instance()
        
    def ybsearch(self,search,maxs):
        youtube = build(
            self.name, 
            self.version, 
            developerKey=self.key)
        search_response = youtube.search().list(
            q=search,
            part="id,snippet",
            maxResults=maxs
        ).execute()
        self.videos = []
        self.channels = []
        self.playlists = []
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                self.videos.append("%s (%s)" % (
                    search_result["snippet"]["title"],
                    search_result["id"]["videoId"]))
            elif search_result["id"]["kind"] == "youtube#channel":
                self.channels.append("%s (%s)" % (
                    search_result["snippet"]["title"],
                    search_result["id"]["channelId"]))
            elif search_result["id"]["kind"] == "youtube#playlist":
                self.playlists.append("%s (%s)" % (
                    search_result["snippet"]["title"],
                    search_result["id"]["playlistId"]))

    def ybprint(self,what):
        if what == "video":
            print("Videos:")
            for name in self.videos:
                  print(name)
        elif what == "channel":
            print("Channel:")
            for name in self.channels:
                  print(name)
        elif what == "playlist":
            print("Playlists:")
            for name in self.playlists:
                print(name)
    def play(self, movie):
        media = self.instance.media_new(movie)
        media_list = self.instance.media_list_new([movie]) 
        self.player = self.instance.media_player_new()
        self.player.set_media(media)
        list_player =  self.instance.media_list_player_new()
        list_player.set_media_player(self.player)
        list_player.set_media_list(media_list)
        self.player.play()
        input("Press any key to stop play")

if __name__ == "__main__":
    argparser.add_argument("--q", help="Search term", default="Google")
    argparser.add_argument("--max-results", help="Max results", default=25)
    args = argparser.parse_args()
    yut=yb()
    yut.ybsearch(args.q,args.max_results)
    yut.ybprint("video")
    yut.ybsearch("hello",args.max_results)
    yut.ybprint("video")
    yut.play('https://www.youtube.com/watch?v=fihQM_-9ueI')
