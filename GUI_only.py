#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from __future__ import unicode_literals
import sys
import os
import random
import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from iFilter import iImage

progname = os.path.basename(sys.argv[0])
progversion = "0.1"

# Starter Code from
# https://matplotlib.org/examples/user_interfaces/embedding_in_qt5.html

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
        
    def __init__(self, parent=None, image=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.axes.imshow(image)


    def compute_initial_figure(self):
        pass


class MyStaticMplCanvas(MyMplCanvas):

    @classmethod
    def compute_initial_figure(cls, parent, **kwargs):
        image=iImage.load('/home/sufiyan/Downloads/eye.png').RGB
        return cls(parent, image=image, **kwargs)
        
    
    @classmethod
    def imshow(cls, parent, image, **kwargs):
        if isinstance(image, iImage): #handles both iImage instance or RGB Image directly
            image=image.RGB
        return cls(parent, image, **kwargs)



from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")
        self.setupUi()
        self.set_button_bindings()

    def setupUi(self):
        # MainWindow.setObjectName("MainWindow")
        # MainWindow.resize(858, 572)
        self.centralWidget = QtWidgets.QWidget()
        self.centralWidget.setObjectName("centralWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")

        self.listWidget = QtWidgets.QListWidget(self.splitter)
        self.listWidget.setObjectName("listWidget")
        # self.gridLayout_2.addWidget(self.listWidget, 8, 1, 1, 1)

        self.stackedWidget = QtWidgets.QStackedWidget(self.splitter)
        self.stackedWidget.setEnabled(True)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_main = QtWidgets.QWidget()
        self.page_main.setObjectName("page_main")
        self.gridLayout = QtWidgets.QGridLayout(self.page_main)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.button_browse = QtWidgets.QPushButton(self.page_main)
        self.button_browse.setObjectName("button_browse")
        self.gridLayout.addWidget(self.button_browse, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.button_quit = QtWidgets.QPushButton(self.page_main)
        self.button_quit.setObjectName("button_quit")
        self.gridLayout.addWidget(self.button_quit, 3, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_main)
        self.page_edit = QtWidgets.QWidget()
        self.page_edit.setObjectName("page_edit")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.page_edit)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.button_back = QtWidgets.QPushButton(self.page_edit)
        self.button_back.setObjectName("button_back")
        self.gridLayout_2.addWidget(self.button_back, 13, 0, 1, 1)
        self.button_sharpen = QtWidgets.QPushButton(self.page_edit)
        self.button_sharpen.setObjectName("button_sharpen")
        self.gridLayout_2.addWidget(self.button_sharpen, 8, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 5, 0, 1, 1)
        self.button_hist = QtWidgets.QPushButton(self.page_edit)
        self.button_hist.setAutoDefault(False)
        self.button_hist.setFlat(False)
        self.button_hist.setObjectName("button_hist")
        self.gridLayout_2.addWidget(self.button_hist, 0, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem2, 11, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem3, 3, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem4, 9, 0, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem5, 1, 0, 1, 1)
        self.button_blur = QtWidgets.QPushButton(self.page_edit)
        self.button_blur.setObjectName("button_blur")
        self.gridLayout_2.addWidget(self.button_blur, 6, 0, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem6, 7, 0, 1, 1)
        self.button_save = QtWidgets.QPushButton(self.page_edit)
        self.button_save.setObjectName("button_save")
        self.gridLayout_2.addWidget(self.button_save, 12, 0, 1, 1)
        self.button_gamma = QtWidgets.QPushButton(self.page_edit)
        self.button_gamma.setObjectName("button_gamma")
        self.gridLayout_2.addWidget(self.button_gamma, 4, 0, 1, 1)
        self.button_log = QtWidgets.QPushButton(self.page_edit)
        self.button_log.setObjectName("button_log")
        self.gridLayout_2.addWidget(self.button_log, 2, 0, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem7, 10, 0, 1, 1)
        
        self.stackedWidget.addWidget(self.page_edit)
        self.page_hist = QtWidgets.QWidget()
        self.page_hist.setObjectName("page_hist")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.page_hist)
        self.gridLayout_3.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.apply_hist = QtWidgets.QPushButton(self.page_hist)
        self.apply_hist.setObjectName("apply_hist")
        self.gridLayout_3.addWidget(self.apply_hist, 5, 0, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem8, 4, 0, 1, 1)
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem9, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.page_hist)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 1, 0, 1, 1)
        self.slider_hist = QtWidgets.QSlider(self.page_hist)
        self.slider_hist.setMaximum(5)
        self.slider_hist.setOrientation(QtCore.Qt.Horizontal)
        self.slider_hist.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.slider_hist.setObjectName("slider_hist")
        self.gridLayout_3.addWidget(self.slider_hist, 2, 0, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem10, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_hist)
        self.page_log = QtWidgets.QWidget()
        self.page_log.setObjectName("page_log")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.page_log)
        self.gridLayout_4.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_4.setSpacing(6)
        self.gridLayout_4.setObjectName("gridLayout_4")
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem11, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.page_log)
        self.label_2.setObjectName("label_2")
        self.gridLayout_4.addWidget(self.label_2, 1, 0, 1, 1)
        spacerItem12 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem12, 4, 0, 1, 1)
        self.apply_log = QtWidgets.QPushButton(self.page_log)
        self.apply_log.setObjectName("apply_log")
        self.gridLayout_4.addWidget(self.apply_log, 5, 0, 1, 1)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setSpacing(6)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_3 = QtWidgets.QLabel(self.page_log)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.text_log = QtWidgets.QLineEdit(self.page_log)
        self.text_log.setObjectName("text_log")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.text_log)
        self.gridLayout_4.addLayout(self.formLayout_2, 2, 0, 1, 1)
        spacerItem13 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem13, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_log)
        self.page_gamma = QtWidgets.QWidget()
        self.page_gamma.setObjectName("page_gamma")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.page_gamma)
        self.gridLayout_5.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_5.setSpacing(6)
        self.gridLayout_5.setObjectName("gridLayout_5")
        spacerItem14 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem14, 5, 0, 1, 1)
        spacerItem15 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem15, 4, 0, 1, 1)
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setSpacing(6)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_4 = QtWidgets.QLabel(self.page_gamma)
        self.label_4.setObjectName("label_4")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.text_gamma = QtWidgets.QLineEdit(self.page_gamma)
        self.text_gamma.setObjectName("text_gamma")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.text_gamma)
        self.gridLayout_5.addLayout(self.formLayout_3, 3, 0, 1, 1)
        self.apply_gamma = QtWidgets.QPushButton(self.page_gamma)
        self.apply_gamma.setObjectName("apply_gamma")
        self.gridLayout_5.addWidget(self.apply_gamma, 6, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.page_gamma)
        self.label_5.setObjectName("label_5")
        self.gridLayout_5.addWidget(self.label_5, 1, 0, 1, 1)
        spacerItem16 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem16, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_gamma)
        self.page_blur = QtWidgets.QWidget()
        self.page_blur.setObjectName("page_blur")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.page_blur)
        self.gridLayout_6.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_6.setSpacing(6)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.apply_blur = QtWidgets.QPushButton(self.page_blur)
        self.apply_blur.setObjectName("apply_blur")
        self.gridLayout_6.addWidget(self.apply_blur, 4, 0, 1, 1)
        self.formLayout_4 = QtWidgets.QFormLayout()
        self.formLayout_4.setSpacing(6)
        self.formLayout_4.setObjectName("formLayout_4")
        self.label_6 = QtWidgets.QLabel(self.page_blur)
        self.label_6.setObjectName("label_6")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.slider_blur = QtWidgets.QSlider(self.page_blur)
        self.slider_blur.setMinimum(1)
        self.slider_blur.setMaximum(11)
        self.slider_blur.setSingleStep(2)
        self.slider_blur.setOrientation(QtCore.Qt.Horizontal)
        self.slider_blur.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slider_blur.setObjectName("slider_blur")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.slider_blur)
        self.gridLayout_6.addLayout(self.formLayout_4, 2, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.page_blur)
        self.label_7.setObjectName("label_7")
        self.gridLayout_6.addWidget(self.label_7, 1, 0, 1, 1)
        spacerItem17 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem17, 0, 0, 1, 1)
        spacerItem18 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem18, 3, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_blur)
        self.page_sharpen = QtWidgets.QWidget()
        self.page_sharpen.setObjectName("page_sharpen")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.page_sharpen)
        self.gridLayout_7.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_7.setSpacing(6)
        self.gridLayout_7.setObjectName("gridLayout_7")
        spacerItem19 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_7.addItem(spacerItem19, 4, 0, 1, 1)
        spacerItem20 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_7.addItem(spacerItem20, 0, 0, 1, 1)
        self.apply_sharpen = QtWidgets.QPushButton(self.page_sharpen)
        self.apply_sharpen.setObjectName("apply_sharpen")
        self.gridLayout_7.addWidget(self.apply_sharpen, 5, 0, 1, 1)
        self.formLayout_5 = QtWidgets.QFormLayout()
        self.formLayout_5.setSpacing(6)
        self.formLayout_5.setObjectName("formLayout_5")
        self.label_8 = QtWidgets.QLabel(self.page_sharpen)
        self.label_8.setObjectName("label_8")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.slider_sharpen = QtWidgets.QSlider(self.page_sharpen)
        self.slider_sharpen.setMaximum(30)
        self.slider_sharpen.setOrientation(QtCore.Qt.Horizontal)
        self.slider_sharpen.setObjectName("slider_sharpen")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.slider_sharpen)
        self.gridLayout_7.addLayout(self.formLayout_5, 2, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.page_sharpen)
        self.label_9.setObjectName("label_9")
        self.gridLayout_7.addWidget(self.label_9, 1, 0, 1, 1)
        spacerItem21 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_7.addItem(spacerItem21, 3, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_sharpen)
        self.display_widget = QtWidgets.QWidget(self.splitter)
        self.display_widget.setObjectName("display_widget")
        self.display_layout = QtWidgets.QVBoxLayout(self.display_widget)
        self.display = MyStaticMplCanvas.compute_initial_figure(self.display_widget, width=5, height=4, dpi=100)
        self.display_layout.addWidget(self.display)
        self.horizontalLayout.addWidget(self.splitter)
        self.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(self)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 858, 22))
        self.menuBar.setObjectName("menuBar")
        self.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(self)
        self.mainToolBar.setObjectName("mainToolBar")
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(self)
        self.statusBar.setObjectName("statusBar")
        self.setStatusBar(self.statusBar)

        self.retranslateUi()
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.button_browse.setText(_translate("MainWindow", "Browse..."))
        self.button_quit.setText(_translate("MainWindow", "Quit"))
        self.button_back.setText(_translate("MainWindow", "Back"))
        self.button_sharpen.setText(_translate("MainWindow", "Sharpen"))
        self.button_hist.setText(_translate("MainWindow", "Histogram Equalization"))
        self.button_blur.setText(_translate("MainWindow", "Blur"))
        self.button_save.setText(_translate("MainWindow", "Save"))
        self.button_gamma.setText(_translate("MainWindow", "Gamma Correction"))
        self.button_log.setText(_translate("MainWindow", "Log Transform"))
        self.apply_hist.setText(_translate("MainWindow", "Apply"))
        self.label.setText(_translate("MainWindow", "Histogram Equalization"))
        self.label_2.setText(_translate("MainWindow", "Log Transform"))
        self.apply_log.setText(_translate("MainWindow", "Apply"))
        self.label_3.setText(_translate("MainWindow", "Log Base"))
        self.text_log.setText(_translate("MainWindow", "e"))
        self.label_4.setText(_translate("MainWindow", "Gamma Value"))
        self.text_gamma.setText(_translate("MainWindow", "1"))
        self.apply_gamma.setText(_translate("MainWindow", "Apply"))
        self.label_5.setText(_translate("MainWindow", "Gamma Correction"))
        self.apply_blur.setText(_translate("MainWindow", "Apply"))
        self.label_6.setText(_translate("MainWindow", "Filter Size"))
        self.label_7.setText(_translate("MainWindow", "Blur"))
        self.apply_sharpen.setText(_translate("MainWindow", "Apply"))
        self.label_8.setText(_translate("MainWindow", "Sharpness"))
        self.label_9.setText(_translate("MainWindow", "Adjust Sharpness"))

    
    def imshow_(self, image):
        if isinstance(image, iImage):
            image=image.RGB
        self.display_layout.removeWidget(self.display)
        self.display = MyStaticMplCanvas.imshow(self.display_widget, image, width=5, height=4, dpi=100)
        self.display_layout.addWidget(self.display)
    
    def get_file(self): #Get file Name when Browse is clicked
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File, QtCore.QDir.rootPath() , *.*')
        self.image = iImage.load(fileName)
        self.imshow_(self.image)
        self.stackedWidget.setCurrentIndex(1)

    def set_button_bindings(self):
        self.button_browse.clicked.connect(self.get_file)
        self.button_quit.clicked.connect(self.close)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())

