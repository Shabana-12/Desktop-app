from os import name
import sys
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from PyQt5.uic import loadUi
import MySQLdb as mdb


class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.gotocreate)

    def loginfunction(self):
        try:
            email = self.email.text()
            password = self.password.text()
            db = mdb.connect('localhost', 'root', '', 'pyqt5')
            cur = db.cursor()
            cur.execute('SELECT * FROM userdata WHERE email= %s AND password = %s', (email, password,))
            result = cur.fetchone()
            if result==None:
                QMessageBox.about(self, 'Login', 'Incorrect Email/Password')
                # self.labelResult.setText("Incorrect Email/Password")
            else:
                QMessageBox.about(self, 'Login', "You are logged in successfully!")
                
                # self.labelResult.setText("You are logged in successfully!")
        except mdb.Error as e:
            QMessageBox.about(self, 'Login', "Sorry! something went wrong")
            # self.labelResult.setText("Error! something went wrong")
           

    def gotocreate(self):
        createacc = CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)


class CreateAcc(QDialog):
    def __init__(self):
        super(CreateAcc, self).__init__()
        loadUi("createacc.ui", self)
        self.signupbutton.clicked.connect(self.createaccfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)

    def createaccfunction(self):
        try:
            email = self.email.text()
            name = self.name.text()
            password=self.password.text()
            db = mdb.connect('localhost', 'root', '', 'pyqt5')
            cur = db.cursor()
            cur.execute('SELECT * FROM userdata WHERE email= %s', (email, ))
            result = cur.fetchone()
            if result:
                QMessageBox.about(self, 'register', 'Account already exist!')
            elif self.password.text() == self.confirmpass.text():
        
                db = mdb.connect('localhost', 'root', '', 'pyqt5')
                cur = db.cursor()
                cur.execute("INSERT INTO userdata(name,  email, password) VALUES(%s, %s, %s)",
                           (name, email, password,))
                db.commit()
                QMessageBox.about(self, 'Register', 'You have registered successfully!')
                login = Login()
                widget.addWidget(login)
                widget.setCurrentIndex(widget.currentIndex()+1)
                # self.labelResult.setText("Incorrect Email/Password")
            else:
                QMessageBox.about(self, 'Register', "Please fill out the form properly!")
                
                # self.labelResult.setText("You are logged in successfully!")
        except mdb.Error as e:
            QMessageBox.about(self, 'Register', "Sorry! something went wrong")
            


app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(480)
widget.setFixedHeight(620)
widget.show()
app.exec_()
