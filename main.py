import sys
from PyQt5 import QtWidgets
from mainwindow import MainWindow
from login_win import login_win
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    login_dialog = login_win()
    if login_dialog.exec_() == 1:
        login_info = login_dialog.get_login_info()
        myWin = MainWindow(login_info[0], '你好，%s' % login_info[1])
        myWin.show()
        sys.exit(app.exec_())

    else:
        app.quit()


# 将ui文件和qrc文件转化成py文件
# pyuic5 -o ui_mainwindow.py mainwindow.ui
# pyrcc5 -o resource_rc.py resource.qrc

# pyinstaller的使用方法
# pyinstaller -F main.py --noconsole
# pyinstaller -D main.py --noconsole

# 加在spec里面
# import sys
# sys.setrecursionlimit(5000)

# TODO LIST
# 图片加载速度优化
# 标签UI显示居中
