#!/usr/bin/python

from __future__ import unicode_literals
import vlc
import sys 
import youtube_dl
import json

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
        self.defq=['bestall',
                   'midall',
                   'lowall',
                   'bestvidmidaud',
                   'bestvidlowaudi',
                   'bestaudmidvid',
                   'bestaudlowvid',
                   'midvidlowaud'
                   'midauidlowvid']

    def search2(self,sformat,ca=True,cv=True):
        for a in self.result['formats']:
            if cv==True and ca==True:
                if 'DASH' not in a['format'] and a['acodec']!='none':
                    print('yes')
                    if sformat in a['format']:
                        print(a)
    def infos(self):
        with youtube_dl.YoutubeDL() as ydl:
            self.result=ydl.extract_info(self.url, download=False)
        return self.result
"""    def search(self,defq=self.defq[0],vq=self.vq,aq=self.aq,allin=False):
        if allin==False:
            if defq==self.defq[0]:
"""


yt=getinfo('fihQM_-9ueI')
yt.search2('1080')



