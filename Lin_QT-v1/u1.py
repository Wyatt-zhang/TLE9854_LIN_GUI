# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'u1.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1401, 953)
        self.groupBox_connect = QtWidgets.QGroupBox(Form)
        self.groupBox_connect.setGeometry(QtCore.QRect(20, 40, 1361, 111))
        self.groupBox_connect.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.groupBox_connect.setObjectName("groupBox_connect")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.groupBox_connect)
        self.horizontalLayout_8.setContentsMargins(18, 18, 18, 18)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_hardware = QtWidgets.QLabel(self.groupBox_connect)
        self.label_hardware.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_hardware.setObjectName("label_hardware")
        self.horizontalLayout.addWidget(self.label_hardware)
        self.cbBox_hardware = QtWidgets.QComboBox(self.groupBox_connect)
        self.cbBox_hardware.setSizeIncrement(QtCore.QSize(2, 2))
        self.cbBox_hardware.setIconSize(QtCore.QSize(35, 36))
        self.cbBox_hardware.setObjectName("cbBox_hardware")
        self.cbBox_hardware.addItem("")
        self.horizontalLayout.addWidget(self.cbBox_hardware)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout_8.addLayout(self.horizontalLayout)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.pushBtn_refresh = QtWidgets.QPushButton(self.groupBox_connect)
        self.pushBtn_refresh.setObjectName("pushBtn_refresh")
        self.horizontalLayout_7.addWidget(self.pushBtn_refresh)
        self.horizontalLayout_8.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_mode = QtWidgets.QLabel(self.groupBox_connect)
        self.label_mode.setEnabled(True)
        self.label_mode.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_mode.setObjectName("label_mode")
        self.horizontalLayout_5.addWidget(self.label_mode)
        self.cbBox_mode = QtWidgets.QComboBox(self.groupBox_connect)
        self.cbBox_mode.setEnabled(True)
        self.cbBox_mode.setObjectName("cbBox_mode")
        self.cbBox_mode.addItem("")
        self.horizontalLayout_5.addWidget(self.cbBox_mode)
        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_5.setStretch(1, 1)
        self.horizontalLayout_8.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.horizontalLayout_6.setSpacing(12)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_buadrate = QtWidgets.QLabel(self.groupBox_connect)
        self.label_buadrate.setEnabled(True)
        self.label_buadrate.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_buadrate.setObjectName("label_buadrate")
        self.horizontalLayout_6.addWidget(self.label_buadrate)
        self.cbBox_buadrate = QtWidgets.QComboBox(self.groupBox_connect)
        self.cbBox_buadrate.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbBox_buadrate.sizePolicy().hasHeightForWidth())
        self.cbBox_buadrate.setSizePolicy(sizePolicy)
        self.cbBox_buadrate.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.cbBox_buadrate.setAutoFillBackground(False)
        self.cbBox_buadrate.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContentsOnFirstShow)
        self.cbBox_buadrate.setIconSize(QtCore.QSize(36, 32))
        self.cbBox_buadrate.setObjectName("cbBox_buadrate")
        self.cbBox_buadrate.addItem("")
        self.cbBox_buadrate.addItem("")
        self.cbBox_buadrate.addItem("")
        self.cbBox_buadrate.addItem("")
        self.horizontalLayout_6.addWidget(self.cbBox_buadrate)
        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 1)
        self.horizontalLayout_8.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushBtn_disconnect = QtWidgets.QPushButton(self.groupBox_connect)
        self.pushBtn_disconnect.setEnabled(False)
        self.pushBtn_disconnect.setFlat(False)
        self.pushBtn_disconnect.setObjectName("pushBtn_disconnect")
        self.horizontalLayout_4.addWidget(self.pushBtn_disconnect)
        self.pushBtn_connect = QtWidgets.QPushButton(self.groupBox_connect)
        self.pushBtn_connect.setEnabled(True)
        self.pushBtn_connect.setObjectName("pushBtn_connect")
        self.horizontalLayout_4.addWidget(self.pushBtn_connect)
        self.horizontalLayout_8.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_8.setStretch(0, 4)
        self.horizontalLayout_8.setStretch(1, 1)
        self.horizontalLayout_8.setStretch(2, 2)
        self.horizontalLayout_8.setStretch(3, 2)
        self.horizontalLayout_8.setStretch(4, 2)
        self.groupBox_Action = QtWidgets.QGroupBox(Form)
        self.groupBox_Action.setEnabled(False)
        self.groupBox_Action.setGeometry(QtCore.QRect(10, 200, 1351, 92))
        self.groupBox_Action.setObjectName("groupBox_Action")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_Action)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.radioBtn_nocmd = QtWidgets.QRadioButton(self.groupBox_Action)
        self.radioBtn_nocmd.setObjectName("radioBtn_nocmd")
        self.horizontalLayout_3.addWidget(self.radioBtn_nocmd)
        self.radioBtn_manualup = QtWidgets.QRadioButton(self.groupBox_Action)
        self.radioBtn_manualup.setObjectName("radioBtn_manualup")
        self.horizontalLayout_3.addWidget(self.radioBtn_manualup)
        self.radioBtn_manualdown = QtWidgets.QRadioButton(self.groupBox_Action)
        self.radioBtn_manualdown.setObjectName("radioBtn_manualdown")
        self.horizontalLayout_3.addWidget(self.radioBtn_manualdown)
        self.radioBtn_autoup = QtWidgets.QRadioButton(self.groupBox_Action)
        self.radioBtn_autoup.setObjectName("radioBtn_autoup")
        self.horizontalLayout_3.addWidget(self.radioBtn_autoup)
        self.radioBtn_autodown = QtWidgets.QRadioButton(self.groupBox_Action)
        self.radioBtn_autodown.setObjectName("radioBtn_autodown")
        self.horizontalLayout_3.addWidget(self.radioBtn_autodown)
        self.horizontalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 320, 1231, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.HLayout_Readmsg = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.HLayout_Readmsg.setContentsMargins(0, 0, 0, 0)
        self.HLayout_Readmsg.setObjectName("HLayout_Readmsg")
        self.pushBtn_showmsg = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushBtn_showmsg.setObjectName("pushBtn_showmsg")
        self.HLayout_Readmsg.addWidget(self.pushBtn_showmsg)
        self.pushBtn_Linread = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushBtn_Linread.setObjectName("pushBtn_Linread")
        self.HLayout_Readmsg.addWidget(self.pushBtn_Linread)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.HLayout_Readmsg.addItem(spacerItem)
        self.HLayout_Readmsg.setStretch(0, 1)
        self.HLayout_Readmsg.setStretch(1, 1)
        self.HLayout_Readmsg.setStretch(2, 4)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(40, 430, 1261, 491))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.HLayout_showpic = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.HLayout_showpic.setContentsMargins(0, 0, 0, 0)
        self.HLayout_showpic.setObjectName("HLayout_showpic")

        self.retranslateUi(Form)
        self.pushBtn_connect.clicked['bool'].connect(self.groupBox_Action.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Mosfet_tool"))
        self.groupBox_connect.setTitle(_translate("Form", "Connection"))
        self.label_hardware.setText(_translate("Form", "Hardware:"))
        self.cbBox_hardware.setItemText(0, _translate("Form", "No Hardware Found"))
        self.pushBtn_refresh.setText(_translate("Form", "Refresh"))
        self.label_mode.setText(_translate("Form", "Mode:"))
        self.cbBox_mode.setItemText(0, _translate("Form", "Master"))
        self.label_buadrate.setText(_translate("Form", "Buadrate:"))
        self.cbBox_buadrate.setItemText(0, _translate("Form", "2400"))
        self.cbBox_buadrate.setItemText(1, _translate("Form", "9600"))
        self.cbBox_buadrate.setItemText(2, _translate("Form", "10400"))
        self.cbBox_buadrate.setItemText(3, _translate("Form", "19200"))
        self.pushBtn_disconnect.setText(_translate("Form", "Disconnect"))
        self.pushBtn_connect.setText(_translate("Form", "Connect"))
        self.groupBox_Action.setTitle(_translate("Form", "Window Control"))
        self.radioBtn_nocmd.setText(_translate("Form", "NoCMD"))
        self.radioBtn_manualup.setText(_translate("Form", "Manual Up"))
        self.radioBtn_manualdown.setText(_translate("Form", "Manual Down"))
        self.radioBtn_autoup.setText(_translate("Form", "Auto Up"))
        self.radioBtn_autodown.setText(_translate("Form", "Auto Down"))
        self.pushBtn_showmsg.setText(_translate("Form", "show received msg"))
        self.pushBtn_Linread.setText(_translate("Form", "sent read lin cmd"))