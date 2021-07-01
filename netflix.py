from os import name
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox,QLabel,QComboBox
from PyQt5.uic import loadUi
import MySQLdb as mdb
from PyQt5.QtGui import QPixmap



class Login(QDialog):
    def __init__(self):
       
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.loginbutton.clicked.connect(self.loginfunction)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createaccbutton.clicked.connect(self.gotocreate)

    def loginfunction(self):
        try:
            name = self.name.text()
            password = self.password.text()
            db = mdb.connect('localhost', 'root', 'pass@1New', 'pyqt5')
            cur = db.cursor()
            cur.execute(
                'SELECT * FROM userdata WHERE name= %s AND password = %s', (name, password,))
            result = cur.fetchone()
            if result == None:
                QMessageBox.about(self, 'Login', 'Incorrect Email/Password')
                # self.labelResult.setText("Incorrect Email/Password")
            else:
                QMessageBox.about(
                    self, 'Login',  "You are logged in successfully!")

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
        self.loginbutton.clicked.connect(self.gotologin)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpass.setEchoMode(QtWidgets.QLineEdit.Password)

    def createaccfunction(self):
        try:
            email = self.email.text()
            name = self.name.text()
            password = self.password.text()
            phone = self.phone.text()
            dob = self.dob.text()
            gender = self.gender.currentText()
           
     
            db=mdb.connect('localhost', 'root', 'pass@1New', 'pyqt5')
            cur=db.cursor()
            cur.execute('SELECT * FROM userdata WHERE email= %s or name=%s', (email,name, ))
            result=cur.fetchone()
            if result:
                QMessageBox.about(self, 'register', 'Account already exist!')
            elif not name or not password or not email or not dob:
                QMessageBox.about(self, 'Register',
                                  'Please fill out the form properly !')
            elif self.password.text() == self.confirmpass.text():

                db=mdb.connect('localhost', 'root', 'pass@1New', 'pyqt5')
                cur=db.cursor()
                cur.execute("INSERT INTO userdata(name,  email, password,phone,dob,gender) VALUES(%s, %s, %s,%s,%s,%s)",
                           (name, email, password, phone, dob,gender))
                db.commit()
                QMessageBox.about(self, 'Register',
                                  'You have registered successfully!')
                login=Login()
                widget.addWidget(login)
                widget.setCurrentIndex(widget.currentIndex()+1)
                # self.labelResult.setText("Incorrect Email/Password")
            else:
                QMessageBox.about(self, 'Register',
                                  "your passwords didn't match!")

                # self.labelResult.setText("You are logged in successfully!")
        except mdb.Error as e:
            QMessageBox.about(self, 'Register', "Sorry! something went wrong")

    def gotologin(self):
        login=Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)


app=QApplication(sys.argv)
mainwindow=Login()

widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setStyleSheet("QDialog{\n"
"background-image:url(bgg.jpg)\n"
"}")
widget.setFixedWidth(750)
widget.setFixedHeight(750)
widget.show()
app.exec_()
