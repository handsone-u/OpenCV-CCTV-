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
        
        
        self.tabs.addTab(self.tab3, "기록")

       

        self.tab3.layout = QVBoxLayout()
        self.tab3.btn1 = QPushButton('refresh')
        self.tab3.btn2 = QPushButton('clear')
        self.tab3.box = QHBoxLayout()
        self.tab3.logtable = QTableWidget(parent)
        df2 = pd.read_csv("log_file.csv")
        lst2 = []
        for j in range(len(df2.columns)):
            if j==1:
                continue
            lst2.append(str(df2.columns[j]))
        self.tab3.row = len(df2.index)
        self.tab3.col = len(df2.columns) 
        self.tab3.logtable.setRowCount(self.tab3.row)
        self.tab3.logtable.setColumnCount(self.tab3.col-1)
        self.tab3.logtable.setHorizontalHeaderLabels(lst2)

        for i in range(self.tab3.row):
            for j in range(self.tab3.col):
                if j == 1:
                    continue
                elif j >1:
                    self.tab3.logtable.setItem(i, j-1, QTableWidgetItem(str(df2.iloc[i,j])))
                else:
                    self.tab3.logtable.setItem(i, j, QTableWidgetItem(str(df2.iloc[i,j])))

        self.tab3.logtable.resizeColumnsToContents()
        self.tab2.datatable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tab3.box.addWidget(self.tab3.btn1)
        self.tab3.box.addWidget(self.tab3.btn2)
        self.tab3.layout.addLayout(self.tab3.box)
        self.tab3.layout.addWidget(self.tab3.logtable)
        self.tab3.setLayout(self.tab3.layout)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
