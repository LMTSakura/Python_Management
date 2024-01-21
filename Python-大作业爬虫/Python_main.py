# import Python_request
import csv
import sys
import time
import pymysql
import mysql.connector
from collections import namedtuple
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QPixmap
from PyQt5 import uic
from PyQt5.QtDataVisualization import Q3DBars, QBar3DSeries, QBarDataItem, Q3DCamera


# from PyQt5.QtCore import QCoreApplication
# from Python_pyqt5_login import MyWindow as login_ui
# from Python_pyqt5_index import Mywindow as index_ui
#将因版本问题产生的警告排除
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

'''
@Project ：Python-Classcode 
@File    ：Python_main.py
@IDE     ：PyCharm 
@Author  ：刘明焘
@Date    ：2023/12/21 8:46 
'''
#192.168.254.73 宿舍
#192.168.1.121 317
#192.168.254.73 数媒
#192.168.1.114 Java
#192.168.1.128 317
#id SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY id设为主键且从1开始依次递增

class db_connect:
    # 获取连接
    def __init__(self):
        try:
            self.sqldb = mysql.connector.connect(
                host="localhost",  # 数据库主机名称
                user="root",  # 数据库用户名
                passwd="root",  # 数据库密码
                port=3306, # 端口
                database="db_csv" # 数据库名称
            )
            print("连接成功！")
            print()
        except:
            print("连接失败！")
            print()
        self.sqlcursor = self.sqldb.cursor() # 创建一个游标

    def find_any(self, sql): # 找多个数据
        self.sqlcursor.execute(sql)
        result = self.sqlcursor.fetchall()
        return result
    def find_one(self, sql): # 找单个数据
        self.sqlcursor.execute(sql)
        result = self.sqlcursor.fetchone()
        return result
    def delete_one(self, sql): #删除单个数据
        self.sqlcursor.execute(sql)
        result = self.sqlcursor.fetchone()
        return result
    def insert_one(self, sql): #插入单个数据
        self.sqlcursor.execute(sql)
        result = self.sqlcursor.fetchone()
        return result
    def execute(self, sql): # 数据库执行
        try:
            self.sqlcursor.execute(sql)
            self.sqldb.commit() # 提交执行
            print("数据库操作成功！")
            return 1
        except:
            self.sqldb.rollback()
            print("发生错误数据信息回滚！")
            return 0
    def close_db(self):
        self.sqlcursor.close() # 关闭创建的游标
        self.sqldb.close() # 关闭数据库

def CSV_SQL(): #数据库初始化操作
    sql_conn = pymysql.connect(host='192.168.1.128', port=3306, user='root',
                               password='root', db='db_csv', charset='utf8', connect_timeout=1000)
    cursor = sql_conn.cursor()
    sql_1 = 'CREATE TABLE IF NOT EXISTS `csv_test` (`id` SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,`card_name` VARCHAR ( 80 ),`cards_unit` VARCHAR ( 80 ),`price` VARCHAR ( 80 ), ' \
            '`original_price` VARCHAR ( 80 ),`href_url` TEXT ( 21845 ),`img_url` TEXT ( 21845 ))'
    sql_2 = 'CREATE TABLE IF NOT EXISTS `csv_admin` (`uid` SMALLINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,`username` VARCHAR ( 80 ),`password` VARCHAR (80)) '
    #网站数据表建表操作
    if cursor.execute(sql_1):
        print("执行成功，网站数据录入完成")
    else:
        print("执行失败，数据表已存在")
    sql_conn.commit()  # 提交到数据库
    #用户表建表操作
    if cursor.execute(sql_2):
        print("执行成功，用户数据录入完成")
    else:
        print("执行失败，用户表已存在")
    file_name = '汽车之家.csv'
    # 将CSV文件中的数据插入MySQL数据表中
    SQL_FORMAT = 'insert into csv_test (card_name, cards_unit, price, original_price, href_url, img_url) values(%s, %s, %s, %s, %s, %s)'
    sql_conn.autocommit(1)
    for t in get_data(file_name):
        print(t.card_name, " ", t.cards_unit, " ", t.price, " ", t.original_price, " ", t.href_url, " ", t.img_url)
        if cursor.execute(SQL_FORMAT, (t.card_name, t.cards_unit, t.price, t.original_price, t.href_url, t.img_url)):
            print("执行插入成功")
        else:
            print("执行插入失败")
    sql_conn.commit()  # 提交到数据库
    sql_conn.close()  # 关闭数据库服务

def get_data(file_name):
    with open(file_name,encoding='utf-8') as f:
        f_csv = csv.reader(f)
        headings = next(f_csv)
        Row = namedtuple('Row', headings)
        for r in f_csv:
            yield Row(*r)

