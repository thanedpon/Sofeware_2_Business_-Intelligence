import hashlib
import sqlite3
import sys
from PyQt5 import QtCore, QtWidgets, Qt
from PyQt5.QtWidgets import QFileDialog
import pandas as pd
from define_cat import data
from plotcanvas import PlotCanvas
from listwid import TableWidgetDragRows
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.text import Text
import numpy as np

class Ui_MainWindow(QtWidgets.QMainWindow,data):
    def __init__(self,parent=None):
        super(Ui_MainWindow,self).__init__(parent=parent)
        self.setupUi(self)
# Gui
    def setupUi(self, graph):
        graph.setObjectName("graph")
        graph.resize(985, 693)
        self.centralwidget = QtWidgets.QWidget(graph)
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.win = PlotCanvas(self.centralwidget)
        self.gridLayout.addWidget(self.win, 3, 0, 4, 3)
        self.gridLayout.addWidget(self.win.scroll, 6,0,6,3)
        self.gridLayout.addWidget(self.win.scroll2, 3,0,4,3)
        self.gui_winlist()
        self.gui_filter()
        self.gui_graphtree()
        self.gui_tab(graph)
        self.gui_slotsig(graph)

    def gui_winlist(self):
        self.win.mpl_connect('pick_event', self.onpick1)
        self.listcol = QtWidgets.QLineEdit(self.centralwidget)
        self.gridLayout.addWidget(self.listcol, 0, 1, 1, 2)
        self.listrows = QtWidgets.QLineEdit(self.centralwidget)
        self.gridLayout.addWidget(self.listrows, 1, 1, 1, 2)

    def gui_filter(self):
        self.hafe = QtWidgets.QHBoxLayout(self.centralwidget)
        self.filterlist2 = QtWidgets.QLineEdit(self.centralwidget)
        self.hafe.addWidget(self.filterlist2)
        self.gridLayout.addItem(self.hafe, 2, 1, 1, 2)
        self.tag_list = QtWidgets.QHBoxLayout(self.centralwidget)
        self.gridLayout.addItem(self.tag_list,0,3,6,3)
        self.tree_filter = QtWidgets.QTreeWidget(self.centralwidget)
        self.tree_filter.setHeaderLabel('FILTER')
        self.tree_filter.setFixedSize(300, 900)
        self.tag_list.addWidget(self.tree_filter)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.tag_list.addItem(self.verticalLayout)

    def gui_graphtree(self):
        self.getgraph_b()
        self.verticalLayout2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.addItem(self.verticalLayout2)
        self.getlist()
        self.treestyle()

    def gui_tab(self,graph):
        graph.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(graph)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 985, 31))
        self.menuFile = QtWidgets.QMenu(self.menubar)
        graph.setMenuBar(self.menubar)
        self.actionOpen = QtWidgets.QAction(graph)
        self.menuFile.addAction(self.actionOpen)
        self.menubar.addAction(self.menuFile.menuAction())
        self.actionOpen.triggered.connect(self.file_open)
        saveFile = QtWidgets.QAction("&Save File", self)
        saveFile.triggered.connect(self.file_save)
        self.menuFile.addAction(saveFile)
        self.retranslateUi(graph)
        self.creatdateselect()

    def gui_slotsig(self,graph):
        self.listrows.textChanged.connect(self.treestyle)
        self.listcol.textChanged.connect(self.treestyle)
        self.tree_filter.clicked.connect(self.filter)
        self.comboBox3.setVisible(False)
        QtCore.QMetaObject.connectSlotsByName(graph)



    def file_save(self):
        name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File',"", "xlsx(*.xlsx);;csv(*.csv)")
        file = open(name,'w')
        text = self.textEdit.toPlainText()
        file.write(text)
        file.close()

#edit try to closethen open
    def file_open(self):
        self.deleat_to_repeat(self.cat)
        self.deleat_to_repeat(self.valueslist)
        self.deleat_to_repeat(self.datelist)
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName,_ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()","","xlsx(*.xlsx);;csv(*.csv)",options=options)
        self.oldset = set()
        hasher = hashlib.md5()
        f = open(self.fileName,'rb')
        for chunk in iter (lambda :f.read(4096),b""):
            hasher.update(chunk)
        self.read = hasher.hexdigest()
        try:
            self.check_sum(self.read)
            self.getitemlist()
            self.dataset = pd.read_excel(self.fileName)
        except:
            self.check_non(self.read)
            self.getitemlist()
            self.dataset = pd.read_excel(self.fileName)
