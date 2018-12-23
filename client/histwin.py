# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'histwin.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_histwin(object):
    def setupUi(self, histwin):
        histwin.setObjectName("histwin")
        histwin.resize(324, 264)
        self.verticalLayoutWidget = QtWidgets.QWidget(histwin)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 30, 321, 231))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.histogram = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.histogram.setContentsMargins(0, 0, 0, 0)
        self.histogram.setObjectName("histogram")
        self.frame = QtWidgets.QFrame(histwin)
        self.frame.setGeometry(QtCore.QRect(0, 0, 311, 23))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.pctOverB = QtWidgets.QLabel(self.frame)
        self.pctOverB.setGeometry(QtCore.QRect(125, 3, 41, 17))
        self.pctOverB.setStyleSheet("background-color: white; color: blue")
        self.pctOverB.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.pctOverB.setText("")
        self.pctOverB.setTextFormat(QtCore.Qt.PlainText)
        self.pctOverB.setObjectName("pctOverB")
        self.pctOverR = QtWidgets.QLabel(self.frame)
        self.pctOverR.setGeometry(QtCore.QRect(35, 3, 41, 17))
        self.pctOverR.setStyleSheet("background-color: white; color: red")
        self.pctOverR.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.pctOverR.setText("")
        self.pctOverR.setTextFormat(QtCore.Qt.PlainText)
        self.pctOverR.setObjectName("pctOverR")
        self.pctOverG = QtWidgets.QLabel(self.frame)
        self.pctOverG.setGeometry(QtCore.QRect(80, 3, 41, 17))
        self.pctOverG.setStyleSheet("background-color: white; color: green")
        self.pctOverG.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.pctOverG.setText("")
        self.pctOverG.setTextFormat(QtCore.Qt.PlainText)
        self.pctOverG.setObjectName("pctOverG")
        self.label_9 = QtWidgets.QLabel(self.frame)
        self.label_9.setGeometry(QtCore.QRect(168, 3, 31, 17))
        self.label_9.setObjectName("label_9")
        self.pctUnder = QtWidgets.QLabel(self.frame)
        self.pctUnder.setGeometry(QtCore.QRect(198, 3, 41, 17))
        self.pctUnder.setStyleSheet("background-color: white")
        self.pctUnder.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.pctUnder.setText("")
        self.pctUnder.setTextFormat(QtCore.Qt.PlainText)
        self.pctUnder.setObjectName("pctUnder")
        self.pctAvg = QtWidgets.QLabel(self.frame)
        self.pctAvg.setGeometry(QtCore.QRect(271, 4, 41, 17))
        self.pctAvg.setStyleSheet("background-color: white")
        self.pctAvg.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.pctAvg.setText("")
        self.pctAvg.setTextFormat(QtCore.Qt.PlainText)
        self.pctAvg.setObjectName("pctAvg")
        self.label_19 = QtWidgets.QLabel(self.frame)
        self.label_19.setGeometry(QtCore.QRect(241, 1, 31, 21))
        self.label_19.setObjectName("label_19")
        self.label_35 = QtWidgets.QLabel(self.frame)
        self.label_35.setGeometry(QtCore.QRect(0, 2, 31, 17))
        self.label_35.setObjectName("label_35")

        self.retranslateUi(histwin)
        QtCore.QMetaObject.connectSlotsByName(histwin)

    def retranslateUi(self, histwin):
        _translate = QtCore.QCoreApplication.translate
        histwin.setWindowTitle(_translate("histwin", "Pi Film Capture"))
        self.label_9.setText(_translate("histwin", "%Lo:"))
        self.label_19.setText(_translate("histwin", "Avg:"))
        self.label_35.setText(_translate("histwin", "%Hi:"))

