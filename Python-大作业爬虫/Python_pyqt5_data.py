#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：Python-Classcode 
@File    ：Python_pyqt5_data.py
@IDE     ：PyCharm 
@Author  ：刘明焘
@Date    ：2023/12/27 8:52 
'''
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtDataVisualization import Q3DBars, QBar3DSeries, QBarDataItem, Q3DCamera

if __name__ == '__main__':
    app = QApplication(sys.argv)

    bars = Q3DBars()
    bars.setFlags(bars.flags() ^ Qt.FramelessWindowHint)
    bars.rowAxis().setRange(0, 4)
    series = QBar3DSeries()
    data = []
    data.append(QBarDataItem(1.0))
    data.append(QBarDataItem(3.0))
    data.append(QBarDataItem(7.5))
    data.append(QBarDataItem(5.0))
    data.append(QBarDataItem(2.2))
    series.dataProxy().addRow(data)
    bars.addSeries(series)

    # 调整相机位置，更好的角度来观察柱状图
    camera = bars.scene().activeCamera()
    camera.setCameraPreset(Q3DCamera.CameraPresetIsometricRight)

    bars.setTitle('实战 Qt for Python: 3D柱状图演示')
    bars.resize(480, 360)
    bars.show()

    sys.exit(app.exec())