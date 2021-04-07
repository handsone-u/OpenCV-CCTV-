class ShowVideo(QObject):
    camera = cv2.VideoCapture(0)

    ret, image = camera.read()
    height, width = image.shape[:2]

    VideoSignal1 = pyqtSignal(QImage)
    VideoSignal2 = pyqtSignal(QImage)

    def __init__(self, parent=None):
        super(ShowVideo, self).__init__(parent)

    @pyqtSlot()
    def startVideo(self):
        global image

        # 줄이고 싶은 배율 입력
        sizechange = 0.5

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

            color_son = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            color_son = cv2.resize(color_son, None, fx=sizechange, fy=sizechange)
            
            qt_image2 = QImage(color_son.data,
                                    self.width*sizechange,
                                    self.height*sizechange,
                                    color_son.strides[0],
                                    QImage.Format_RGB888)
            self.VideoSignal2.emit(qt_image2)                        

            loop = QEventLoop()
            QTimer.singleShot(25, loop.quit) #25 ms
            loop.exec_()


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