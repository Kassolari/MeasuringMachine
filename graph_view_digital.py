from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 480)
        MainWindow.setMinimumSize(QtCore.QSize(800, 480))
        MainWindow.setMaximumSize(QtCore.QSize(800, 480))
        MainWindow.setBaseSize(QtCore.QSize(800, 480))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.close_graph = QtWidgets.QPushButton(self.centralwidget)
        self.close_graph.setGeometry(QtCore.QRect(0, 420, 400, 60))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(23)
        self.close_graph.setFont(font)
        self.close_graph.setAutoDefault(False)
        self.close_graph.setObjectName("close_graph")
        self.graphicsView = pg.PlotWidget(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 800, 420))
        self.graphicsView.setObjectName("graphicsView")
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(400, 420, 400, 60))
        self.lcdNumber.setMinimumSize(QtCore.QSize(400, 60))
        self.lcdNumber.setMaximumSize(QtCore.QSize(400, 60))
        self.lcdNumber.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lcdNumber.setSmallDecimalPoint(False)
        self.lcdNumber.setDigitCount(5)
        self.lcdNumber.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber.setObjectName("lcdNumber")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.close_graph.clicked.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.close_graph.setText(_translate("MainWindow", "Zamknij"))