class pylogin(QWidget):

    def __init__(self):
        super().__init__()
        # self.ui = None
        self.ui = uic.loadUi("./Python_ui_login.ui")
        self.init_ui()

    def init_ui(self):
        # self.ui = uic.loadUi("./Python_ui_login.ui")
        # print(self.ui.__dict__)  # 查看ui文件中有哪些控件

        # 提取要操作的控件
        self.username_lineEdit = self.ui.username_lineEdit  # 用户名输入框
        self.password_lineEdit = self.ui.password_lineEdit  # 密码输入框
        self.login_pushButton = self.ui.login_pushButton  # 登录按钮
        self.register_pushButton = self.ui.register_pushButton  # 忘记密码按钮
        self.textBrowser = self.ui.textBrowser  # 文本显示区域

        # 绑定信号与槽函数
        self.login_pushButton.clicked.connect(self.login)
        self.register_pushButton.clicked.connect(self.register)
        # 设置密码掩码字符显示
        self.password_lineEdit.setEchoMode(QLineEdit.Password)
        # 设置用户名和密码提示输入
        self.username_lineEdit.setPlaceholderText("             请输入用户名")
        self.password_lineEdit.setPlaceholderText("             请输入密码")
        # 设置登录与退出的icon
        self.login_pushButton.setIcon(QIcon(QPixmap('用户登录.png')))
        self.register_pushButton.setIcon(QIcon(QPixmap('用户注册.png')))
    def login(self):
        """登录按钮的槽函数"""
        username = self.username_lineEdit.text()
        password = self.password_lineEdit.text()

        # "SELECT * FROM admin_login WHERE username = '%s'" % self.count.get()


        if username == "123456" and password == "123456": # user_name == "admin" and password == "123456"
            self.textBrowser.setText("欢迎%s" % username)
            self.textBrowser.repaint()
            time.sleep(2)
            self.ui.close()
            a.ui.show()
        else:
            self.textBrowser.setText("用户名或密码错误....请重试")
            self.textBrowser.repaint()

    def register(self):
        """注册按钮的槽函数"""
        self.ui.close()
        b.ui.show()

class pyregister(QWidget):

    def __init__(self):
        super().__init__()
        # self.ui = None
        self.ui = uic.loadUi("./Python_ui_register.ui")
        self.init_ui()

    def init_ui(self):
        self.username_lineEdit = self.ui.username_lineEdit  # 用户名输入框
        self.password_lineEdit = self.ui.password_lineEdit  # 密码输入框
        self.yes_pushButton = self.ui.yes_pushButton  # 确认按钮
        self.goback_pushButton = self.ui.goback_pushButton  # 确认按钮
        self.textBrowser = self.ui.textBrowser  # 文本显示区域

        # 给查询按钮绑定槽函数
        self.yes_pushButton.clicked.connect(self.register)
        self.goback_pushButton.clicked.connect(self.goback)
        # 设置用户名和密码提示输入
        self.username_lineEdit.setPlaceholderText("             请输入用户名")
        self.password_lineEdit.setPlaceholderText("             请输入密码")

    def register(self):
        mydb = db_connect()
        username = str(self.username_lineEdit.text())
        password = str(self.password_lineEdit.text())
        rename = mydb.find_one("SELECT * FROM csv_admin WHERE username = '%s'" % username)
        SQL_FORMAT = 'insert into csv_admin (username, password) values(%s, %s)' % (username,password)
        if username == "" or password == "":
            self.textBrowser.setText("注册失败，注册信息不完整，请重试")
        elif rename:
            self.textBrowser.setText("注册失败，该账户已经被注册过，请重试")
        else:
            if mydb.execute(SQL_FORMAT):
                self.textBrowser.setText("注册成功，欢迎%s" % username)
                self.textBrowser.repaint()
                time.sleep(2)
                self.ui.close()
                w.ui.show()
            else:
                self.textBrowser.setText("数据库连接有问题，注册失败，请重试")
                self.textBrowser.repaint()
        mydb.close_db()

    def goback(self):
        self.ui.close()
        w.ui.show()

