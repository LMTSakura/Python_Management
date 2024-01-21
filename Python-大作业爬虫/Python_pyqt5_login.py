#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Python-Classcode 
@File    ：Python_pyqt5_login.py
@IDE     ：PyCharm 
@Author  ：刘明焘
@Date    ：2023/12/23 16:36 
'''

import sys
import time
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from Python_pyqt5_index import Mywindow as index_ui


class MyWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = None
        self.init_ui()

    def init_ui(self):
        self.ui = uic.loadUi("./Python_ui_login.ui")
        # print(self.ui.__dict__)  # 查看ui文件中有哪些控件

        # 提取要操作的控件
        username_lineEdit = self.ui.username_lineEdit  # 用户名输入框
        password_lineEdit = self.ui.password_lineEdit  # 密码输入框
        login_pushButton = self.ui.login_pushButton  # 登录按钮
        register_pushButton = self.ui.register_pushButton  # 忘记密码按钮
        textBrowser = self.ui.textBrowser  # 文本显示区域

        # 绑定信号与槽函数
        self.login_pushButton.clicked.connect(self.login)

    def login(self):
        """登录按钮的槽函数"""
        user_name = self.username_lineEdit.text()
        password = self.password_lineEdit.text()
        if user_name == "1" and password == "1": # user_name == "admin" and password == "123456"
            self.textBrowser.setText("欢迎%s" % user_name)
            self.textBrowser.repaint()

            w = index_ui()
            w.ui.show()
        else:
            self.textBrowser.setText("用户名或密码错误....请重试")
            self.textBrowser.repaint()


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#
#     w = MyWindow()
#     # 展示窗口
#     w.ui.show()
#
#     app.exec()
