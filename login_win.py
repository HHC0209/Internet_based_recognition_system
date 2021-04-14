from Ui_login_win import Ui_Dialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.Qt import *
import pymysql
import data_manip
from ERRORS import EXECUTE_FAILURE, UPDATE_FAILURE, INSERT_FAILURE, NETWORK_ERR





class login_win(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        QtWidgets.QApplication.setStyle('Fusion')  # ui风格为Fusion
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 无标题栏
        self.bnt_minimize.clicked.connect(self.showMinimized)
        self.bnt_close.clicked.connect(self.close)
        self.btn_login.clicked.connect(self.verify)
        self.led_userName.cursorPositionChanged.connect(self.clear_error_hint)
        self.led_passwd.cursorPositionChanged.connect(self.clear_error_hint)

    # 拖动窗口
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def verify(self):
        try:
            data_manip.check_network()
        except NETWORK_ERR as ne:
            QMessageBox.critical(self, "错误", ne.__str__())
            return
        userName = self.led_userName.text()
        passwd = self.led_passwd.text()
        if not userName:
            self.lab_error_hint_1.setText("<font color='red'>   请输入用户名！" )
        elif not passwd:
            self.lab_error_hint_2.setText("<font color='red'>   请输入密码！")
        elif self.isAdministrator(userName,passwd):
            QDialog.accept(self)
        elif data_manip.check_psw(userName,passwd):
            QDialog.accept(self)
        else:
            self.lab_error_hint_2.setText("<font color='red'> 用户名或者密码错误，请检查！")


    def get_login_info(self):
        #判断是管理员还是辅导员，管理员0，辅导员1
        if self.isAdministrator(self.led_userName.text(),self.led_passwd.text()):
            return (0, self.led_userName.text())
        else:
            return (1,self.led_userName.text())


    def clear_error_hint(self, lab_err_hint):
        self.lab_error_hint_1.clear()
        self.lab_error_hint_2.clear()
    

    '''
    判断是否为管理员，暂时指定管理员的账号名为admin，密码为123456
    '''
    def isAdministrator(self,name,password):
        if name=="admin" and password=="123456":
            return 1
        return 0



