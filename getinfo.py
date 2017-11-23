#!/usr/bin/python

from __future__ import unicode_literals
import vlc
import sys 
import youtube_dl
import json
import urllib.request as urlb
class getinfo():
    def __init__(self,url):
        self.str=""
        self.url=url
        self.infos()
        self.vq=['2160p',
                 '1440p',
                 '1080p',
                 '720p',
                 '480p',
                 '360p',
                 '240p',
                 '144p']
        self.aq=['256',
                 '192',
                 '160',
                 '128',
                 '96',
                 '70',
                 '64',
                 '50',
                 '48',
                 '24']
    def Response(self,link):
        self.link=link
        response = urlb.Request(link)
        self.response=urlb.urlopen(response).readlines()
        return self.response

    def FormatInfo(self):
        if not self.response:
            self.Response(self.link)
        for a in self.response:
            if'var ytplayer' in a.decode():
                print(a)


    def search2(self,sformat,cv=True,ca=True):
        result={}
        for a in self.result['formats']:
            if sformat=='all':
                if sformat in a['format']:
                    result[a['format']]=a['url']
            elif cv==True and ca==True:
                if a['vcodec']!='none' and a['acodec']!='none':
                    if sformat in a['format']:
                        result[a['format']]=a['url']
            elif cv==False:
                if a['vcodec']=='none':
                        result['{} kbps'.format(a['abr'])]=a['url']
            elif ca==False:
                if a['acodec']=='none':
                    if sformat in a['format']:
                        result[a['format']]=a['url']

        return result
    def infos(self):
        with youtube_dl.YoutubeDL() as ydl:
            self.result=ydl.extract_info(self.url, download=False)
        return self.result
"""    def search(self,defq=self.defq[0],vq=self.vq,aq=self.aq,allin=False):
        if allin==False:
            if defq==self.defq[0]:
"""


yt=getinfo('fihQM_-9ueI')
yt.Response('https://www.youtube.com/watch?v=TPbs_Ztm16k')
yt.FormatInfo()



