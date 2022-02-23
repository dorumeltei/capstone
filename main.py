import sys, json, ctypes
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.uic import loadUi
from pathlib import Path
import requests
# import wikipediaapi 

file_path = Path('config.json')
config_file = {}
user_data = {}
username = ""
first_init = True


# APIs
quote_url = "http://quotes.stormconsultancy.co.uk/random.json"
quote_response = requests.get(quote_url).json()

newsapi_key = 'ef6e6c998f0e4ba5925122cd3c9dca10'
newsapi_search_keywords = ['country=us', 'sources=bbc-news']
newsapi_url = (f'https://newsapi.org/v2/top-headlines?{newsapi_search_keywords[0]}&apiKey={newsapi_key}')
newsapi_response = requests.get(newsapi_url).json()
newsapi_data = newsapi_response["articles"]

if file_path.is_file():
    with open('config.json', 'r') as f:
        config_file = json.load(f)
        first_init = False
else:
    with open('config.json', 'w') as f:
        config_file['last_user'] = None
        json.dump(config_file, f)

class Page_Auto_Login(QDialog):
    # scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
    # user32 = ctypes.windll.user32
    # screen_w = user32.GetSystemMetrics(0)    
    # screen_h = user32.GetSystemMetrics(1) 
    set_width = 0
    set_height = 0
    
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
        global username
        page_main = Page_Main()
        widget.addWidget(page_main)
        username = config_file['last_user']  
        # widget.setFixedWidth(1000)
        # widget.setFixedHeight(2000)
        width = int(Page_Auto_Login.set_width / 5)
        height = Page_Auto_Login.set_height - 50
        x_pos = Page_Auto_Login.set_width - width
        y_pos = 45
        widget.setGeometry(x_pos, y_pos, width, height) 
        widget.setCurrentIndex(widget.currentIndex()+1)

class Page_Login(QDialog):
    def __init__(self):
        super(Page_Login, self).__init__()
        loadUi("login.ui", self)        
        self.btn_login.clicked.connect(self.login)
        self.input_pwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.btn_create_account.clicked.connect(self.goto_page_create_user)

    def login(self):
        global config_file, user_data, username        
        username = self.input_username.text()
        password = self.input_pwd.text()
        msg = QMessageBox()
        msg.setWindowTitle("Warning")
        msg.setIcon(QMessageBox.Warning)

        if username in config_file.keys() and config_file[username]["password"] == password:
            user_data = config_file[username]
            config_file['last_user'] = username
            Page_Auto_Login.goto_page_main(QDialog)
        else:
            msg.setText("Wrong username or password. Try again")
            msg.exec_()
            self.input_username.clear()
            self.input_pwd.clear()

    def goto_page_create_user(self):
        page_access = Page_Create_Account()
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
        global config_file        
        msg = QMessageBox()
        msg.setWindowTitle("Warning")
        msg.setIcon(QMessageBox.Warning)
        username = self.input_username.text()
        password = self.input_pwd.text()
        conf_pwd = self.input_confirm_pwd.text()
        if username in config_file.keys():
            msg.setText("Username exists! Try again.")
            msg.exec_()
        else:
            if username == "" or password == "":
                msg.setText("Username and password cannot be emtpy.")
                msg.exec_()
            elif len(password) < 5:
                msg.setText(
                    "Password too short. Chose a password with minimum 5 characters.")
                msg.exec_()
            elif password != conf_pwd:
                    msg.setText("Passwords do not match. Try again.")
                    msg.exec_()
            else:
                with open('config.json', 'r+') as f:
                    config_file = json.load(f)
                    config_file.update({username: {"password": password,
                        "auto_login": False}})
                    f.seek(0)  # reset file pointer to position 0
                    json.dump(config_file, f, indent=4)
                Page_Auto_Login.goto_page_login(QDialog)

