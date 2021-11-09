# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reconnaissance_des_images.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import math
import numpy as np
import matplotlib.pyplot as plt
import sklearn.tree as tree 
import cv2
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QTextEdit
from PyQt5.QtGui import QPixmap


# DB_img(path,extension,a) c'est une fonction qui retourne une liste des paths des images qui vont être utilisées pendant l'apprentissage
def DB_img(path,extension,a):
    lst = np.array([])
    for i in range(1,a):
        full_path = path+str(i)+extension
        lst = np.append(lst,full_path)  
    return lst

# img_reading(path,extension,a) une fonction qui retourne une liste des photos qui sont transformées 
def img_reading(path,extension,a):
    db_img = DB_img(path,extension,a)
    lst_img = np.array([])
    for i in range(db_img.size):
        image_flatten = transformation(db_img[i])
        lst_img = np.append(lst_img,image_flatten)    
    return lst_img
# transformation(path_image) retourne une matrice des données qui correspond à une image transformée en gray puis en binaire et enfin flatten
def transformation(path_image):
    image = cv2.imread(path_image)
    image_gray =  cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, image_bin = cv2.threshold(image_gray, 175, 255, cv2.THRESH_BINARY) 
    image_flatten = image_bin.flatten()
    return image_flatten
# **************************************************************************************** 
def score_fct(D,D_reslt):
    score = 0
    for i in range(D.shape[0]):
        if D_reslt[i] == D[i]: score += 1
    score = (score*100)/D.shape[0]   
    return score

def partie_app():
    a = 63
    D = np.array([])
    D = np.append(D,[(1,1,1,1,1,2,2,2,3,3,4,4,5,5,5,6,6,7,7,8,8,9,9,9,9,9,10,10,
    11,11,12,12,13,13,14,14,15,15,15,16,16,17,17,18,18,19,19,20,20,21,21,21,22,22,23,23,24,24,25,25,26,26)])
    D = np.reshape(D,(a-1,1))

    path = "C:/Users/yas_f/Downloads/TAD/TP_3/images/apprentissage/"
    extension = ".png"
    lst = img_reading(path,extension,a)
    lst = np.reshape(lst,(a-1,2500))
    return lst , D , a

def partie_test():
    path = "C:/Users/yas_f/Downloads/TAD/TP_3/images/TEST/"
    extension = ".png"
    a = 42

    D = np.array([])
    D = np.append(D,[(1,1,2,2,3,3,4,4,5,5,6,6,7,8,8,9,9,10,10,11,12,13,13,14,14,15,15,16,16,17,18,19,19,20,21,21,
    22,23,24,25,26)])
    D = np.reshape(D,(a-1,1))

    lst = img_reading(path,extension,a)
    lst = np.reshape(lst,(a-1,2500))
    return lst , D , a

def app_DTC():
    lst , D , a = partie_app()
    cl = tree.DecisionTreeClassifier(criterion="entropy",min_impurity_decrease=0.007,ccp_alpha=0.009,max_leaf_nodes=50000)

    depart_time = time.time()
    cl.fit(lst,D)
    finish_time = time.time()
    tmpE = finish_time - depart_time

    D_reslt = np.array([])
    for i in range(lst.shape[0]):
        v_test = cl.predict(lst[i].reshape(1, -1))
        D_reslt = np.append(D_reslt,v_test)
    D_reslt = np.reshape(D_reslt,(a-1,1))

    score_appr = score_fct(D,D_reslt)

    lst , D , a = partie_test()
    D_reslt = np.array([])
    for i in range(lst.shape[0]):
        v_test = cl.predict(lst[i].reshape(1, -1))
        D_reslt = np.append(D_reslt,v_test)
    D_reslt = np.reshape(D_reslt,(a-1,1))

    score_test = score_fct(D,D_reslt)
    return tmpE,score_appr,score_test,cl

def app_ETC():
    lst , D , a = partie_app()
    cl = tree.ExtraTreeClassifier(criterion="gini",splitter="random",max_depth=5000,min_impurity_decrease=0.005)

    depart_time = time.time()
    cl.fit(lst,D)
    finish_time = time.time()
    tmpE = finish_time - depart_time

    D_reslt = np.array([])
    for i in range(lst.shape[0]):
        v_test = cl.predict(lst[i].reshape(1, -1))
        D_reslt = np.append(D_reslt,v_test)
    D_reslt = np.reshape(D_reslt,(a-1,1))

    score_appr = score_fct(D,D_reslt)

    lst , D , a = partie_test()
    D_reslt = np.array([])
    for i in range(lst.shape[0]):
        v_test = cl.predict(lst[i].reshape(1, -1))
        D_reslt = np.append(D_reslt,v_test)
    D_reslt = np.reshape(D_reslt,(a-1,1))

    score_test = score_fct(D,D_reslt)
    return tmpE,score_appr,score_test,cl

DecisionTree = app_DTC()
ExtraTree = app_ETC()