class pyindex(QWidget):

    def __init__(self):
        super().__init__()
        # self.ui = None
        self.ui = uic.loadUi("./Python_ui_index.ui")

        # 数据的临时存储列表
        self.list_card_id = ""
        self.list_card_name = ""
        self.list_cards_unit = ""
        self.list_card_price = ""
        self.list_sum = []
        self.count_x = 0
        self.count_y = 4

        self.init_ui()

    def init_ui(self):
        # self.ui = uic.loadUi("./Python_ui_index.ui")
        print(self.ui) # .ui文件中最顶层的对象(From)
        print(self.ui.__dict__) # 最顶层对象的所有属性(key:value方式显示)
        print(self.ui.card_info_tableView) # 最顶层对象中嵌套的Qtable
        print(self.ui.card_name_label.text()) # 最顶层对象中嵌套的Qlable的文本

        # self.card_info_verticalScrollBar = self.ui.card_info_verticalScrollBar
        self.card_info_tableView = self.ui.card_info_tableView
        # self.carad_name_label = self.ui.card_name_label
        self.card_name_lineEdit = self.ui.card_name_lineEdit
        # self.cards_unit_label = self.ui.cards_unit_label
        self.cards_unit_lineEdit = self.ui.cards_unit_lineEdit
        # self.dead_Line = self.ui.dead_Line
        # self.img_label = self.ui.img_label
        # self.price_label = self.ui.price_label
        self.price_lineEdit = self.ui.price_lineEdit
        self.price_lineEdit_2 = self.ui.price_lineEdit_2
        self.progressBar = self.ui.progressBar
        self.findout_pushButton = self.ui.findout_pushButton
        self.display_pushButton = self.ui.display_pushButton
        self.goback_pushButton = self.ui.goback_pushButton

        # 给查询按钮绑定槽函数
        self.findout_pushButton.clicked.connect(self.findout)
        self.display_pushButton.clicked.connect(self.qt_datavision_1)

        # 设置各项条件提示输入
        self.card_name_lineEdit.setPlaceholderText("             请输入二手车品牌名称")
        self.cards_unit_lineEdit.setPlaceholderText("             请输入二手车交易地址")
        self.price_lineEdit.setPlaceholderText(" 请输入最小范围")
        self.price_lineEdit_2.setPlaceholderText(" 请输入最大范围")

        # 设置进度条最大长度与最小长度
        min = self.progressBar.setMinimum(0)  # 设置进度条的最小值
        max = self.progressBar.setMaximum(100)  # 设置进度条的最大值
        # 设置进度条加载走向（从左到右）
        self.progressBar.setInvertedAppearance(False)

        # 设置进度条当前值
        self.progressBar.setValue(100)

        # 设置QListView的属性
        # self.listModel = QStringListModel()
        # self.list = ["列表项1", "列表项2", "列表项3"]
        # self.listModel.setStringList(self.list)
        # self.card_nifo_listView.setModel(self.listModel)

        # 设置QTableView的属性
        self.card_info_tableView.verticalHeader().setVisible(True)  # 垂直标题栏可见
        self.card_info_tableView.horizontalHeader().setVisible(True)  # 水平标题栏可见
        self.card_info_tableView.horizontalHeader().setFixedHeight(30) # 设置表格标题栏的高度
        self.card_info_tableView.horizontalHeader().setStyleSheet("QHeaderView::section{background:#eafef9;}")  # 垂直标题栏背景色为灰色 设置表格标题栏的背景色

        self.model = QStandardItemModel(8000, 4) # 设置显示模式表格中的行和列
        self.card_info_tableView.setModel(self.model) # 设置显示模式

        self.column_name = ['ID', '品牌', '地址', '价格'] # 设置标题名称
        self.model.setHorizontalHeaderLabels(self.column_name)

        # 设置行列填满窗口
        self.card_info_tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 使表宽度自适应
        self.card_info_tableView.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 使表高度自适应

        # 设置表格不可编辑
        # self.card_info_tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # 设置表格参考线为可见
        self.card_info_tableView.setShowGrid(True)

    def qt_datavision_1(self):
        print(self.count_x)
        # bars = Q3DBars()
        bars.setFlags(bars.flags() ^ Qt.FramelessWindowHint)
        bars.rowAxis().setRange(0, 4)
        series = QBar3DSeries()
        data = []
        data.append(QBarDataItem(10))
        data.append(QBarDataItem(30))
        data.append(QBarDataItem(70))
        data.append(QBarDataItem(50))
        data.append(QBarDataItem(22))
        data.append(QBarDataItem())
        series.dataProxy().addRow(data)
        bars.addSeries(series)

        # 调整相机位置，更好的角度来观察柱状图
        camera = bars.scene().activeCamera()
        camera.setCameraPreset(Q3DCamera.CameraPresetIsometricRight)

        bars.setTitle('二手车价格图')
        bars.resize(1000, 800)
        bars.show()


    def findout(self):
        """实现查询的逻辑"""
        self.model.clear()
        self.model = QStandardItemModel(8000, 4)  # 设置显示模式表格中的行和列
        self.card_info_tableView.setModel(self.model)  # 设置显示模式
        self.column_name = ['ID', '品牌', '地址', '价格']  # 设置标题名称
        self.model.setHorizontalHeaderLabels(self.column_name)

        #数据的临时存储列表
        self.list_card_id = ""
        self.list_card_name = ""
        self.list_cards_unit = ""
        self.list_card_price = ""
        self.list_sum = []
        self.count_x = 0
        self.count_y = 4

        mydb = db_connect()

        card_name = self.card_name_lineEdit.text()
        cards_unit = self.cards_unit_lineEdit.text()
        card_price = self.price_lineEdit.text()
        card_price_2 = self.price_lineEdit_2.text()
        if  card_price_2 == '' or card_price == '':
            card_price = 0.00
            card_price_2 = 99999999999.00
        elif float(card_price) > float(card_price_2):
            card_price = 0.00
            card_price_2 = 0.00
            print("无此数据")
        else:
            card_price = float(card_price)
            card_price_2 = float(card_price_2)
        sql_check = "SELECT * from csv_test where card_name like '%%%s%%' and cards_unit like '%%%s%%' and price between '%f' and '%f'" % (card_name, cards_unit, card_price, card_price_2) # 名称
        # sql_check_name = "SELECT * from csv_test where card_name like '%%%s%%'" % card_name # 名称
        # sql_check_unit = "SELECT * from csv_test where cards_unit like '%%%s%%'" % cards_unit # 地区
        print("正在查询。。。。。。")
        results = mydb.find_any(sql_check)
        if results:
            print(results)
            print("查询完毕")
            card_price = 0.00
            card_price_2 = 0.00
        else:
            print("无此数据")
            card_price = 0.00
            card_price_2 = 0.00
            self.list_sum = []
            self.model.clear()
            self.model = QStandardItemModel(8000, 4)  # 设置显示模式表格中的行和列
            self.card_info_tableView.setModel(self.model)  # 设置显示模式
            self.column_name = ['ID', '品牌', '地址', '价格']  # 设置标题名称
            self.model.setHorizontalHeaderLabels(self.column_name)
        # results_name = mydb.find_any(sql_check_name)
        # results_unit = mydb.find_any(sql_check_unit)
        # print(results_name)
        # print(type(results_name))
        print()
        # print(results_unit)
        # print(type(results_unit))
        # print(card_name)
        # print(cards_unit)
        # print(card_price)
        for i in results:
            # list_new = list(i)
            self.list_card = []
            self.list_card_id = str(i[0])
            print(self.list_card_id)
            print(type(self.list_card_id))
            self.list_card_name = str(i[1])
            print(self.list_card_name)
            self.list_cards_unit = str(i[2])
            print(self.list_cards_unit)
            self.list_card_price = str(i[3])
            print(self.list_card_price)
            print()
            self.list_card.append(self.list_card_id)
            self.list_card.append(self.list_card_name)
            self.list_card.append(self.list_cards_unit)
            self.list_card.append(self.list_card_price)
            print(self.list_card)

            self.list_sum.append(self.list_card)
            # print()
            self.count_x = self.count_x + 1
        print(self.list_sum)
        print(self.count_x)

        count_begin = 0
        # 设置进度条最大长度与最小长度
        min = self.progressBar.setMinimum(0)  # 设置进度条的最小值
        max = self.progressBar.setMaximum(self.count_x)  # 设置进度条的最大值
        # 设置进度条加载走向（从左到右）
        self.progressBar.setInvertedAppearance(False)
        # 设置进度条当前值
        self.progressBar.setValue(0)

        for i in range(self.count_x):
            count_begin = count_begin + 1
            # 设置进度条当前值
            self.progressBar.setValue(count_begin)
            for j in range(self.count_y):
                user_info = QStandardItem(self.list_sum[i][j])
                self.model.setItem(i, j, user_info)
                user_info.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        # self.list = results
        # self.listModel.setStringList(list(self.list))
        # self.card_nifo_listView.setModel(self.listModel)

if __name__ == '__main__':
    # Python_request.py_requests()
    # CSV_SQL()
    app = QApplication(sys.argv)
    w = pylogin()
    a = pyindex()
    b = pyregister()
    bars = Q3DBars()
    w.ui.setWindowTitle("二手车信息查询系统")
    w.ui.setWindowIcon(QIcon("./二手车图片.png"))
    a.ui.setWindowTitle("二手车信息查询系统")
    a.ui.setWindowIcon(QIcon("./二手车图片.png"))
    b.ui.setWindowTitle("二手车信息查询系统")
    b.ui.setWindowIcon(QIcon("./二手车图片.png"))
    w.ui.show()
    # w = pyindex()
    # w.ui.show()
    app.exec()
