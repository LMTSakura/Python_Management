#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Python-Classcode 
@File    ：Python_pyqt5_index.py
@IDE     ：PyCharm 
@Author  ：刘明焘
@Date    ：2023/12/22 13:42 
'''

import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic


# 旋钮案例

# class MyWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.init_ui()
#
#     def init_ui(self):
#         # 更改当前Widge的宽高
#         self.resize(500, 300)
#         # 创建一个按钮
#         btn = QPushButton("点我点我", self)
#         # 设置窗口位置、宽高
#         btn.setGeometry(200, 200, 100, 30)
#         # 将按钮被点击时触发的信号与我们定义的函数（方法）进行绑定
#         # 注意：这里没有()，即写函数的名字，而不是名字()
#         btn.clicked.connect(self.click_my_btn)
#
#         dial = QDial(self)
#         dial.setRange(30, 150)  # 设置范围
#         dial.setNotchesVisible(True)  # 设置刻度
#         dial.setPageStep(20)  # 翻页步长
#         dial.setWrapping(True)  # 刻度不留缺口
#         dial.setNotchTarget(50)  # 设置刻度密度，即单位刻度所代表的大小
#
#
#     def click_my_btn(self, arg):
#         # 槽函数，点击按钮则调用该函数
#         # 这里的参数正好是信号发出，传递的参数
#         print("点击按钮啦~", arg)
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     w = MyWindow()
#     w.show()
#     app.exec()

class Mywindow(QWidget):

    def __init__(self):
        super().__init__()
        self.ui = None
        self.init_ui()

    def init_ui(self):
        self.ui = uic.loadUi("./Python_ui_index.ui")
        print(self.ui) # .ui文件中最顶层的对象(From)
        print(self.ui.__dict__) # 最顶层对象的所有属性(key:value方式显示)
        print(self.ui.card_nifo_listView) # 最顶层对象中嵌套的QList
        print(self.ui.card_name_label.text()) # 最顶层对象中嵌套的Qlable的文本

        card_info_verticalScrollBar = self.ui.card_info_verticalScrollBar
        card_nifo_listView = self.ui.card_nifo_listView
        carad_name_label = self.ui.card_name_label
        carad_name_linEdit = self.ui.card_name_lineEdit
        cards_unit_label = self.ui.cards_unit_label
        cards_unit_lineEdit = self.ui.cards_unit_lineEdit
        dead_Line = self.ui.dead_Line
        img_label = self.ui.img_label
        price_label = self.ui.price_label
        price_lineEdit = self.ui.price_lineEdit
        progressBar = self.ui.progressBar
        findout_pushButton = self.ui.findout_pushButton

        #给查询按钮绑定槽函数
        findout_pushButton.clicked.connect(self.findout)

    def findout(self):
        """实现查询的逻辑"""
        print("正在查询。。。。。。")

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#
#     w = Mywindow()
#     #展示窗口
#     w.ui.show()
#
#     # ui = uic.loadUi("./untitled.ui")
#     # 展示窗口
#     # ui.show()
#
#     app.exec()
