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

        # tab1
        self.tab1.mainLay = QVBoxLayout()
        self.tab1.stat1 = QHBoxLayout()
        self.tab1.start1  = QPushButton("start")
        self.tab1.pause1 = QPushButton("pause")
        self.tab1.stat1.addWidget(self.tab1.start1)
        self.tab1.stat1.addWidget(self.tab1.pause1)

        self.tab1.mov1 = ImageViewer()
        self.tab1.each1 = QVBoxLayout()
        self.tab1.thread = QThread()
        self.tab1.thread.start()
        self.tab1.vid = ShowVideo()
        self.tab1.vid.moveToThread(self.tab1.thread)
        image_viewer1 = ImageViewer()
        self.tab1.vid.VideoSignal1.connect(image_viewer1.setImage)
        self.tab1.each1.addWidget(image_viewer1)
        self.tab1.each1.addLayout(self.tab1.stat1)
        
        self.tab1.start1.clicked.connect(self.tab1.vid.startVideo)
        self.tab1.mainLay.addLayout(self.tab1.each1)
        self.tab1.setLayout(self.tab1.mainLay)