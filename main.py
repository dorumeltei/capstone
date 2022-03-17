import sys, json, ctypes
from PyQt5.QtCore import QUrl, QTimer, Qt
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QLabel, QTextBrowser, QStyle
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtMultimediaWidgets import QVideoWidget
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
# Quotes
quote_url = "http://quotes.stormconsultancy.co.uk/random.json"

newsapi_key = 'ef6e6c998f0e4ba5925122cd3c9dca10'
newsapi_search_keywords = ['country=us', 'sources=bbc-news']
newsapi_url = (f'https://newsapi.org/v2/top-headlines?{newsapi_search_keywords[0]}&apiKey={newsapi_key}')

# Jokes
jokesapi_url = "https://humor-jokes-and-memes.p.rapidapi.com/jokes/random"
jokesapi_querystring = {"api-key":"undefined","max-length":"200","include-tags":"one_liner","min-rating":"7","exclude-tags":"nsfw","keywords":"rocket"}
jokesapi_headers = {
    'x-rapidapi-host': "humor-jokes-and-memes.p.rapidapi.com",
    'x-rapidapi-key': "09119aef4cmshd3b58d3da340673p186437jsnf4c8854db8d4"
    }

# Memes
memesapi_url = "https://humor-jokes-and-memes.p.rapidapi.com/memes/random"
memesapi_querystring = {"api-key":"undefined","number":"3","media-type":"image","keywords-in-image":"true","min-rating":"7"}
memesapi_headers = {
    'x-rapidapi-host': "humor-jokes-and-memes.p.rapidapi.com",
    'x-rapidapi-key': "09119aef4cmshd3b58d3da340673p186437jsnf4c8854db8d4"
    }

# Humor
base_url = 'https://api.humorapi.com/'
jokes_url = 'jokes/random?'
memes_url = 'memes/random?'
humorapi_key = '7d3031ae95c2424a8629e4e75575bce3'
humorapi_url = f"{base_url}{jokes_url}api-key={humorapi_key}"
# meme_url = 'https://api.humorapi.com/memes/random?keywords=rocket'

# Radio
radio_url = "https://radio-world-50-000-radios-stations.p.rapidapi.com/v1/radios/getTopByCountry"
radio_querystring = {"query":"tr"}
radio_headers = {
    'x-rapidapi-host': "radio-world-50-000-radios-stations.p.rapidapi.com",
    'x-rapidapi-key': "09119aef4cmshd3b58d3da340673p186437jsnf4c8854db8d4"
    }
radioapi_response = requests.get(radio_url, headers=radio_headers, params=radio_querystring).json()


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
        self.btn_window_close.clicked.connect(lambda x:save_data_on_close())
        
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
        self.btn_window_close.clicked.connect(lambda x:save_data_on_close())
        

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
        self.btn_window_close.clicked.connect(lambda x:save_data_on_close())

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
                        "auto_login": False, "default_tab": 0}})
                    f.seek(0)  # reset file pointer to position 0
                    json.dump(config_file, f, indent=4)
                Page_Auto_Login.goto_page_login(QDialog)

