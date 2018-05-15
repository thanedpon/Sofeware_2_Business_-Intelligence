import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class PlotCanvas(FigureCanvas):

    def __init__(self,parent = None,*args,**kwargs):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        self.factor = kwargs.pop("factor", 2)
        FigureCanvas.__init__(self, fig, *args,**kwargs)

        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,QSizePolicy.Expanding,QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.setFocusPolicy( Qt.ClickFocus )
        self.setFocus()

        self.scroll = QScrollBar(Qt.Horizontal)
        self.scroll2 = QScrollBar(Qt.Vertical)
        #self.scroll3 = QScrollBar(Qt.Vertical)
        self.scroll.actionTriggered.connect(self.updateFromScroll)
        self.scroll2.actionTriggered.connect(self.updateFromScroll2)
        #self.scroll3.actionTriggered.connect(self.updateFromScroll3)

    def plotbar(self,xy,x,y):
        self.scroll2.setVisible(False)
        self.scroll.setVisible(True)
        self.getdict(xy)
        xs = np.arange(len(self.plotx))
        self.ax.bar(xs,self.ploty,width=0.5,align='center',color='lightpink',picker=True)
        self.ax.set_xlabel(x)
        self.ax.set_ylabel(y)
        self.ax.set_xticks(xs)
        self.ax.set_xticklabels(self.plotx,rotation=90)
        for label in self.ax.get_xticklabels():  # make the xtick labels pickable
            label.set_picker(True)
        self.ax.grid(True)
        self.ax.set_xlim([-5,20])
        self.xmin,self.xmax = self.ax.get_xlim()
        self.ax.set_xlim(self.xmin, self.xmax)
        self.draw()


    def updateFromScroll(self, evt):
        v = self.scroll.value()
        print(v)
        a = [self.xmin, self.xmax/float(self.factor)]
        lim = a+v/100.*np.diff(a)[0]
        self.ax.set_xlim(lim)
        self.draw_idle()

    def updateFromScroll2(self, evt):
        v = self.scroll2.value()
        a = [self.ymin,self.ymax/float(self.factor)]
        lim = a+v/100.*np.diff(a)[0]
        self.ax.set_ylim(lim)
        self.draw_idle()



    def plotbary(self,xy,x,y):
        self.scroll.setVisible(False)
        self.scroll2.setVisible(True)
        self.getdict(xy)
        xs = np.arange(len(self.plotx))
        error = np.random.rand(len(self.plotx))
        self.ax.set_yticks(xs)
        self.ax.set_yticklabels(self.plotx,picker=True)
        self.ax.set_xlabel(y)
        self.ax.set_ylabel(x)
        self.ax.barh(xs, self.ploty, xerr=error, align='center',color='lightpink',picker=True)
        for label in self.ax.get_xticklabels():  # make the xtick labels pickable
            label.set_picker(True)
        self.ax.grid(True)
        self.ax.set_ylim([-5,20])
        self.ymin,self.ymax = self.ax.get_ylim()
        self.ax.set_ylim(self.ymin, self.ymax)
        self.draw()

    def plot_pie(self,xy):
        self.scroll.setVisible(False)
        self.scroll2.setVisible(False)
        self.getdict(xy)
        colors = ['tomato', 'darksalmon', 'rosybrown', 'lightcoral','indianred','darkred','lightpink','coral','hotpink','mistyrose']
        labels = self.plotx
        sizes = self.ploty
        patches,text = self.ax.pie(sizes,colors=colors, shadow=True,startangle=140)
        self.ax.legend(patches, labels,bbox_to_anchor=(0.85,1.025),loc="upper left")
        self.draw()

    def plot_line(self,xy,x,y):
        self.getdict(xy)
        xs = np.arange(len(self.plotx))
        num = 0
        for i in range(len(self.plotx)):
            num += 1
        self.ax.plot(xs,self.ploty,marker='',color='darksalmon', linewidth=3, alpha=0.9, label=x)
        self.ax.set_xticks(xs)
        self.ax.set_xticklabels(self.plotx)
        self.ax.grid(True)
        self.ax.set_xlabel(x)
        self.ax.set_ylabel(y)
        self.ax.set_xlim(self.xmin, self.xmax/float(self.factor))
        self.draw()

    def plot_bubble(self,xy):
        self.getdict(xy)
        x = np.arange(len(self.plotx))
        self.ax.grid(True)
        self.ax.scatter(x, self.ploty)
        self.draw()

#edit
    def table(self,xy,x,y):
        self.getdict(xy)
        tablelist = []
        for i in range(len(self.plotx)):
            tablelist.append([self.plotx[i],self.ploty[i]])
        head = (x,y)
        self.ax.xaxis.set_visible(False)
        self.ax.yaxis.set_visible(False)
        self.ax.table(cellText=tablelist,colLabels=head,loc='center')
        self.draw()


    def getdict(self,xy):
        self.ax = self.figure.add_subplot(111)
        self.ax.clear()
        self.ax.xaxis.set_visible(True)
        self.ax.yaxis.set_visible(True)
        self.plotx = []
        self.ploty = []
        for a in xy:
            self.plotx.append(a[0])
            self.ploty.append(a[1])






