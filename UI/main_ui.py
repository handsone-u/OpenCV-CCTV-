import sys
import cv2
import pandas as pd
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import *

from sftp_upload import server_db
from add_person import addPerson
# global var here !
s = server_db()
ap = addPerson()
df = s.persondata_df

#print(df)
# ----------------!

class TabWIdget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)     

        self.table_row = 0;
        self.table_col = 0;
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.tabs.addTab(self.tab1, "영상")
        self.tabs.addTab(self.tab2, "탐색 대상")
        self.tabs.addTab(self.tab3, "기록")

        # tab1
        self.tab1.mainLay = QVBoxLayout()
        self.tab1.stat = QHBoxLayout()
        self.tab1.start = QPushButton("start")
        self.tab1.pause = QPushButton("pause")
        self.tab1.stat.addWidget(self.tab1.start)
        self.tab1.stat.addWidget(self.tab1.pause)

        self.tab1.mainLay.addLayout(self.tab1.stat)
        self.tab1.setLayout(self.tab1.mainLay)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.tab2.hbox_first = QHBoxLayout()
        self.tab2.btn_new = QPushButton('new')
        self.tab2.btn_ref = QPushButton('ref')
        # event not implemented yet
        self.tab2.btn_new.clicked.connect(self.get_Person)
        #
        
        self.tab2.hbox_first.addWidget(self.tab2.btn_new)
        self.tab2.hbox_first.addWidget(self.tab2.btn_ref)
        self.tab2.datatable = QTableWidget(parent)

        lst = []
        for j in range(len(df.columns)):
            lst.append(str(df.columns[j]))
        lst.append('삭제')
        self.table_row = len(df.index)
        self.table_col = len(lst)
        #print(self.table_row, self.table_col)
        self.tab2.datatable.setColumnCount(self.table_col)
        self.tab2.datatable.setRowCount(self.table_row)
        self.tab2.datatable.setHorizontalHeaderLabels(lst)
        for i in range(len(df.index)):
            pic = QPixmap('IMG_6648.JPG')
            piclabel = QLabel()
            piclabel.setPixmap(pic)
            sbtn = QPushButton('탐색')
            sbtn.setCheckable(True)
            sbtn.clicked.connect(self.search_state)
            if df.iloc[i,6] == True:
                sbtn.setChecked(True)
            dbtn = QPushButton('삭제')
            dbtn.clicked.connect(self.deleteClicked)
            dbtn.setCheckable(True)
            self.tab2.datatable.setCellWidget(i, 5, piclabel)
            self.tab2.datatable.setCellWidget(i, 7, dbtn)
            self.tab2.datatable.setCellWidget(i, 6, sbtn)
            for j in range(len(df.columns)-1):
                self.tab2.datatable.setItem(i, j, QTableWidgetItem(str(df.iloc[i,j])))

        self.tab2.datatable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tab2.layout = QVBoxLayout()
        self.tab2.layout.addLayout(self.tab2.hbox_first)
        self.tab2.layout.addWidget(self.tab2.datatable)
        self.tab2.setLayout(self.tab2.layout)


        self.tab3.layout = QVBoxLayout()
        self.tab3.btn1 = QPushButton('refresh')
        self.tab3.btn2 = QPushButton('clear')
        self.tab3.box = QHBoxLayout()
        self.tab3.logtable = QTableWidget(parent)
        df2 = pd.read_csv("./csvfile/log_file.csv")
        lst2 = []
        for j in range(len(df2.columns)):
            if j == 1:
                continue
            lst2.append(str(df2.columns[j]))
        self.tab3.row = len(df2.index)
        self.tab3.col = len(df2.columns)
        self.tab3.logtable.setRowCount(self.tab3.row)
        self.tab3.logtable.setColumnCount(self.tab3.col - 1)
        self.tab3.logtable.setHorizontalHeaderLabels(lst2)

        for i in range(self.tab3.row):
            for j in range(self.tab3.col):
                if j == 1:
                    continue
                elif j > 1:
                    self.tab3.logtable.setItem(i, j - 1, QTableWidgetItem(str(df2.iloc[i, j])))
                else:
                    self.tab3.logtable.setItem(i, j, QTableWidgetItem(str(df2.iloc[i, j])))

        self.tab3.logtable.resizeColumnsToContents()
        self.tab2.datatable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tab3.box.addWidget(self.tab3.btn1)
        self.tab3.box.addWidget(self.tab3.btn2)
        self.tab3.layout.addLayout(self.tab3.box)
        self.tab3.layout.addWidget(self.tab3.logtable)
        self.tab3.setLayout(self.tab3.layout)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


    def get_Person(self):
        self.tmp = Person_dialog(self.tab2.datatable)
        self.tmp.show()
        if self.tmp.exec_() == self.tmp.Accepted:
            self.addinTable()

    def addinTable(self):
        global s
        row = self.tab2.datatable.rowCount()
        print(row)
        self.tab2.datatable.insertRow(row)
        global df
        s.renewal_df()
        df = pd.read_csv("./csvfile/persondata.csv", index_col=0)
        pic = QPixmap('IMG_6648.JPG')
        piclabel = QLabel()
        piclabel.setPixmap(pic)
        sbtn = QPushButton('탐색')
        sbtn.setCheckable(True)
        sbtn.setChecked(True)
        sbtn.clicked.connect(self.search_state)
        dbtn = QPushButton('삭제')
        dbtn.clicked.connect(self.deleteClicked)
        dbtn.setCheckable(True)
        self.tab2.datatable.setCellWidget(row, 5, piclabel)
        self.tab2.datatable.setCellWidget(row, 7, dbtn)
        self.tab2.datatable.setCellWidget(row, 6, sbtn)
        for j in range(len(df.columns)-1):
                self.tab2.datatable.setItem(row, j, QTableWidgetItem(str(df.iloc[row,j])))
        

    @pyqtSlot()
    def deleteClicked(self):
        button = self.sender()
        if button:
            global df
            global s
            global ap
            row = self.tab2.datatable.indexAt(button.pos()).row()
            self.tab2.datatable.removeRow(row)
            df = df.drop(df.index[row])
            df = df.reset_index(drop=True)
            df.to_csv("./csvfile/persondata.csv", mode='w')
            s.upload_file('./csvfile/','csv')
            ap.delete_person_from_list(row)

    def search_state(self):
        button = self.sender()
        if button:
            global df
            row = self.tab2.datatable.indexAt(button.pos()).row()
            print(row)
            if button.isChecked():
                print("checked!")
                print(df.iloc[row,6])
                df.iloc[row,6] = True
                print(df.iloc[row,6])
            else:
                print("unchecked!")
                print(df.iloc[row,6])
                df.iloc[row,6] = False
                print(df.iloc[row,6])
            df.to_csv("./csvfile/persondata.csv", mode='w')
            s.upload_file('./csvfile/','csv')
            