class Page_Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Page_Main, self).__init__()
        loadUi("digest.ui", self)  
        global user_data
        user_data = config_file[config_file['last_user']] 
        tab_index = user_data['default_tab']
        self.tabWidget.setCurrentIndex(tab_index)

        # Tab Configuration
        self.cb_auto_login.setChecked(2)
        self.cb_auto_login.clicked.connect(self.ch_box_auto_login)
        self.cb_start_tab.setCurrentIndex(tab_index)
        self.cb_start_tab.currentIndexChanged.connect(self.change_start_tab)

        self.btn_refresh_news.clicked.connect(self.get_news)
        self.news_index = 0 
        # self.get_news()
        
        self.txt_browser_quotes.setText('')
        self.btn_refresh_quote.clicked.connect(self.get_quotes) 
        # self.get_quotes()

        self.txt_jokes.setText('')
        self.btn_refresh_jokes.clicked.connect(self.get_jokes)        
        # self.get_jokes()
        
        self.lbl_img_memes.setText('')
        self.btn_refresh_memes.clicked.connect(self.get_memes)        
        # self.get_memes()

        self.txt_humor.setText('')
        self.btn_refresh_humor.clicked.connect(self.get_humor)        
        # self.get_humor()
        
        radio_url = "https://scdn.nrjaudio.fm/fr/30607/mp3_128.mp3?origine=mytuner&aw_0_1st.station=Nostalgie-Funk&cdn_path=adswizz_lbs12&adws_out_b1&access_token=538457b5aa0f4d6cbc8a05a67a6b22b3"
        
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setMedia(QMediaContent(QUrl(radio_url)))
        # videoWidget = QVideoWidget()
        self.btn_radio_play.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.btn_radio_play.clicked.connect(self.play)










        live_cam1_stream = 'https://www.youtube.com/watch?v=48MFrf5ADp8'

        self.mediaPlayer2 = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer2.setMedia(QMediaContent(QUrl(live_cam1_stream)))
        videoWidget = QVideoWidget()
        # self.btn_radio_play.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        # self.btn_radio_play.clicked.connect(self.play)
        # self.video_cam2.setPixmap((videoWidget)
        self.mediaPlayer2.play() 









        

        self.delay_load = QTimer()
        self.delay_load.start(3000)
        self.delay_load.timeout.connect(self.load_all_apis)

        widget.closeEvent = onClose
        self.btn_window_close.clicked.connect(lambda x:save_data_on_close())  

    ##Tab - News
    def get_news(self):
        print('starting getting news')
        newsapi_response = requests.get(newsapi_url).json()
        newsapi_data = newsapi_response["articles"]
        no_of_rows = 3                
        for row in range(0, no_of_rows):
            lbl_title = self.findChild(QLabel, f'lbl_news_title_{row}')
            lbl_title.setText(newsapi_data[self.news_index]['title'])
            txt_body = self.findChild(QTextBrowser, f'txt_body_{row}')
            txt_body.setOpenExternalLinks(True)
            txt_body.setText(f"{newsapi_data[self.news_index]['description']} <a href={newsapi_data[self.news_index]['url']} target=\"_blank\">link</a>")
            try:
                img = QImage()   
                img.loadFromData(requests.get(newsapi_data[self.news_index]['urlToImage']).content)
                lbl_img = self.findChild(QLabel, f'img_news_{row}')
                lbl_img.setScaledContents(True)
                lbl_img.setPixmap(QPixmap(img))
            except:
                lbl_img = QLabel()
                lbl_img.setText("Memes reached maximum per day")
            self.news_index +=1

    ##Tab - Inspire
    def get_quotes(self):
        quote_response = requests.get(quote_url).json()
        quote = f"Author: {quote_response['author']}\n{quote_response['quote']}"
        self.txt_browser_quotes.setText(quote) 

    ##Tab - Entertain
    # 1 - Jokes
    def get_jokes(self):
        jokesapi_response = requests.get(jokesapi_url, headers=jokesapi_headers, params=jokesapi_querystring).json()
        try:
            jokesapi_data = jokesapi_response['joke']
            self.txt_jokes.setText(jokesapi_data)
        except:
            self.txt_jokes.setText('Jokes reached maxium per day')

    # 2 - Memes
    def get_memes(self):
        memesapi_response = requests.get(memesapi_url, headers=memesapi_headers, params=memesapi_querystring).json()
        # memesapi_data = 'https://preview.redd.it/mtavie3t4kr31.jpg?width=640&crop=smart&auto=webp&s=77a0e2e7bbe6ec68f2343d7b11081af2cf60a55f'
        try:
            memesapi_data = memesapi_response['url']
            img_memes = QImage()  
            img_memes.loadFromData(requests.get(memesapi_data).content) 
            self.lbl_img_memes.setScaledContents(True)
            self.lbl_img_memes.setPixmap(QPixmap(img_memes))
        except:
            self.lbl_img_memes.setText("Memes reached maximum per day")

    # 3 - Humor
    def get_humor(self):
        humorapi_response = requests.get(humorapi_url).json()
        try:
            humorapi_data = humorapi_response['joke']
            self.txt_humor.setText(humorapi_data)
        except:
            self.txt_humor.setText("Humor reached maximum per day")

    # 4 - Radio
    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            self.btn_radio_play.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        else:
            self.btn_radio_play.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            self.mediaPlayer.play() 
    
    def load_all_apis(self):
        self.delay_load.stop()
        # self.get_news()
        # self.get_quotes()
        # self.get_jokes()
        # self.get_memes()
        # self.get_humor()

    ##Tab - Configuration
    def ch_box_auto_login(self, state):
        user_data['auto_login'] = state   

    def change_start_tab(self, value):
        user_data['default_tab'] = value 
        

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
    save_data_on_close()

def save_data_on_close():
    config_file[username] = user_data
    with open('config.json', 'w') as f:
        json.dump(config_file, f, indent=4)
    sys.exit()

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
    widget.setWindowFlags(Qt.FramelessWindowHint) 
    widget.show()
    app.exec_()