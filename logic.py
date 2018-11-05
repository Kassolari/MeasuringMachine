#!/usr/bin/env python3

import sys
import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import main_view
import graph_view
import graph_view_digital
import serial
import time
import os.path
import RPi.GPIO as GPIO
import PyQt5.QtGui
import numpy as np

# ustawienie portu rs232

ser = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate = 9600,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.5
        )
# ustawienie pinow

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT) #Dir
GPIO.setup(27, GPIO.OUT) #Step
GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_UP) # Czujnik przy silniku
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP) # Czujnik na koncu

# create class for our Raspberry Pi GUI

class GraphWindow(QMainWindow, graph_view.Ui_MainWindow):
    def __init__(self,parent):
        super(GraphWindow, self).__init__(parent)
        self.setupUi(self) # gets defined in the UI file

 
class DigitalWindow(QMainWindow, graph_view_digital.Ui_MainWindow):
    def __init__(self,parent):
        super(DigitalWindow, self).__init__(parent)
        self.setupUi(self) # gets defined in the UI file 
    

class MainWindow(QMainWindow, main_view.Ui_MainWindow):
    # access variables inside of the UI's file
    global my_dir
    my_dir = "Bad path"
    
    global tablica_wynikow
    tablica_wynikow = []
    
    global tablica_pom_10
    tablica_pom_10 = []
    
    global x_fin
    x_fin = 0
    
    global y_fin
    y_fin = 0

    
    ### functions for the buttons to call
    def pressedstop(self):
        global stop
        stop = 1
        
    def pressedpomiar(self):
        global stop
        global tablica_wynikow
        global tablica_pom_10
        global x_fin
        global y_fin
        
        self.pomiar.setEnabled(False)
        stop = 0
        logika_GUI()
        parkuj()
        self.pressedwykres()
        zapis(tablica_wynikow,tablica_pom_10,x_fin,y_fin)
        self.pomiar.setEnabled(True)
        
        
        
    def pressedwykres(self):
        global tablica_wynikow
        global tablica_pom_10
        global x_fin
        global y_fin
              
        tablica_pom_10 = []
        if len(tablica_wynikow) > 98:
            graph = GraphWindow(self)
            graph1 = DigitalWindow(self)
            graph.graphicsView.plot(tablica_wynikow, pen=0)
            x = len(tablica_wynikow)
            
            for pom in range (x-3):
                sma = 0
                for pom_in in range (0,3):
                    sma = sma + tablica_wynikow[pom+pom_in]
                    if pom_in == 2:
                        sma = round(sma/3,2)
                tablica_pom_10.append(sma)
            
            xpomo=0
            for pom in range (x-3,x):
                sma = 0
                for pom_in in range (0,3-xpomo):
                    sma = sma + tablica_wynikow[pom+pom_in]
                    if pom_in == 2-xpomo:
                        sma = round(sma/(3-xpomo),2)
                tablica_pom_10.append(sma) 
                xpomo = xpomo + 1
                
            tablica_lewo = tablica_pom_10.copy()
            tablica_prawo = tablica_pom_10.copy()
            graph.showFullScreen()
            
            x_aver = round(len(tablica_pom_10)/2)
            y_aver = tablica_pom_10[x_aver]
            range_max = len(tablica_pom_10)
            
            del tablica_lewo[x_aver:range_max]
            del tablica_prawo[0:x_aver]
            
            ymax_lewo = max(tablica_lewo)
            xmax_lewo = tablica_lewo.index(ymax_lewo)
            
            ymax_prawo = max(tablica_prawo)
            xmax_prawo = x_aver + tablica_prawo.index(ymax_prawo)
            
            A = np.array([[xmax_lewo,1],[xmax_prawo,1]])
            B = np.array ([ymax_lewo,ymax_prawo])
            
            x_b_table = np.linalg.solve(A,B)
            x = x_b_table[0]
            b = x_b_table[1]
            
            y_fin = 0
            x_fin = 0
            y_pom = 0      
            
            for pom_pom in range (xmax_lewo,xmax_prawo+1):
                y_pom = pom_pom*x + b
                y_pom = y_pom - tablica_pom_10[pom_pom]
                if y_pom >= y_fin:
                    y_fin = y_pom
                    x_fin = pom_pom
                    
            graph1.lcdNumber.display(y_fin)
            graph1.graphicsView.plot(tablica_pom_10, pen=1)
            graph1.graphicsView.plot([x_fin,x_fin],[tablica_pom_10[x_fin],x_fin*x+b], pen=2)
            graph1.graphicsView.plot([xmax_lewo,xmax_prawo],[ymax_lewo,ymax_prawo], pen=3)
            
            while graph.isVisible() == True:
                QApplication.processEvents()
            graph1.showFullScreen()
            
    
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self) # gets defined in the UI file

        ### Hooks to for buttons
      
        self.wykres.clicked.connect(lambda: self.pressedwykres())
        self.pomiar.clicked.connect(lambda: self.pressedpomiar())
        self.stop.clicked.connect(lambda: self.pressedstop())

 