class Log(QDialog):
    def __init__(self, parent):
        super(Log, self).__init__(parent)
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle('탐색 기록')
        self.resize(480,300)


class Person_dialog(QDialog):
    def __init__(self, parent):
        super(Person_dialog, self).__init__(parent)
        self.setup_UI()


    def openFile(self):
        self.fileName , _ = QFileDialog.getOpenFileName(self, "불러올 파일 선택.", "",
                                                  "All Files (*);;jpg (*.jpg);;png (*.png)")
        if self.fileName:
            print(self.fileName)
        # file 경로 전달

    def setup_UI(self):
        self.setWindowTitle('person_Dialog')
        self.resize(360, 300)

        self.label_name = QLabel("name : ")
        self.line_name = QLineEdit()
        self.line_name.setPlaceholderText('name')
        self.label_age = QLabel("age : ")
        self.line_age = QLineEdit()
        self.line_age.setPlaceholderText('age')
        self.label_gender = QLabel("gender : ")
        self.btn_genderm = QPushButton('male')
        self.btn_genderm.setCheckable(True)
        self.btn_genderm.toggle()
        self.btn_genderf = QPushButton('female')
        self.btn_genderf.setCheckable(True)
        self.genderlay = QHBoxLayout()
        self.genderlay.addWidget(self.btn_genderm)
        self.genderlay.addWidget(self.btn_genderf)
        self.label_race = QLabel("race : ")
        self.btn_racey = QPushButton("yellow")
        self.btn_racey.setCheckable(True)
        self.btn_racey.toggle()
        self.btn_racew = QPushButton("white")
        self.btn_racew.setCheckable(True)
        self.btn_raceb = QPushButton("black")
        self.btn_raceb.setCheckable(True)
        self.racelay = QHBoxLayout()
        self.racelay.addWidget(self.btn_racey)
        self.racelay.addWidget(self.btn_racew)
        self.racelay.addWidget(self.btn_raceb)
        self.label_height = QLabel("height : ")
        self.line_height = QLineEdit()
        self.line_height.setPlaceholderText('height')
        self.label_cloth = QLabel("cloth color : ")
        self.cloth_colorlay1 = QHBoxLayout()
        self.cloth_colorlay2 = QHBoxLayout()
        self.cloth_none = QPushButton('None')
        self.cloth_none.setCheckable(True)
        self.cloth_none.toggle()
        self.cloth_black = QPushButton('black')
        self.cloth_black.setCheckable(True)
        self.cloth_black.setStyleSheet("background-color : black")
        self.cloth_white = QPushButton('white')
        self.cloth_white.setCheckable(True)
        self.cloth_white.setStyleSheet("background-color : white")
        self.cloth_red = QPushButton('red')
        self.cloth_red.setCheckable(True)
        self.cloth_red.setStyleSheet("background-color : red")
        self.cloth_yellow = QPushButton('yellow')
        self.cloth_yellow.setCheckable(True)
        self.cloth_yellow.setStyleSheet("background-color : yellow")
        self.cloth_green = QPushButton('green')
        self.cloth_green.setCheckable(True)
        self.cloth_green.setStyleSheet("background-color : green")
        self.cloth_blue = QPushButton('blue')
        self.cloth_blue.setCheckable(True)
        self.cloth_blue.setStyleSheet("background-color : blue")
        self.cloth_purple = QPushButton('purple')
        self.cloth_purple.setCheckable(True)
        self.cloth_purple.setStyleSheet("background-color : purple")
        self.cloth_colorlay1.addWidget(self.cloth_none)
        self.cloth_colorlay1.addWidget(self.cloth_black)
        self.cloth_colorlay1.addWidget(self.cloth_white)
        self.cloth_colorlay1.addWidget(self.cloth_red)
        self.cloth_colorlay2.addWidget(self.cloth_yellow)
        self.cloth_colorlay2.addWidget(self.cloth_green)
        self.cloth_colorlay2.addWidget(self.cloth_blue)
        self.cloth_colorlay2.addWidget(self.cloth_purple)
        self.label_pic = QLabel("picture : ")
        self.btn_pic = QPushButton("open")

        layout = QGridLayout()

        layout.addWidget(self.label_name, 0, 0)
        layout.addWidget(self.line_name, 0, 1)
        layout.addWidget(self.label_age, 1, 0)
        layout.addWidget(self.line_age, 1, 1)
        layout.addWidget(self.label_gender, 2, 0)
        layout.addLayout(self.genderlay, 2, 1)
        layout.addWidget(self.label_height, 3, 0)
        layout.addWidget(self.line_height, 3, 1)
        layout.addWidget(self.label_race, 4, 0)
        layout.addLayout(self.racelay, 4, 1)
        layout.addWidget(self.label_cloth, 5, 0)
        layout.addLayout(self.cloth_colorlay1, 5, 1)
        layout.addLayout(self.cloth_colorlay2, 6, 1)
        layout.addWidget(self.label_pic, 7, 0)
        layout.addWidget(self.btn_pic, 7, 1)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(10, 440, 621, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.btn_pic.clicked.connect(self.openFile)
        self.buttonBox.accepted.connect(self.save)
        self.buttonBox.rejected.connect(self.reject)

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(layout)
        self.mainLayout.addWidget(self.buttonBox)
        self.setLayout(self.mainLayout)

    def save(self):
        global df
        global s
        global ap

        tname = self.line_name.text()
        tage = self.line_age.text()
        theight = self.line_height.text()
        tcloth = "none"
        try:
            tfile = self.fileName
        except:
            tfile = 0
        if self.btn_genderm.isChecked():
            tgen = 'm'
        else:
            tgen = 'f'
        if self.btn_racey.isChecked():
            trace = 'y'
        elif self.btn_racew.isChecked():
            trace = 'w'
        else:
            trace = 'b'
        # if self.cloth_none.isChecked():
        #     pass
        # elif self.cloth_black.isChecked():
        #     tcloth = "black"
        # elif self.cloth_white.isChecked():
        #     tcloth = "white"
        # elif self.cloth_red.isChecked():
        #     tcloth = "red"
        # elif self.cloth_yellow.isChecked():
        #     tcloth = "yellow"
        # elif self.cloth_green.isChecked():
        #     tcloth = "green"
        # elif self.cloth_blue.isChecked():
        #     tcloth = "blue"
        # else:
        #     tcloth = "purple"
        tcheck = True
        tmp = [tname, tage, tgen, theight, trace, tfile, tcheck]
        df2 = df.append(pd.Series(tmp, index=df.columns), ignore_index=True)
        df2.to_csv("./csvfile/persondata.csv", mode='w')
        s.upload_file('./csvfile/','csv')
        ap.add_person_to_list(tname, tfile)

        self.accept()

class ShowVideo(QObject):

    flag = 0

    camera = cv2.VideoCapture(0)

    ret, image = camera.read()
    height, width = image.shape[:2]

    VideoSignal1 = pyqtSignal(QImage)

    def __init__(self, parent=None):
        super(ShowVideo, self).__init__(parent)

    @pyqtSlot()
    def startVideo(self):
        global image

        # 줄이고 싶은 배율 입력
        sizechange = 1

        run_video = True
        while run_video:
            ret, image = self.camera.read()
            color_swapped_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            color_swapped_image = cv2.resize(color_swapped_image, None, fx=sizechange, fy=sizechange)

            qt_image1 = QImage(color_swapped_image.data,
                                    self.width*sizechange,
                                    self.height*sizechange,
                                    color_swapped_image.strides[0],
                                    QImage.Format_RGB888)
            self.VideoSignal1.emit(qt_image1)


            if self.flag:
                img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                img_canny = cv2.Canny(img_gray, 50, 100)

                img_canny = cv2.resize(img_canny, None, fx=sizechange, fy=sizechange)

                qt_image2 = QImage(img_canny.data,
                                         self.width*sizechange,
                                         self.height*sizechange,
                                         img_canny.strides[0],
                                         QImage.Format_Grayscale8)


            # loop = QEventLoop()
            # QTimer.singleShot(25, loop.quit) #25 ms
            # loop.exec_()


class ImageViewer(QWidget):
    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)
        self.image = QImage()
        self.setAttribute(Qt.WA_OpaquePaintEvent)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QImage()

    def initUI(self):
        self.setWindowTitle('Test')

    @pyqtSlot(QImage)
    def setImage(self, image):
        if image.isNull():
            print("Viewer Dropped frame!")

        self.image = image
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.update()

