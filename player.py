import sys
import os.path
import vlc
from PyQt4 import QtGui, QtCore

url='https://r1---sn-oxunxg8pjvn-bpbz7.googlevideo.com/videoplayback?key=yt6&mn=sn-oxunxg8pjvn-bpbz7&mm=31&sparams=aitags%2Cclen%2Cdur%2Cei%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Ckeepalive%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Crequiressl%2Csource%2Cexpire&pl=22&mv=m&mt=1511050842&ms=au&ei=E88QWrG7PMSWwwTcwYTAAQ&signature=6E6F7EC8DCD775901392C52AE4A8EC7C9E05FF16.4AD49216FBD83866CF1FBECA15309CEB65F0063D&clen=1445171528&ip=189.123.8.217&keepalive=yes&lmt=1510151627800863&itag=248&requiressl=yes&id=o-AP2CklGceieDo4bVRt4W8KnejJ3RilbBHKVt6UmTpCmE&source=youtube&dur=4478.500&mime=video%2Fwebm&aitags=133%2C134%2C135%2C136%2C137%2C160%2C242%2C243%2C244%2C247%2C248%2C278%2C298%2C299%2C302%2C303&initcwndbps=603750&ipbits=0&expire=1511072628&gir=yes&ratebypass=yes'
urlv='https://r1---sn-oxunxg8pjvn-bpbz7.googlevideo.com/videoplayback?dur=4478.501&itag=251&pl=22&keepalive=yes&source=youtube&expire=1511072372&mime=audio%2Fwebm&signature=03D1004EFADF2C828DC599AF15B6B4DD4C1FB181.73F0729D2C1EA381674EF09F7B8F59360E879995&ipbits=0&clen=68389315&initcwndbps=581250&ip=189.123.8.217&key=yt6&ms=au&mt=1511050675&mv=m&id=o-AE19OiZgM5b4BlneLG1szrCwOZ6MjLXUMAFuojD6lGEz&gir=yes&mn=sn-oxunxg8pjvn-bpbz7&lmt=1510151293556017&ei=FM4QWrHrJ4WKwwSCkJKIBw&sparams=clen%2Cdur%2Cei%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Ckeepalive%2Clmt%2Cmime%2Cmm%2Cmn%2Cms%2Cmv%2Cpl%2Crequiressl%2Csource%2Cexpire&requiressl=yes&mm=31&rateby'
position2=0
class Player(QtGui.QMainWindow):
    """A simple Media Player using VLC and Qt
    """
    def __init__(self, master=None):
        QtGui.QMainWindow.__init__(self, master)
        self.setWindowTitle("Media Player")

        # creating a basic vlc instance
        self.instance = vlc.Instance("--no-xlib")
        # creating an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()
        self.mediaplayer2 = self.instance.media_player_new()
        self.events = self.mediaplayer.event_manager()

        self.createUI()
        self.isPaused = False

    def createUI(self):
        """Set up the user interface, signals & slots
        """
        self.widget = QtGui.QWidget(self)
        self.setCentralWidget(self.widget)

        # In this widget, the video will be drawn
        if sys.platform == "darwin": # for MacOS
            self.videoframe = QtGui.QMacCocoaViewContainer(0)
        else:
            self.videoframe = QtGui.QFrame()
        self.palette = self.videoframe.palette()
        self.palette.setColor (QtGui.QPalette.Window,
                               QtGui.QColor(0,0,0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)

        self.positionslider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.positionslider.setToolTip("Position")
        self.positionslider.setMaximum(1000)
        self.connect(self.positionslider,
                     QtCore.SIGNAL("sliderMoved(int)"), self.setPosition)

        self.hbuttonbox = QtGui.QHBoxLayout()
        self.playbutton = QtGui.QPushButton("Play")
        self.hbuttonbox.addWidget(self.playbutton)
        self.connect(self.playbutton, QtCore.SIGNAL("clicked()"),
                     self.PlayPause)

        self.stopbutton = QtGui.QPushButton("Stop")
        self.hbuttonbox.addWidget(self.stopbutton)
        self.connect(self.stopbutton, QtCore.SIGNAL("clicked()"),
                     self.Stop)

        self.hbuttonbox.addStretch(1)
        self.volumeslider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.volumeslider.setMaximum(100)
        self.volumeslider.setValue(self.mediaplayer.audio_get_volume())
        self.volumeslider.setToolTip("Volume")
        self.hbuttonbox.addWidget(self.volumeslider)
        self.connect(self.volumeslider,
                     QtCore.SIGNAL("valueChanged(int)"),
                     self.setVolume)

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.addWidget(self.videoframe)
        self.vboxlayout.addWidget(self.positionslider)
        self.vboxlayout.addLayout(self.hbuttonbox)

        self.widget.setLayout(self.vboxlayout)

        open = QtGui.QAction("&Open", self)
        self.connect(open, QtCore.SIGNAL("triggered()"), self.OpenFile)
        exit = QtGui.QAction("&Exit", self)
        self.connect(exit, QtCore.SIGNAL("triggered()"), sys.exit)
        menubar = self.menuBar()
        filemenu = menubar.addMenu("&File")
        filemenu.addAction(open)
        filemenu.addSeparator()
        filemenu.addAction(exit)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(200)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"),
                     self.updateUI)

    def PlayPause(self):
        """Toggle play/pause status
        """
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.playbutton.setText("Play")
            self.isPaused = True
        else:
            if self.mediaplayer.play() == -1:
                self.OpenFile()
                return
            self.mediaplayer.play()
            self.playbutton.setText("Pause")
            self.timer.start()
            self.isPaused = False

    def Stop(self):
        """Stop player
        """
        self.mediaplayer.stop()
        self.playbutton.setText("Play")

    def open2(self,status):
        self.mediaplayer2.play()
    def OpenFile(self, filename=None,filename2=None):
        """Open a media file in a MediaPlayer
        """
        if filename is None:
            filename = QtGui.QFileDialog.getOpenFileName(self, "Open File", os.path.expanduser('~'))
        if not filename:
            return

        # create the media
        self.media = self.instance.media_new(filename)
        self.media2 = self.instance.media_new(filename2)
        # put the media in the media player
        self.mediaplayer.set_media(self.media)
        self.mediaplayer2.set_media(self.media2)

        self.events.event_attach(vlc.EventType.MediaPlayerPlaying, self.open2)

        # parse the metadata of the file
        self.media.parse()
        # set the title of the track as window title
        self.setWindowTitle(self.media.get_meta(0))

        # the media player has to be 'connected' to the QFrame
        # (otherwise a video would be displayed in it's own window)
        ## this is platform specific!
        # you have to give the id of the QFrame (or similar object) to
        # vlc, different platforms have different functions for this
        if sys.platform.startswith('linux'): # for Linux using the X Server
        
            self.mediaplayer.set_xwindow(self.videoframe.winId())
            self.mediaplayer2.set_xwindow(self.videoframe.winId())
        elif sys.platform == "win32": # for Windows
            self.mediaplayer.set_hwnd(self.videoframe.winId())
            self.mediaplayer2.set_hwnd(self.videoframe.winId())
        elif sys.platform == "darwin": # for MacOS
            self.mediaplayer.set_nsobject(self.videoframe.winId())
            self.mediaplayer2.set_nsobject(self.videoframe.winId())
        self.mediaplayer.play()
    def setVolume(self, Volume):
        """Set the volume
        """
        self.mediaplayer.audio_set_volume(Volume)

    def change2(self,status):
        position2=self.mediaplayer.get_position()
        self.mediaplayer2.set_position(position2)

        self.events.event_detach(vlc.EventType.MediaPlayerPositionChanged)
    def setPosition(self, position):
        """Set the position
        """
        self.events.event_attach(vlc.EventType.MediaPlayerPositionChanged,self.change2)
        # setting the position to where the slider was dragged
        self.mediaplayer.set_position(position / 1000.0)

        # the vlc MediaPlayer needs a float value between 0 and 1, Qt
        # uses integer variables, so you need a factor; the higher the
        # factor, the more precise are the results
        # (1000 should be enough)

    def updateUI(self):
        """updates the user interface"""
        # setting the slider to the desired position
        self.positionslider.setValue(self.mediaplayer.get_position() * 1000)

        if not self.mediaplayer.is_playing():
            # no need to call this function if nothing is played
            self.timer.stop()
            if not self.isPaused:
                # after the video finished, the play button stills shows
                # "Pause", not the desired behavior of a media player
                # this will fix it
                self.Stop()
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    player = Player()
    player.show()
    player.resize(640, 480)
    player.OpenFile(urlv,url)
    sys.exit(app.exec_())
   