class Page_Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Page_Main, self).__init__()
        loadUi("main.ui", self)  
        global user_data
        user_data = config_file[config_file['last_user']] 
        quote = f"Author: {quote_response['author']}\n{quote_response['quote']}"
        self.cb_auto_login.setChecked(user_data['auto_login'])
        self.cb_auto_login.clicked.connect(self.ch_box_auto_login)
        self.txt_browser_quotes.setText(quote)
        self.btn_refresh_quote.clicked.connect(self.get_quotes)

        self.lbl_news1.setText(newsapi_data[0]['title'])
        self.txt_news1.setText(f"{newsapi_data[0]['description']}\n <a href=\{newsapi_data[0]['url']}></a>")
        news_img1 = QImage()
        news_img1.loadFromData(requests.get(newsapi_data[0]['urlToImage']).content)
        self.lbl_news_img1.setScaledContents(True)
        self.lbl_news_img1.setPixmap(QPixmap(news_img1))

        self.lbl_news2.setText(newsapi_data[1]['title'])
        self.txt_news2.setText(f"{newsapi_data[1]['description']}\n <a href=\{newsapi_data[1]['url']}></a>")
        news_img2 = QImage()
        news_img2.loadFromData(requests.get(newsapi_data[1]['urlToImage']).content)
        self.lbl_news_img2.setScaledContents(True)
        self.lbl_news_img2.setPixmap(QPixmap(news_img2))

        self.lbl_news3.setText(newsapi_data[2]['title'])
        self.txt_news3.setText(f"{newsapi_data[2]['description']}\n <a href=\{newsapi_data[2]['url']}></a>")  
        news_img3 = QImage()
        news_img3.loadFromData(requests.get(newsapi_data[2]['urlToImage']).content)
        self.lbl_news_img3.setScaledContents(True)
        self.lbl_news_img3.setPixmap(QPixmap(news_img3))

        self.news_index = 3      
        self.btn_refresh_news.clicked.connect(self.refresh_news)

        widget.closeEvent = onClose

    ##Tab - Inspire
    def get_quotes(self):
        quote_response = requests.get(quote_url).json()
        quote = f"Author: {quote_response['author']}\n{quote_response['quote']}"
        self.txt_browser_quotes.setText(quote)


    def refresh_news(self):
        self.lbl_news1.setText(newsapi_data[self.news_index]['title'])
        self.txt_news1.setText(f"{newsapi_data[self.news_index]['description']}\n{newsapi_data[self.news_index]['url']}")
        news_img1 = QImage()
        news_img1.loadFromData(requests.get(newsapi_data[self.news_index]['urlToImage']).content)
        self.lbl_news_img1.setScaledContents(True)
        self.lbl_news_img1.setPixmap(QPixmap(news_img1))

        self.lbl_news2.setText(newsapi_data[self.news_index+1]['title'])
        self.txt_news2.setText(f"{newsapi_data[self.news_index+1]['description']}\n{newsapi_data[self.news_index+1]['url']}")
        news_img2 = QImage()
        news_img2.loadFromData(requests.get(newsapi_data[self.news_index+1]['urlToImage']).content)
        self.lbl_news_img2.setScaledContents(True)
        self.lbl_news_img2.setPixmap(QPixmap(news_img2))

        self.lbl_news3.setText(newsapi_data[self.news_index+2]['title'])
        self.txt_news3.setText(f"{newsapi_data[self.news_index+2]['description']}\n{newsapi_data[self.news_index+2]['url']}")   
        news_img3 = QImage()
        news_img3.loadFromData(requests.get(newsapi_data[self.news_index+2]['urlToImage']).content)
        self.lbl_news_img3.setScaledContents(True)
        self.lbl_news_img3.setPixmap(QPixmap(news_img3))

        self.news_index+=3
        


    ##Tab - Configuration
    def ch_box_auto_login(self, state):
        user_data['auto_login'] = state   
        

def onResize(event):
    size = event.size()
    page_w = size.width()
    page_h = size.height()
    # print(page_w, page_h)

def onMove(event):
    location = event.pos()
    page_x = location.x()
    page_y = location.y()
    # print(page_x, page_y)

def onClose(event):
    config_file[username] = user_data
    with open('config.json', 'w') as f:
        json.dump(config_file, f, indent=4)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dw = app.desktop()
    screen_width = dw.screenGeometry().width()
    screen_height = dw.availableGeometry().height()
    Page_Auto_Login.set_width = screen_width
    Page_Auto_Login.set_height = screen_height
    # mainwindow = Page_Main()
    last_user = config_file['last_user']
    if first_init == True:
        mainwindow = Page_Create_Account() 
    else:
        if config_file['last_user'] == None or config_file[last_user]['auto_login'] == False:
            mainwindow = Page_Login()
        else:
            mainwindow = Page_Auto_Login()
    widget=QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    # widget.setFixedWidth(480)
    # widget.setFixedHeight(620)
    widget.resize(480, 620)

    widget.setWindowTitle('Daily Digest')
    gui_icon = "config/img/icon.png"
    widget.setWindowIcon(QIcon(gui_icon))
    widget.resizeEvent = onResize
    widget.moveEvent = onMove  
    # print('object name', widget.objectName()) 
    # widget.closeEvent = onClose	 
    widget.show()
    app.exec_()