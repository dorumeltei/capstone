import sys, json
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from PyQt5.uic import loadUi
from pathlib import Path

file_path = Path('config.json')


data = {}

first_init = True

if file_path.is_file():
    with open('config.json', 'r') as f:        
        data = json.load(f)
        first_init = False        
else:
    with open ('config.json', 'w') as f:
        dict_start = dict()
        json.dump(dict_start, f)    

class Page_Auto_Login(QDialog):
    def __init__(self):
        super(Page_Auto_Login, self).__init__()
        loadUi("auto_login.ui", self)
        self.btn_confirm.accepted.connect(self.goto_page_main)
        self.btn_confirm.rejected.connect(self.goto_page_login)     
        

    def goto_page_login(self):
        page_login = Page_Login()
        widget.addWidget(page_login)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def goto_page_main(self):
        page_main = Page_Main()
        widget.addWidget(page_main)
        widget.setFixedWidth(1000)
        widget.setFixedHeight(2000)
        
        widget.setCurrentIndex(widget.currentIndex()+1)

class Page_Login(QDialog):            
    def __init__(self):
        super(Page_Login, self).__init__()
        loadUi("login.ui", self)
        self.btn_login.clicked.connect(self.login)
        self.input_pwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.btn_create_account.clicked.connect(self.goto_page_create_user)            

    def login(self):
        global data
        print(data)
        username = self.input_username.text()
        password = self.input_pwd.text()
        msg = QMessageBox()
        msg.setWindowTitle("Warning") 
        msg.setIcon(QMessageBox.Warning)
        
        if username in data.keys() and data[username]["password"] == password:              
            Page_Auto_Login.goto_page_main(QDialog) 
        else:
            msg.setText("Wrong username or password. Try again")
            msg.exec_()
            self.input_username.clear()
            self.input_pwd.clear()
            

    def goto_page_create_user(self):
        page_access=Page_Create_Account()
        widget.addWidget(page_access)
        widget.setCurrentIndex(widget.currentIndex()+1)

class Page_Create_Account(QDialog):
    def __init__(self):
        super(Page_Create_Account, self).__init__()
        loadUi("create_account.ui", self)
        self.btn_sign_up.clicked.connect(self.create_account)
        self.input_pwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.input_confirm_pwd.setEchoMode(QtWidgets.QLineEdit.Password)               

    def create_account(self):
        global data
        msg = QMessageBox()
        msg.setWindowTitle("Warning") 
        msg.setIcon(QMessageBox.Warning)
        username = self.input_username.text()
        password = self.input_pwd.text()
        conf_pwd = self.input_confirm_pwd.text()
        if username in data.keys():
            msg.setText("Username exists! Try again.")
            msg.exec_()
        else:
            if username == "" or password == "":
                msg.setText("Username and password cannot be emtpy.")
                msg.exec_()
            elif len(password) < 5:
                msg.setText("Password too short. Chose a password with minimum 5 characters.")
                msg.exec_()
            elif password != conf_pwd:
                    msg.setText("Passwords do not match. Try again.")
                    msg.exec_()
            else:   
                with open ('config.json', 'r+') as f:
                    data = json.load(f)
                    data.update({username:{"password": password, 
                        "auto_login": False}})
                    f.seek(0)   #reset file pointer to position 0
                    json.dump(data, f, indent=4)  
                Page_Auto_Login.goto_page_login(QDialog)

class Page_Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Page_Main, self).__init__()
        loadUi("main.ui", self)        

if __name__ == "__main__":
    app=QApplication(sys.argv)
    if first_init == True:
        mainwindow=Page_Create_Account() 
    else:
        mainwindow=Page_Auto_Login()
    widget=QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.setFixedWidth(480)
    widget.setFixedHeight(620)
    widget.show()
    app.exec_()