#edit

    def varforfilter(self):
        self.x = self.listcol.text()
        self.y = self.listrows.text()
        self.listx = self.x.split(',')
        self.listy = self.y.split(',')
        self.dimentionplotlist = []
        self.valuesplotlist = []
        self.dateplotlist = []
        self.in_key_di = []
        self.in_key_val = []
        self.in_key_date = []
        self.genlist(self.listx)
        self.genlist(self.listy)

    def condition_plot(self):
        self.listfil = {}
        for i in self.in_key_di:
            for a in self.filterlist:
                if self.key[i] == a:
                    self.listfil[i] = self.filterlist[a]

        if len(self.in_key_date) == 1 and len(self.in_key_di) == 0 and len(self.in_key_val) != 0:
            self.condition(self.in_key_date)
        elif len(self.in_key_date) == 1 and len(self.in_key_di) >= 1:
            self.condition(self.in_key_di)
        else:
            self.getdataform = self.getinfo(self.in_key_di,self.in_key_val,self.dataset,self.listfil)
            print(self.getdataform)
            self.tellaxisplot(self.dimentionplotlist)
            self.comboBox3.setVisible(False)


    def condition(self,diordate):
        self.getdataform = self.getinfo(diordate,self.in_key_val,self.dataset,self.listfil)
        self.getdataform = self.fordate(self.getdataform,self.listfil)
        self.tellaxisplot(self.dateplotlist)
        self.comboBox3.setVisible(True)
        self.comboBox3.setCurrentIndex(0)

    def state_con(self):
        #for plot
        if 'y' not in self.findaxis:
            return self.win.plotbar(self.getdataform,self.listx,self.listy)
        if 'x' not in self.findaxis:
            return self.win.plotbary(self.getdataform,self.listy,self.listx)
        if 'x' in self.findaxis and 'y' in self.findaxis:
            print('multitable')
            return self.warning()
        if len(self.dimentionplotlist) == 0 or len(self.valuesplotlist) == 0:
            return  self.warning()
        else:
            return self.warning()

    def find_catagories(self):
        for i in range(len(self.key)):
            if self.key[i] in self.dimentionplotlist:
                self.in_key_di.append(i)
            elif self.key[i] in self.valuesplotlist:
                self.in_key_val.append(i)
            elif self.key[i] in self.dateplotlist:
                self.in_key_date.append(i)


    def filter(self):
        self.filterlist = self.find_checked()
        forloop = self.find_checked()

        for i in forloop:
            if forloop[i] == [] and i in self.x:
                self.connection(self.x,self.listcol,i)
            elif forloop[i] == [] and i in self.y:
                self.connection(self.y,self.listrows,i)
        try:
            self.condition_plot()
            self.state_con()
        except:
            pass

    def connection(self,axis,plaintext,i):
        axisx = axis.split(',')
        deepaxis = axis.split(',')
        for a in range(len(axisx)):
            if deepaxis[a] == i:
                deepaxis.remove(i)
                text = ','.join(deepaxis)
                plaintext.setText(text)
                break



    def tellaxisplot(self,daidate):
        self.findaxis=[]
        for a in daidate:
            if a in self.listx:
               self.findaxis.append('x')
            if a in self.listy:
               self.findaxis.append('y')

    def genlist(self,inaxis):
        for i in inaxis:
            if i in self.catagories:
                self.dimentionplotlist.append(i)
            elif i in self.values:
                self.valuesplotlist.append(i)
            elif i in self.date:
                self.dateplotlist.append(i)
# select false
    def warning(self):
        self.error_dialog = QtWidgets.QErrorMessage()
        self.error_dialog.showMessage('Not acceptable for dimention3')
        self.error_dialog.exec_()

