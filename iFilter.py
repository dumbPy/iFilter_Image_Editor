#! /usr/bin/env python

import sys
from PyQt5.QtWidgets import  QApplication, QWidget, QToolTip, QPushButton
from PyQt5.QtGui import QFont

class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initGUI()
    def initGUI(self):
        
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('This is a <b>QWidget<\b> Widget')
        
        btn=QPushButton('RandomButton', self)
        btn.setToolTip('This is a <b>Random Botton<\b>')
        btn.resize(btn.sizeHint())
        btn.move(50, 50)

        self.setGeometry(300, 300, 400, 500)
        self.setWindowTitle("Using tooltips")
        self.show()
        


if __name__=="__main__":
    app=QApplication(sys.argv)

    gui=GUI()
    sys.exit(app.exec_())