# class Ui_MainWindow(object):
#     path_test = ""
#     def setupUi(self, MainWindow):
#         MainWindow.setObjectName("MainWindow")
#         MainWindow.resize(800, 600)
#         self.centralwidget = QtWidgets.QWidget(MainWindow)
#         self.centralwidget.setObjectName("centralwidget")
#         self.getImage = QtWidgets.QPushButton(self.centralwidget)
#         self.getImage.setGeometry(QtCore.QRect(260, 150, 111, 41))
#         self.getImage.setObjectName("getImage")
#         self.getImage.clicked.connect(self.fct_getimage)
#         self.ETC = QtWidgets.QPushButton(self.centralwidget)
#         self.ETC.setGeometry(QtCore.QRect(560, 150, 111, 41))
#         self.ETC.setObjectName("ETC")
#         self.ETC.clicked.connect(self.ETClass)
#         self.DTC = QtWidgets.QPushButton(self.centralwidget)
#         self.DTC.setGeometry(QtCore.QRect(410, 150, 111, 41))
#         self.DTC.setObjectName("DTC")
#         self.DTC.clicked.connect(self.DTClass)
#         self.Comp = QtWidgets.QPushButton(self.centralwidget)
#         self.Comp.setGeometry(QtCore.QRect(110, 150, 111, 41))
#         self.Comp.setObjectName("Comp")
#         self.Comp.clicked.connect(self.Comparaison)
#         self.label = QtWidgets.QLabel(self.centralwidget)
#         self.label.setGeometry(QtCore.QRect(234, 40, 321, 41))
#         font = QtGui.QFont()
#         font.setFamily("Rockwell")
#         font.setPointSize(15)
#         font.setItalic(True)
#         font.setUnderline(False)
#         font.setStrikeOut(False)
#         font.setKerning(True)
#         self.label.setFont(font)
#         self.label.setObjectName("label")
#         self.results = QtWidgets.QLabel(self.centralwidget)
#         self.results.setGeometry(QtCore.QRect(110, 480, 561, 41))
#         font = QtGui.QFont()
#         font.setPointSize(9)
#         font.setBold(True)
#         font.setWeight(75)
#         self.results.setFont(font)
#         self.results.setText("")
#         self.results.setObjectName("results")
#         self.lettre = QtWidgets.QLabel(self.centralwidget)
#         self.lettre.setGeometry(QtCore.QRect(220, 209, 341, 241))
#         self.lettre.setText("")
#         self.lettre.setObjectName("lettre")
#         MainWindow.setCentralWidget(self.centralwidget)
#         self.menubar = QtWidgets.QMenuBar(MainWindow)
#         self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
#         self.menubar.setObjectName("menubar")
#         MainWindow.setMenuBar(self.menubar)
#         self.statusbar = QtWidgets.QStatusBar(MainWindow)
#         self.statusbar.setObjectName("statusbar")
#         MainWindow.setStatusBar(self.statusbar)

#         self.retranslateUi(MainWindow)
#         QtCore.QMetaObject.connectSlotsByName(MainWindow)

#     def retranslateUi(self, MainWindow):
#         _translate = QtCore.QCoreApplication.translate
#         MainWindow.setWindowTitle(_translate("MainWindow", "Reconnaissance des images"))
#         self.getImage.setText(_translate("MainWindow", "Choisir une image"))
#         self.ETC.setText(_translate("MainWindow", "ETC"))
#         self.DTC.setText(_translate("MainWindow", "DTC"))
#         self.Comp.setText(_translate("MainWindow", "Comparaison"))
#         self.label.setText(_translate("MainWindow", " Les Arbres des décisions"))
    
#     # fct_getimage(self) va retourner l'image choisi et l'affiché sur l'interface avec le resultat du fonction predict
#     def fct_getimage(self):
#         filename = QFileDialog.getOpenFileName()
#         Ui_MainWindow.path = filename[0]
#         self.path_test = filename[0]
#         self.lettre.setPixmap(QtGui.QPixmap(Ui_MainWindow.path).scaled(300, 300, QtCore.Qt.KeepAspectRatio))
#     # Decision Tree Classifier
#     def DTClass(self):
#         if self.path_test == "" : self.results.setText("ERREUR : il faut choisir une image")
#         else :
#             test_sample = transformation(self.path_test)
#             v_test = DecisionTree[3].predict(test_sample.reshape(1, -1))
#             lettre = chr(ord('@')+int(v_test))
#             self.results.setText("le caractère que vous aves choisi est : "+lettre)
#     # Comparaison des deux classifieurs Decision tree classifier & Extra Tree classifier
#     def Comparaison(self):
print("--------------------------------------------------------------------------------------")
print("DecisionTree :")
print( "Temps d'execution: ",round(DecisionTree[0]*100,3),"ms")
print("Précision de la classification sur l'apprentissage:" ,round(DecisionTree[1],2),"%")
print("Précision de la classification sur le test:" ,round(DecisionTree[2],3),"%")
print("--------------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------------")
print("ExtraTree :")
print( "Temps d'execution: ",round(ExtraTree[0]*100,3),"ms")
print("Précision de la classification sur l'apprentissage:" ,round(ExtraTree[1],2),"%")
print("Précision de la classification sur le test:" ,round(ExtraTree[2],3),"%")
print("--------------------------------------------------------------------------------------")  

    
    
    
    
    
    # Extra Tree Classifier 
    # def ETClass(self):
    #     if self.path_test == "" : self.results.setText("ERREUR : il faut choisir une image")
    #     else :
    #         test_sample = transformation(self.path_test)
    #         v_test = ExtraTree[3].predict(test_sample.reshape(1, -1))
    #         lettre = chr(ord('@')+int(v_test))
    #         self.results.setText("le caractère que vous aves choisi est : "+lettre)


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())