def zapis(a,b,c,d):
    global my_dir
    filenumber = 0
    
    while os.path.isfile("%s/Pomiar%i.txt"%(str(my_dir),filenumber)):
        filenumber += 1
    if os.path.isdir(my_dir) != False:
        file = open("%s/Pomiar%i.txt"%(str(my_dir),filenumber),'+a')
    if os.path.isdir(my_dir) != False:
        xx = 1
        file.write("Delta: %.2f \n"%d)
        file.write("W punkcie: %i \n"%c)
        for item in a:
            file.write("Pomiar%i: "%xx)
            file.write(format(item))
            file.write("\n")
            xx += 1
        xx = 1
        file.write("Pomiary SMA :------------- \n")
        for item in b:
            file.write("Pomiar SMA%i: "%xx)
            file.write(format(item))
            file.write("\n")
            xx += 1
        file.close()
    
def logika_GUI():
    global my_dir
    global stop
    global tablica_wynikow

    tablica_wynikow = []
    
    #Wybranie folderu zapisu tylko za pierwszym razem i sprawdzenie czy folder istnieje
    if os.path.isdir(my_dir) == False:
        dialog = QFileDialog(None,"Wybierz folder","media/pi/")
        dialog.setFileMode(2)
        dialog.setViewMode(1)
        dialog.setLabelText(4,"Pomiar bez zapisu")
        dialog.setLabelText(3,"Wybierz folder do zapisu pomiarow")
        dialog.setOption(QFileDialog.ShowDirsOnly)
        dialog.showFullScreen()
        if(dialog.exec()):
            my_dir = dialog.selectedFiles()[0]
            print(my_dir)
            if my_dir == "/media/pi":
                my_dir = "nic"
                print(my_dir)
            
        else:
            my_dir = "nic"
            
    #odpalenie silnika i parkowanie wskaznika
    parkuj()
    
    GPIO.output(17,GPIO.HIGH)

    # ilosc krokow na 8000 rozdzialce to 158600
    # ilosc krokow na 4000 rozdzialce to 79100
    # ilosc krokow na 2000 rozdzialce to 39450
    for x in range (100):
        tablica_wynikow.append(pomiar())
        QApplication.processEvents()
        time.sleep(1/10)
        if stop == 1:
            break
        for y in range (78):
            step()
        
    
     
     
def parkuj():
    GPIO.output(17,GPIO.LOW)
    while GPIO.input(24) == False:
        time.sleep(1/2000)
        GPIO.output(27,GPIO.HIGH)
        time.sleep(1/2000)          
        GPIO.output(27,GPIO.LOW)
    GPIO.output(17,GPIO.HIGH)
    while GPIO.input(24) == True:
        GPIO.output(27,GPIO.HIGH)
        time.sleep(1/2000)          
        GPIO.output(27,GPIO.LOW)
              
def step():
    GPIO.output(27,GPIO.HIGH)
    time.sleep(1/2000)           
    GPIO.output(27,GPIO.LOW)
    time.sleep(1/2000)  

def pomiar():
    t = 0
    ser.write(bytes([0x01, 0x86]))
    # wczytanie poszczegolnych bitow
    data = ser.read(4)
    if len(data) == 4:
        # wyliczenie wyniku
        rawValue = (data[0] & 0x0F) + ((data[1] & 0x0F) << 4) \
        + ((data[2] & 0x0F) << 8) + ((data[3] & 0x0F) << 12)
        t = 50.8 - rawValue * 100 / 16384
    return round(t,2)
  
def main():
    # a new app instance
    app = QApplication(sys.argv)
    form = MainWindow()
    form.showFullScreen()
    # without this, the script exits immediately.
    sys.exit(app.exec_())
# python bit to figure how who started This
if __name__ == "__main__":
    main()
