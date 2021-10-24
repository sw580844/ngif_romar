# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(880, 617)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_layout = QtWidgets.QVBoxLayout()
        self.button_layout.setContentsMargins(-1, -1, 0, -1)
        self.button_layout.setObjectName("button_layout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.button_layout.addWidget(self.label)
        self.open_file_button = QtWidgets.QPushButton(self.centralwidget)
        self.open_file_button.setObjectName("open_file_button")
        self.button_layout.addWidget(self.open_file_button)
        self.preprocess_file_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.preprocess_file_checkbox.setChecked(True)
        self.preprocess_file_checkbox.setObjectName("preprocess_file_checkbox")
        self.button_layout.addWidget(self.preprocess_file_checkbox)
        self.combo_box_select_page = QtWidgets.QComboBox(self.centralwidget)
        self.combo_box_select_page.setObjectName("combo_box_select_page")
        self.combo_box_select_page.addItem("")
        self.combo_box_select_page.addItem("")
        self.combo_box_select_page.addItem("")
        self.combo_box_select_page.addItem("")
        self.button_layout.addWidget(self.combo_box_select_page)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.button_layout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.button_layout)
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_1 = QtWidgets.QWidget()
        self.page_1.setObjectName("page_1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.page_1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.page1_topright = QtWidgets.QWidget(self.page_1)
        self.page1_topright.setObjectName("page1_topright")
        self.gridLayout.addWidget(self.page1_topright, 0, 2, 1, 1)
        self.page1_bottomleft = QtWidgets.QWidget(self.page_1)
        self.page1_bottomleft.setObjectName("page1_bottomleft")
        self.gridLayout.addWidget(self.page1_bottomleft, 1, 1, 1, 1)
        self.page1_bottomright = QtWidgets.QWidget(self.page_1)
        self.page1_bottomright.setObjectName("page1_bottomright")
        self.gridLayout.addWidget(self.page1_bottomright, 1, 2, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.page1_label = QtWidgets.QLabel(self.page_1)
        self.page1_label.setAlignment(QtCore.Qt.AlignCenter)
        self.page1_label.setObjectName("page1_label")
        self.verticalLayout_3.addWidget(self.page1_label)
        self.make_plots_button = QtWidgets.QPushButton(self.page_1)
        self.make_plots_button.setObjectName("make_plots_button")
        self.verticalLayout_3.addWidget(self.make_plots_button)
        self.plot_laser_on = QtWidgets.QCheckBox(self.page_1)
        self.plot_laser_on.setObjectName("plot_laser_on")
        self.verticalLayout_3.addWidget(self.plot_laser_on)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_2 = QtWidgets.QLabel(self.page_1)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_6.addWidget(self.label_2)
        self.rolling_window_seconds = QtWidgets.QDoubleSpinBox(self.page_1)
        self.rolling_window_seconds.setObjectName("rolling_window_seconds")
        self.horizontalLayout_6.addWidget(self.rolling_window_seconds)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_1)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.page_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.page2_topright = QtWidgets.QWidget(self.page_2)
        self.page2_topright.setObjectName("page2_topright")
        self.gridLayout_6.addWidget(self.page2_topright, 0, 1, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_4 = QtWidgets.QLabel(self.page_2)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.pushButton_make_toolpath_plots = QtWidgets.QPushButton(self.page_2)
        self.pushButton_make_toolpath_plots.setObjectName("pushButton_make_toolpath_plots")
        self.verticalLayout.addWidget(self.pushButton_make_toolpath_plots)
        self.gridLayout_6.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.page2_bottomright = QtWidgets.QWidget(self.page_2)
        self.page2_bottomright.setObjectName("page2_bottomright")
        self.gridLayout_6.addWidget(self.page2_bottomright, 1, 1, 1, 1)
        self.page2_bottomleft = QtWidgets.QWidget(self.page_2)
        self.page2_bottomleft.setObjectName("page2_bottomleft")
        self.gridLayout_6.addWidget(self.page2_bottomleft, 1, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_6, 0, 1, 1, 1)
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.page_3)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.page3_topright = QtWidgets.QLabel(self.page_3)
        self.page3_topright.setObjectName("page3_topright")
        self.gridLayout_4.addWidget(self.page3_topright, 0, 1, 1, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.page3_label = QtWidgets.QLabel(self.page_3)
        self.page3_label.setObjectName("page3_label")
        self.verticalLayout_4.addWidget(self.page3_label)
        self.page3_pushbutton_repopulate = QtWidgets.QPushButton(self.page_3)
        self.page3_pushbutton_repopulate.setObjectName("page3_pushbutton_repopulate")
        self.verticalLayout_4.addWidget(self.page3_pushbutton_repopulate)
        self.page3_pushbutton_makeplots = QtWidgets.QPushButton(self.page_3)
        self.page3_pushbutton_makeplots.setObjectName("page3_pushbutton_makeplots")
        self.verticalLayout_4.addWidget(self.page3_pushbutton_makeplots)
        self.page3_checkbox_laser_on = QtWidgets.QCheckBox(self.page_3)
        self.page3_checkbox_laser_on.setObjectName("page3_checkbox_laser_on")
        self.verticalLayout_4.addWidget(self.page3_checkbox_laser_on)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_10 = QtWidgets.QLabel(self.page_3)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_7.addWidget(self.label_10)
        self.combo_box_arb_var_x = QtWidgets.QComboBox(self.page_3)
        self.combo_box_arb_var_x.setObjectName("combo_box_arb_var_x")
        self.horizontalLayout_7.addWidget(self.combo_box_arb_var_x)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_8 = QtWidgets.QLabel(self.page_3)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_4.addWidget(self.label_8)
        self.combo_box_arb_var_y = QtWidgets.QComboBox(self.page_3)
        self.combo_box_arb_var_y.setObjectName("combo_box_arb_var_y")
        self.horizontalLayout_4.addWidget(self.combo_box_arb_var_y)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.gridLayout_4.addLayout(self.verticalLayout_4, 0, 0, 1, 1)
        self.page3_bottomright = QtWidgets.QWidget(self.page_3)
        self.page3_bottomright.setObjectName("page3_bottomright")
        self.gridLayout_4.addWidget(self.page3_bottomright, 1, 1, 1, 1)
        self.page3_bottomleft = QtWidgets.QLabel(self.page_3)
        self.page3_bottomleft.setObjectName("page3_bottomleft")
        self.gridLayout_4.addWidget(self.page3_bottomleft, 1, 0, 1, 1)
        self.gridLayout_4.setColumnStretch(0, 1)
        self.gridLayout_4.setColumnStretch(1, 2)
        self.gridLayout_5.addLayout(self.gridLayout_4, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.page_4)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(240, 170, 160, 80))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.page4_GLWidget = QtWidgets.QOpenGLWidget(self.gridLayoutWidget_2)
        self.page4_GLWidget.setObjectName("page4_GLWidget")
        self.gridLayout_7.addWidget(self.page4_GLWidget, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_4)
        self.horizontalLayout.addWidget(self.stackedWidget)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 880, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Commands"))
        self.open_file_button.setText(_translate("MainWindow", "Open File"))
        self.preprocess_file_checkbox.setText(_translate("MainWindow", "Preprocess files"))
        self.combo_box_select_page.setCurrentText(_translate("MainWindow", "Summary plots"))
        self.combo_box_select_page.setItemText(0, _translate("MainWindow", "Summary plots"))
        self.combo_box_select_page.setItemText(1, _translate("MainWindow", "Per toolpath plots"))
        self.combo_box_select_page.setItemText(2, _translate("MainWindow", "Arbitrary variable plotting"))
        self.combo_box_select_page.setItemText(3, _translate("MainWindow", "3D visualisation"))
        self.page1_label.setText(_translate("MainWindow", "Summary plots"))
        self.make_plots_button.setText(_translate("MainWindow", "Make plots"))
        self.plot_laser_on.setText(_translate("MainWindow", "Plot only when laser is on"))
        self.label_2.setText(_translate("MainWindow", "Rolling window seconds"))
        self.label_4.setText(_translate("MainWindow", "Per toolpath plots"))
        self.pushButton_make_toolpath_plots.setText(_translate("MainWindow", "Make toolpath plots"))
        self.page3_topright.setText(_translate("MainWindow", "TextLabel"))
        self.page3_label.setText(_translate("MainWindow", "Arbitrary var. plotting"))
        self.page3_pushbutton_repopulate.setText(_translate("MainWindow", "Repopulate variables"))
        self.page3_pushbutton_makeplots.setText(_translate("MainWindow", "Make arbitrary variable plots"))
        self.page3_checkbox_laser_on.setText(_translate("MainWindow", "Plot only when laser on"))
        self.label_10.setText(_translate("MainWindow", "X var"))
        self.label_8.setText(_translate("MainWindow", "Y var"))
        self.page3_bottomleft.setText(_translate("MainWindow", "TextLabel"))