# choose date
    def creatdateselect(self):
        self.comboBox3 = QtWidgets.QComboBox(self.centralwidget)
        self.gridLayout.addWidget(self.comboBox3, 2, 0, 1, 1)
        datedata = ['all','years','months','dates']
        self.comboBox3.addItems(datedata)
        self.comboBox3.currentIndexChanged.connect(self.dateagain)

    def dateagain(self):
        try:
            formatdmy = str(self.comboBox3.currentText())
            if formatdmy == 'all' and 'y' not in self.findaxis:
                return self.win.plotbar(self.getdataform,self.listy,self.listx)
            elif formatdmy == 'all' and 'x' not in self.findaxis:
                return self.win.plotbary(self.getdataform,self.listx,self.listy)
            elif  'y' not in self.findaxis:
                self.getdataform2 = self.selectdate(self.getdataform,formatdmy)
                return self.win.plotbar(self.getdataform2,self.listx,self.listy)
            elif 'x' not in self.findaxis:
                self.getdataform2 = self.selectdate(self.getdataform,formatdmy)
                return self.win.plotbary(self.getdataform2,self.listy,self.listx)
        except:
            print('sorry')


    def retranslateUi(self, graph):
         _translate = QtCore.QCoreApplication.translate
         graph.setWindowTitle(_translate("graph", "MainWindow"))
         self.label_3.setText(_translate("graph", "COLUMNS"))
         self.label.setText(_translate("graph", "ROWS"))
         self.menuFile.setTitle(_translate("graph", "file"))
         self.actionOpen.setText(_translate("graph", "open"))


    def check_sum(self,read):
        connection = sqlite3.connect('database.db')
        cur = connection.cursor()
        cur.execute("SELECT * FROM check_sum where md5=?",(read,))
        list_do = []
        for i in cur.fetchone():
            list_do.append(i)
        self.date = list_do[1].split(',')
        self.catagories = list_do[2].split(',')
        self.values = list_do[3].split(',')
        self.key = list_do[4].split(',')
        cur.close()
        connection.close()


    def check_non(self,read):
        connection = sqlite3.connect('database.db')
        cur = connection.cursor()
        self.data = self.getdf(self.fileName)
        self.date = self.data[0]
        self.catagories = self.data[1]
        self.values = self.data[2]
        self.key = list(self.data[3])
        date = ','.join(self.date)
        catagories = ','.join(self.catagories)
        values = ','.join(self.values)
        key = ','.join(self.key)
        cur.execute("insert into check_sum values(?,?,?,?,?)",(read,date,catagories,values,key))
        connection.commit()
        cur.close()
        connection.close()
# choose button
    def getgraph_b(self):
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setText("Pie Chart")
        self.pushButton_4.clicked.connect(self.pie)
        self.verticalLayout.addWidget(self.pushButton_4)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setText("Line graph")
        self.pushButton.clicked.connect(self.line)
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setText("Bubble")
        self.pushButton_2.clicked.connect(self.Bubbel)
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.verticalLayout.addWidget(self.pushButton_5)
        self.pushButton_5.setText("Table")
        self.pushButton_5.clicked.connect(self.table)
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.verticalLayout.addWidget(self.pushButton_6)
        self.pushButton_6.setText("Bar Graph")
        self.pushButton_6.clicked.connect(self.bar)

    def getitemlist(self):
        self.cat.setFixedSize(470, 189)
        self.setitem(self.cat,self.catagories)
        self.cat.setHorizontalHeaderLabels(['Dimension'])
        self.verticalLayout2.addWidget(self.cat)
        self.valueslist.setFixedSize(470,189 )
        self.setitem(self.valueslist,self.values)
        self.valueslist.setHorizontalHeaderLabels(['Values'])
        self.verticalLayout2.addWidget(self.valueslist)
        self.datelist.setFixedSize(470,189 )
        self.setitem(self.datelist,self.date)
        self.datelist.setHorizontalHeaderLabels(['Date'])
        self.verticalLayout2.addWidget(self.datelist)
        self.addbutcol.setFixedSize(470,50)
        self.verticalLayout2.addWidget(self.addbutcol)
        self.addbutrows.setFixedSize(470,50)
        self.verticalLayout2.addWidget(self.addbutrows)
        self.setvalueforcheck()

