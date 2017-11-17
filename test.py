#!/usr/bin/python

from __future__ import unicode_literals
import vlc
import sys 
import youtube_dl
import json

class yb:
    def __init__(self):
        self.instance = vlc.Instance()
    def play(self, movie):
        media = self.instance.media_new(movie)
        media_list = self.instance.media_list_new([movie]) 
        self.player = self.instance.media_player_new()
        self.player.set_media(media)
        list_player =  self.instance.media_list_player_new()
        list_player.set_media_player(self.player)
        list_player.set_media_list(media_list) 
        self.player.play()

yb=yb()

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')
    elif d['status'] == 'downloading':
        pass
ydl_opts = {
    'progress_hooks': [my_hook],
    'download_archive':'test.tmp'
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    for a in ydl.extract_info('https://www.youtube.com/watch?v=fihQM_-9ueI',
                         download=False)['formats']:
        if a['format_note'] == "DASH audio":
            print('audio:',a['url'])
        if a['format_note'] =='1080p':
            print('video:',a['url'])
#    print(json.dumps(
#        ydl.extract_info('https://www.youtube.com/watch?v=BaW_jenozKc',
#                    download=False)['formats'],
#                     sort_keys=True, 
#                     indent=4)
#    )
#    input("Press any key to stop play")
