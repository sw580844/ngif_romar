# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui\test.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SingleToolpathPlots(object):
    def setupUi(self, SingleToolpathPlots):
        SingleToolpathPlots.setObjectName("SingleToolpathPlots")
        SingleToolpathPlots.resize(772, 393)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(SingleToolpathPlots)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.plot_br = QtWidgets.QWidget(SingleToolpathPlots)
        self.plot_br.setObjectName("plot_br")
        self.gridLayout.addWidget(self.plot_br, 1, 2, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(SingleToolpathPlots)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtWidgets.QLabel(SingleToolpathPlots)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.comboBox = QtWidgets.QComboBox(SingleToolpathPlots)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout.addWidget(self.comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.pushButton = QtWidgets.QPushButton(SingleToolpathPlots)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        self.plot_tr = QtWidgets.QWidget(SingleToolpathPlots)
        self.plot_tr.setObjectName("plot_tr")
        self.gridLayout.addWidget(self.plot_tr, 0, 2, 1, 1)
        self.plot_bl = QtWidgets.QWidget(SingleToolpathPlots)
        self.plot_bl.setObjectName("plot_bl")
        self.gridLayout.addWidget(self.plot_bl, 1, 1, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout)

        self.retranslateUi(SingleToolpathPlots)
        QtCore.QMetaObject.connectSlotsByName(SingleToolpathPlots)

    def retranslateUi(self, SingleToolpathPlots):
        _translate = QtCore.QCoreApplication.translate
        SingleToolpathPlots.setWindowTitle(_translate("SingleToolpathPlots", "Form"))
        self.label_3.setText(_translate("SingleToolpathPlots", "Toolpath viewing plots"))
        self.label_4.setText(_translate("SingleToolpathPlots", "Select toolpath"))
        self.pushButton.setText(_translate("SingleToolpathPlots", "Make plots"))