# change data in database
    def changedata_cat(self):
        try:
            self.checking(self.catagories,self.itemnow)
            self.itemnow = self.cat.currentItem().text()
        except:
            self.itemnow = self.cat.currentItem().text()
            self.checking(self.catagories,self.itemnow)

    def changedata_val(self):
        try:
            self.checking(self.values,self.itemnow)
            self.itemnow = self.valueslist.currentItem().text()
        except:
            self.itemnow = self.valueslist.currentItem().text()
            self.checking(self.values,self.itemnow)

    def changedata_date(self):
        try:
            self.checking(self.date,self.itemnow)
            self.itemnow = self.datelist.currentItem().text()
        except:
            self.itemnow = self.datelist.currentItem().text()
            self.checking(self.date,self.itemnow)

    def checking(self,typechange,item):
        a = self.cat.rowCount()
        b = self.valueslist.rowCount()
        c = self.datelist.rowCount()
        if self.forcheck != [a,b,c]:
            typechange.remove(item)
            if self.forcheck[0] < a:
                self.catagories.append(item)
            if self.forcheck[1] < b:
                self.values.append(item)
            if self.forcheck[2] < c:
                self.date.append(item)
            self.setvalueforcheck()
            self.newinform()
# update data in database

    def newinform(self):
        dai = ','.join(self.catagories)
        val = ','.join(self.values)
        day = ','.join(self.date)
        key = ','.join(self.key)
        connection = sqlite3.connect('database.db')
        cur = connection.cursor()
        read = self.read
        cur.execute("DELETE FROM check_sum WHERE md5 = ? ",(read,))
        cur.execute("insert into check_sum values(?,?,?,?,?)",(read,day,dai,val,key))
        connection.commit()
        cur.close()
        connection.close()

    def setvalueforcheck(self):
        a = len(self.catagories)
        b = len(self.values)
        c = len(self.date)
        self.forcheck = [a,b,c]


    def addplaincol(self):
        if self.listcol.text() == '':
            self.x = list()
            self.x.append(self.itemnow)
            text = ','.join(self.x)
            self.listcol.setText(text)
        else:
            a = self.listcol.text()
            a = a.split(',')
            self.x = a
            self.x.append(self.itemnow)
            text = ','.join(self.x)
            self.listcol.setText(text)

    def addplainrow(self):
        if self.listrows.text() == '':
            self.y=list()
            self.y.append(self.itemnow)
            text = ','.join(self.y)
            self.listrows.setText(text)
        else:
            a = self.listrows.text()
            a = a.split(',')
            self.y = a
            self.y.append(self.itemnow)
            text = ','.join(self.y)
            self.listrows.setText(text)

    def getlist(self):
        self.cat = TableWidgetDragRows(self.centralwidget)
        self.verticalLayout2.addWidget(self.cat)
        self.valueslist = TableWidgetDragRows(self.centralwidget)
        self.verticalLayout2.addWidget(self.valueslist)
        self.datelist = TableWidgetDragRows(self.centralwidget)
        self.verticalLayout2.addWidget(self.datelist)
        self.addbutcol = QtWidgets.QPushButton(self.centralwidget)
        self.addbutcol.setText('Add To Colums')
        self.verticalLayout2.addWidget(self.addbutcol)
        self.addbutrows = QtWidgets.QPushButton(self.centralwidget)
        self.addbutrows.setText('Add To Rows')
        self.verticalLayout2.addWidget(self.addbutrows)
        self.cat.currentItemChanged.connect(self.changedata_cat)
        self.valueslist.currentItemChanged.connect(self.changedata_val)
        self.datelist.currentItemChanged.connect(self.changedata_date)
        self.addbutcol.clicked.connect(self.addplaincol)
        self.addbutrows.clicked.connect(self.addplainrow)

    def clearlist(self):
        pass


    def setitem(self,typelistwid,typeitemwid):
        typelistwid.setColumnCount(1)
        filled_widget = typelistwid
        for i, itemone in enumerate(typeitemwid):
            c = QtWidgets.QTableWidgetItem(itemone)
            filled_widget.insertRow(filled_widget.rowCount())
            filled_widget.setItem(i,0,c)
        header = typelistwid.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)


# plot graph
    def bar(self):
        if str(self.comboBox3.currentText()) != 'all':
            self.win.plotbar(self.getdataform2,self.in_key_di,self.in_key_val)
        else:
            self.win.plotbar(self.getdataform,self.in_key_di,self.in_key_val)
    def pie(self):
        if str(self.comboBox3.currentText()) != 'all':
            self.win.plot_pie(self.getdataform2)
        else:
            self.win.plot_pie(self.getdataform)
    def Bubbel(self):
        if str(self.comboBox3.currentText()) != 'all':
            self.win.plot_bubble(self.getdataform2)
        else:
            self.win.plot_bubble(self.getdataform)
    def line(self):
        if str(self.comboBox3.currentText()) != 'all':
            self.win.plot_line(self.getdataform2,self.in_key_di,self.in_key_val)
        else:
            self.win.plot_line(self.getdataform,self.in_key_di,self.in_key_val)
    def table(self):
        if str(self.comboBox3.currentText()) != 'all':
            self.win.table(self.getdataform2,self.in_key_di,self.in_key_val)
        else:
            self.win.table(self.getdataform,self.in_key_di,self.in_key_val)