class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initui()
        global s
        self.map_path = ""
        self.cctv_path = ""

    def open_map(self):
        msg_box = QMessageBox(self)
        msg_box.question(self, "Choose the map img","Are you sure you want to choose the map img?")
        self.map_path, _ = QFileDialog.getOpenFileName(self, "불러올 파일 선택.", "",
                                                  "All Files (*);;jpg (*.jpg);;png (*.png)")
        if self.map_path:
            print(self.map_path)
        # file 경로 전달

    def open_cctv(self):
        msg_box = QMessageBox(self)
        msg_box.question(self, "Choose the cctv img","Are you sure you want to choose the cctv img?")
        self.cctv_path, _ = QFileDialog.getOpenFileName(self, "불러올 파일 선택.", "",
                                                  "All Files (*);;jpg (*.jpg);;png (*.png)")
        if self.cctv_path:
            print(self.cctv_path)


    def get_log(self):
        self.tmp = Log(self)
        self.tmp.show()

    def initui(self):
        menu_main = self.menuBar()

        self.tab_widget = TabWIdget(self)
        self.setCentralWidget(self.tab_widget)
        # ---menu named edit---
        menu_main_edit = menu_main.addMenu('편집')

        edit_map = QMenu('지도', self)
        edit_cam = QMenu('카메라', self)
        # edit_per = QAction('목적 대상', self)

        menu_main_edit.addMenu(edit_map)
        menu_main_edit.addMenu(edit_cam)
        # menu_main_edit.addAction(edit_per)

        map_img_load = QAction('map load', self)
        cctv_img_load = QAction('cctv load', self)
        cam_new = QAction('new', self)
        cam_del = QAction('delete', self)

        edit_map.addAction(map_img_load)
        edit_map.addAction(cctv_img_load)
        edit_cam.addAction(cam_new)
        edit_cam.addAction(cam_del)


        # ---menu named record---
        menu_main_rec = menu_main.addMenu('녹화')
        rec_edit = QAction('추가', self)
        rec_log = QAction('기록', self)

        menu_main_rec.addAction(rec_edit)
        menu_main_rec.addAction(rec_log)

        # -- sever load & save
        menu_main_server = menu_main.addMenu('서버')
        server_load = QAction('load', self)
        server_save = QAction('save', self)
        server_ref = QAction('refresh', self)

        menu_main_server.addAction(server_load)
        menu_main_server.addAction(server_save)
        menu_main_server.addAction(server_ref)

        # ---events---
        map_img_load.triggered.connect(self.open_map)
        cctv_img_load.triggered.connect(self.open_cctv)
        cam_new.triggered.connect(self.cctv_load)
        cam_del.triggered.connect(self.cctv_delete)
        # edit_per.triggered.connect(self.get_Person)
        rec_edit.triggered.connect(self.log_show)
        rec_log.triggered.connect(self.recod_log)


        self.setGeometry(100,100,1000,600)

        self.show()

    def cctv_load(self):
        if self.map_path == "":
            self.open_map()

        if self.map_path:
            mapmap = cv2.imread(self.map_path)

            cv2.namedWindow('map')  # 윈도우의 이름 설정
            cv2.setMouseCallback('map', self.on_mouse)  # 마우스 이벤트 처리하는 콜백 함수
            cv2.imshow('map', mapmap)
            cv2.waitKey(0)  # 키입력전까지 imshow를 유지시켜줌
            cv2.destroyAllWindows()

    def on_mouse(self, event, x, y, flags, param):  # setMouseCallback 에 인자로 들어가는 on_mouse함수
        if event == cv2.EVENT_LBUTTONDOWN:  # 왼쪽버튼 눌렀을 시에
            # reply = QMessageBox.question(self, 'Message', '저장하시겠습니까?', QMessageBox.Yes | QMessageBox.No)
            text, ok = QInputDialog.getText(self, 'Saving', 'CCTV IP Address : ')
            if ok:
                s.renewal_df()
                print(s.cctv_df)
                row = [x, y, text]
                print(row)
                s.cctv_df.loc[len(s.cctv_df) + 1] = row
                print(s.cctv_df)
                s.cctv_df.to_csv(s.local_path + 'cctv_file.csv', index=False,
                                 columns=['X1 axis', 'Y1 axis', 'CCTV IP Address'])
                s.upload_file(s.local_path, 'csv')

    def cctv_delete(self):
        # 그림 불러오기
        if self.map_path == "":
            self.open_map()
        if self.cctv_path == "":
            self.open_cctv()

        if self.map_path and self.cctv_path:
            label = QLabel()
            pixmap = QPixmap(self.map_path)
            label.setPixmap(pixmap)
            label.resize(pixmap.width(), pixmap.height())
            self.label = label

            # 좌표 설정
            s.renewal_df()
            self.btnList = []
            for i in range(len(s.cctv_df)):
                x1, y1 = s.cctv_df.iloc[i, 0:2]
                print(s.cctv_df.iloc[i, 0:2])
                button = QPushButton(self.label)
                button.clicked.connect(lambda state, x=i: self.delete(x))
                self.btnList.append(button)
                self.btnList[i].setIcon(QIcon(self.cctv_path))
                self.btnList[i].setIconSize(QSize(20, 20))
                self.btnList[i].resize(QSize(20, 20))
                self.btnList[i].move(x1, y1)
                # self.btnList[i].show()

            self.label.show()

    def delete(self, num):
        reply = QMessageBox.question(self.label, 'Message', '삭제하시겠습니까?', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.btnList[num].deleteLater()
            s.cctv_df = s.cctv_df.drop(s.cctv_df.index[num])
            print("삭제된 dataframe형태")
            print(s.cctv_df)
            s.cctv_df.to_csv(s.local_path + 'cctv_file.csv', index=False,
                             columns=['X1 axis', 'Y1 axis', 'CCTV IP Address'])
            s.upload_file(s.local_path, 'csv')
            self.cctv_delete()

    def log_show(self):
        #temp = s.logging("df674251-dede-4204-9e31-5e9d31a56cc6", "255.255.255.255")
        #temp = dataframe
        if len(temp) != 0:
            msg_box = QMessageBox.question(self, "실종자 탐색됨!", "실종자 정보를 보시겠습니까?", QMessageBox.Yes | QMessageBox.No,
                                           QMessageBox.No)
            if msg_box == QMessageBox.Yes:
                self.getInfo(0, temp.loc[:, "name"])

    def recod_log(self):    # logging함수에서 log가 저장 될 때마다,
                            # 팝업을 띄워주는데,(중복문제는 추후 해결예정) 팝업 yes를 할 시에,
                            # logging함수에서 recod_log를 불러오고 파라미터로
                            # temp dataframe을 불러와서
                            # recod_log에서 활용할 예정
        if self.map_path == "":
            self.open_map()
        if self.cctv_path == "":
            self.open_cctv()

        label2 = QLabel()
        pixmap = QPixmap(self.map_path)
        label2.setPixmap(pixmap)
        label2.resize(pixmap.width(), pixmap.height())
        self.label2 = label2

        self.btnList2 = []
        s.renewal_df()
        for i in range(len(s.log_df)):
            for j in range(len(s.cctv_df)):
                print('j :', j, '주소 :', s.cctv_df.iloc[j, 2])
                print('i :', i, '주소 :', s.log_df.iloc[i, 4])
                if s.cctv_df.iloc[j, 2] == s.log_df.iloc[i, 4]:
                    print('same')
                    x1, y1 = s.cctv_df.iloc[j, 0:2]
                    button = QPushButton(self.label2)
                    button.clicked.connect(lambda state, x=i: self.getInfo(x, s.log_df.iloc[i, 0]))
                    self.btnList2.append(button)
                    self.btnList2[i].setIcon(QIcon(self.cctv_path))
                    self.btnList2[i].setIconSize(QSize(40, 40))
                    self.btnList2[i].resize(QSize(40, 40))
                    self.btnList2[i].move(x1, y1)

        self.label2.show()


    def getInfo(self, num, name):
        print('num :', num, 'name :', name)

        # 전체 화면 QLabel 생성
        label4 = QLabel()
        label4.setGeometry(420, 120, 700, 500)

        # 동영상 재생할 QMediaPlayer 생성
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # QMediaPlayer를 표혀해줄 QVideoWidget 생성
        videowidget = QVideoWidget()

        openBtn = QPushButton('Open Video')
        openBtn.clicked.connect(self.open_file)

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

        self.label3.setText("name : {0}\ntime : 2020-08-08/13:02am".format(name))
        self.label3.setFont(QFont("궁서", 15))

        hboxLayout = QHBoxLayout()

        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.slider)

        vboxLayout = QVBoxLayout()

        vboxLayout.addWidget(self.label3)
        vboxLayout.addWidget(videowidget)
        vboxLayout.addWidget(openBtn)
        vboxLayout.addLayout(hboxLayout)

        self.label4 = label4
        self.label4.setLayout(vboxLayout)

        # videowidget에 videooutput을 set준다.
        self.mediaPlayer.setVideoOutput(videowidget)
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)
        self.mediaPlayer.error.connect(self.handle_errors)

        self.label4.show()

    def open_file(self):  # 동영상 open
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video", './')

        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)

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



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_obj = MainUI()
    sys.exit(app.exec_())
