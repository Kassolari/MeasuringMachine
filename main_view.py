from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 480)
        MainWindow.setMinimumSize(QtCore.QSize(800, 480))
        MainWindow.setMaximumSize(QtCore.QSize(800, 480))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pomiar = QtWidgets.QPushButton(self.centralwidget)
        self.pomiar.setGeometry(QtCore.QRect(30, 10, 361, 191))
        #self.pomiar.setGeometry(QtCore.QRect(30, 10, 361, 420))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        self.pomiar.setFont(font)
        self.pomiar.setObjectName("pomiar")
        self.wykres = QtWidgets.QPushButton(self.centralwidget)
        self.wykres.setGeometry(QtCore.QRect(410, 10, 361, 191))
        #self.wykres.setGeometry(QtCore.QRect(410, 10, 361, 420))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        self.wykres.setFont(font)
        self.wykres.setObjectName("wykres")
        self.stop = QtWidgets.QPushButton(self.centralwidget)
        self.stop.setGeometry(QtCore.QRect(30, 230, 741, 191))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(38)
        self.stop.setFont(font)
        self.stop.setObjectName("stop")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pomiar.setText(_translate("MainWindow", "Rozpocznij pomiar"))
        self.wykres.setText(_translate("MainWindow", "Pokaz wykres"))
        self.stop.setText(_translate("MainWindow", "Zatrzymaj"))