# check label
    def onpick1(self,event):
        if isinstance(event.artist, Line2D):
            thisline = event.artist
            xdata = thisline.get_xdata()
            ydata = thisline.get_ydata()
            ind = event.ind
            print('onpick1 line:', zip(np.take(xdata, ind), np.take(ydata, ind)))
        elif isinstance(event.artist, Rectangle):
            patch = event.artist
            print('onpick1 patch:', patch.get_path())
        elif isinstance(event.artist, Text):
            text = event.artist
            print('onpick1 text:', text.get_text())
            self.filterlist2.setText(text.get_text())

    def treestyle(self):
        try:
            self.varforfilter()
            self.find_catagories()
            if self.in_key_di == []:
                self.tree_filter.clear()
                self.oldset = set()
            if len(self.in_key_date) != 0:
                self.in_key_di.append(self.in_key_date[0])
            if self.oldset == []:
                for i in self.in_key_di:
                    self.getchildinroot(i)
            else:
                copydeep = set(self.in_key_di)
                b = self.oldset.intersection(copydeep)
                fortree = copydeep - b
                if len(fortree) != 0:
                    for i in fortree:
                        self.getchildinroot(i)
                elif len(fortree) == 0:
                    for i in self.oldset-copydeep:
                        root = self.tree_filter.invisibleRootItem()
                        signal_count = root.childCount()
                        for a in range(signal_count):
                            signal = root.child(a)
                            if signal.text(0) == self.key[i]:
                                root.removeChild(signal)
                                self.oldset.remove(i)


            if len(self.in_key_di) >= 1:
                self.filter()
        except:
            pass

    def getchildinroot(self,i):
        data = self.dataset[self.key[i]]
        inform = data.tolist()
        notper = set(inform)
        parent = QtWidgets.QTreeWidgetItem(self.tree_filter)
        parent.setText(0, "{}".format(self.key[i]))
        parent.setFlags(parent.flags() |QtCore.Qt.ItemIsAutoTristate | QtCore.Qt.ItemIsUserCheckable)
        self.oldfilter(notper,parent)
        self.oldset.add(i)

    def oldfilter(self,notper,parent):
        for a in notper:
                    child = QtWidgets.QTreeWidgetItem(parent)
                    child.setFlags(child.flags() | QtCore.Qt.ItemIsUserCheckable)
                    child.setText(0, "{}".format(a))
                    child.setCheckState(0, QtCore.Qt.Checked)

    def find_checked(self):
        checked = dict()
        root = self.tree_filter.invisibleRootItem()
        signal_count = root.childCount()

        for i in range(signal_count):
            signal = root.child(i)
            checked_sweeps = list()
            num_children = signal.childCount()
            self.unchecked = list()
            for n in range(num_children):
                child = signal.child(n)
                if child.checkState(0) == QtCore.Qt.Checked:
                    checked_sweeps.append(child.text(0))
            self.incheck_remove(signal,root)

            checked[signal.text(0)] = checked_sweeps
        return checked

    def incheck_remove(self,signal,root):
        if signal.checkState(0) == QtCore.Qt.Unchecked:
                root.removeChild(signal)
                a = [i for i,x in enumerate(self.key) if x == signal.text(0)]
                self.in_key_di.remove(a[0])
                text = []
                if signal.text(0) in self.listcol.text():
                    for i in self.in_key_di:
                        text.append(self.key[i])
                    text = (',').join(text)
                    self.listcol.setText(text)
                elif signal.text(0) in self.listrows.text():
                    for i in self.in_key_di:
                        text.append(self.key[i])
                    text = (',').join(text)
                    self.listrows.setText(text)

                self.oldset.remove(a[0])



    def deleat_to_repeat(self,listdel):
        self.listrows.clear()
        self.listcol.clear()
        listdel.reset()
        while (listdel.rowCount() >= 1):
            listdel.model().removeRow(0)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
