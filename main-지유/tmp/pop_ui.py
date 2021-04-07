import sys
import pandas as pd
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import *
import datetime
import time

from sftp_upload import server_db
from add_person import addPerson

# global var here !
s = server_db()
ap = addPerson()

class Thread1(QMainWindow):
    def __init__(self):
        super().__init__()

        self.hi()

        self.timer = QTimer(self)
        self.timer.start(10000)
        self.timer.timeout.connect(self.hi)


        self.map_path = ""
        self.cctv_path = ""


    def closeEvent(self, QCloseEvent):
        QCloseEvent.ignore()

    def hi(self):
        df = self.visualized_log()
        if df.empty:
            pass

        else:
            self.timer.stop()
            self.getInfo(df)
            self.recod_log(df.loc['CCTV IP Address'])
            '''loop = QEventLoop()
            QTimer.singleShot(10000, loop.quit)
            loop.exec_()'''

    def visualized_log(self):

        global s

        s.renewal_df()
        # s.download_file('./mp4file/', 'mp4')

        Interval = datetime.timedelta(minutes=3)  # 인터벌

        visualized_df = pd.read_csv('./csvfile/visualized_log.csv')
        # df1 = pd.read_csv('./csvfile/log_file.csv')
        # df1 = df1.tail(100)
        df1 = s.log_df.tail(100)

        for j in range(len(visualized_df)):
            tmp = df1[df1['face_id'] == visualized_df.loc[j, 'face_id']]
            tmp = tmp.reset_index(drop=True)
            print('tmp : ', tmp)
            for i in range(len(tmp)):
                visual_time = datetime.datetime.strptime(visualized_df.loc[j, 'Time'], '%Y-%m-%d %H-%M-%S')
                print(tmp.loc[i, 'Time'])
                tmp_time = datetime.datetime.strptime(tmp.loc[i, 'Time'], '%Y-%m-%d %H-%M-%S')
                dif = tmp_time - visual_time
                if Interval < dif:
                    visualized_df.loc[j, 'Time'] = tmp.loc[i, 'Time']
                    print(visualized_df)
                    print('tmp전체 :', tmp.loc[i, :])
                    visualized_df.to_csv('./csvfile/visualized_log.csv', mode='w', index=False)
                    s.upload_file('./csvfile/', 'csv')

                    return tmp.loc[i, :]
                else:
                    print('아쉽네요')
                    tmp = pd.DataFrame()
                    return tmp


    def getInfo(self, df):
        global s
        s.download_file('./mp4file/','mp4')
        # 전체 화면 QLabel 생성
        print('name :', df)
        print('reco_path :', df['reco_path'])
        # 전체 화면 QLabel 생성

        self.setGeometry(420, 120, 700, 500)

        restart_btn = QPushButton('restart')
        restart_btn.clicked.connect(self.restart_pop)

        # 동영상 재생할 QMediaPlayer 생성
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # QMediaPlayer를 표혀해줄 QVideoWidget 생성
        videowidget = QVideoWidget()

        openBtn = QPushButton('Open Video')
        openBtn.clicked.connect(lambda: self.open_file(df['reco_path']))

        # Play 버튼 생성
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        # Silder 생성.. 아직 클릭은 불가..
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)

        # 다른 text정보가 들어갈 QLabel 생성
        self.label3 = QLabel()
        self.label3.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # self.label3.setText("name : \ntime : \n".format(name))
        self.label3.setText("name : {0}\ntime : {1}\n".format(df['name'], df['Time']))
        self.label3.setFont(QFont("궁서", 15))

        self.hboxLayout = QHBoxLayout()

        self.hboxLayout.addWidget(self.playBtn)
        self.hboxLayout.addWidget(self.slider)

        self.vboxLayout = QVBoxLayout()

        self.vboxLayout.addWidget(restart_btn)
        self.vboxLayout.addWidget(self.label3)
        self.vboxLayout.addWidget(videowidget)
        self.vboxLayout.addWidget(openBtn)
        self.vboxLayout.addLayout(self.hboxLayout)


        # videowidget에 videooutput을 set준다.
        self.mediaPlayer.setVideoOutput(videowidget)
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)
        self.mediaPlayer.error.connect(self.handle_errors)


        centralWidget = QWidget()
        centralWidget.setLayout(self.vboxLayout)
        self.setCentralWidget(centralWidget)

        self.show()

        print('show완료')

    def open_file(self, reco_path):  # 동영상 open
        if reco_path != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(reco_path)))
            self.playBtn.setEnabled(True)
        elif reco_path == '':
            filename, _ = QFileDialog.getOpenFileName(self, "Open Video", './')

    def play_video(self):  # 동영상 play
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

        else:
            self.mediaPlayer.play()

    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))

        else:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())

    def restart_pop(self):
        self.timer.start(10000)

    def recod_log(self, ip_address):
        if self.map_path == "":
            self.open_map()
        if self.cctv_path == "":
            self.open_cctv()
        global s
        if self.map_path and self.cctv_path:
            label2 = QLabel()
            pixmap = QPixmap(self.map_path)
            label2.setPixmap(pixmap)
            label2.resize(pixmap.width(), pixmap.height())
            self.label2 = label2

            self.btnList2 = []
            s.renewal_df()

            for j in range(len(s.cctv_df)):
                print('j :', j, '주소 :', s.cctv_df.iloc[j, 2])
                if s.cctv_df.iloc[j, 2] == ip_address:
                    print('same')
                    x1, y1 = s.cctv_df.iloc[j, 0:2]
                    print('x1 :', x1, ' ,y1 :', y1)
                    button = QPushButton(self.label2)
                    self.btnList2.append(button)
                    print(self.cctv_path)
                    self.btnList2[j].setIcon(QIcon(self.cctv_path))
                    self.btnList2[j].setIconSize(QSize(40, 40))
                    self.btnList2[j].resize(QSize(40, 40))
                    self.btnList2[j].move(x1, y1)

            self.label2.show()

    def open_map(self):
        msg_box = QMessageBox(self)
        msg_box.question(self, "Choose the map img", "Are you sure you want to choose the map img?")
        self.map_path, _ = QFileDialog.getOpenFileName(self, "불러올 파일 선택.", "",
                                                       "All Files (*);;jpg (*.jpg);;png (*.png)")
        if self.map_path:
            print(self.map_path)
        # file 경로 전달

    def open_cctv(self):
        msg_box = QMessageBox(self)
        msg_box.question(self, "Choose the cctv img", "Are you sure you want to choose the cctv img?")
        self.cctv_path, _ = QFileDialog.getOpenFileName(self, "불러올 파일 선택.", "",
                                                        "All Files (*);;jpg (*.jpg);;png (*.png)")
        if self.cctv_path:
            print(self.cctv_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tr = Thread1()
    sys.exit(app.exec_())