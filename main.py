import sys, json, ctypes
from PyQt5.QtCore import QUrl, QTimer, Qt
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5 import QtWidgets, QtWebEngineWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QLabel, QTextBrowser, QStyle
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.uic import loadUi

from pathlib import Path
import requests

file_path = Path('config.json')
config_file = {}
user_data = {}
first_init = True

if file_path.is_file():
    with open('config.json', 'r') as f:        
        config_file = json.load(f)
        first_init = False
else:
    with open('config.json', 'w') as f:
        config_file['last_user'] = None
        json.dump(config_file, f)

class Page_Auto_Login(QDialog):    
    # user ctypes to get the display sizes
    # scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
    # user32 = ctypes.windll.user32
    # screen_w = user32.GetSystemMetrics(0)    
    # screen_h = user32.GetSystemMetrics(1) 
    set_width = 0
    set_height = 0
    
    def __init__(self):
        super(Page_Auto_Login, self).__init__()
        loadUi("auto_login.ui", self)
        
        self.last_user = config_file['last_user']
        self.user_data = config_file[self.last_user]        
        self.lbl_last_user.setText(f'as: {self.last_user}')
        self.btn_confirm.accepted.connect(self.goto_page_main)
        self.btn_confirm.rejected.connect(self.goto_page_login)
        self.btn_window_close.clicked.connect(lambda x:save_data_on_close())
        
    def goto_page_login(self):
        page_login = Page_Login()
        widget.addWidget(page_login)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def goto_page_main(self):
        page_main = Page_Main()
        widget.addWidget(page_main)
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
        # global config_file     
        get_username = self.input_username.text()
        get_password = self.input_pwd.text()
        msg = QMessageBox()
        msg.setWindowTitle("Warning")
        msg.setIcon(QMessageBox.Warning)

        if get_username in config_file.keys() and config_file[get_username]["password"] == get_password:
            self.user_data = config_file[get_username]
            config_file['last_user'] = get_username
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

        if username == "" or password == "":
            msg.setText("Username and password cannot be emtpy.")
            msg.exec_()
        elif username in config_file.keys():
            msg.setText("Username exists! Try again.")
            msg.exec_()
        elif len(password) < 5:
            msg.setText("Password too short. Chose a password with minimum 5 characters.")
            msg.exec_()
        elif password != conf_pwd:
            msg.setText("Passwords do not match. Try again.")
            msg.exec_()
        else:
            with open('config.json', 'r+') as f:
                config_file = json.load(f)
                config_file.update({username: {"password": password,
                    "auto_login": False, "default_tab": 0, "apikey_news":"", "apikey_quotes":"", "apikey_jokes":"", "apikey_memes":"", "apikey_humor":"", "apikey_radio":"",}})
                f.seek(0)  # reset file pointer to position 0
                json.dump(config_file, f, indent=4)
            Page_Auto_Login.goto_page_login(QDialog)


class Page_Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Page_Main, self).__init__()
        loadUi("digest.ui", self) 
        global user_data
        self.user_data = config_file[config_file['last_user']]

        # Tab Configuration
        auto_login = self.user_data['auto_login'] 
        default_tab = self.user_data['default_tab'] 
        apikey_news = self.user_data['apikey_news'] 
        apikey_quotes = self.user_data['apikey_quotes'] 
        apikey_jokes = self.user_data['apikey_jokes'] 
        apikey_memes = self.user_data['apikey_memes'] 
        apikey_humor = self.user_data['apikey_humor'] 
        apikey_radio = self.user_data['apikey_radio'] 
        
        self.cb_auto_login.setChecked(auto_login)
        
        self.tabWidget.setCurrentIndex(default_tab)
        self.cb_start_tab.setCurrentIndex(default_tab)
        self.btn_conf_save.clicked.connect(self.save_conf_data) 

        self.api_key_news.setText(apikey_news)
        self.api_key_quotes.setText(apikey_quotes)
        self.api_key_jokes.setText(apikey_jokes)
        self.api_key_memes.setText(apikey_memes)
        self.api_key_humor.setText(apikey_humor)
        self.api_key_radio.setText(apikey_radio)

        self.news_index = 0 
        self.btn_refresh_news.clicked.connect(self.get_news)
        self.btn_refresh_quote.clicked.connect(self.get_quotes)
        self.btn_refresh_jokes.clicked.connect(self.get_jokes) 
        self.btn_refresh_memes.clicked.connect(self.get_memes) 
        self.btn_refresh_humor.clicked.connect(self.get_humor) 

        '''
        radio_url = "https://radio-world-50-000-radios-stations.p.rapidapi.com/v1/radios/getTopByCountry"
        radio_querystring = {"query":"tr"}
        radio_headers = {
            'x-rapidapi-host': "radio-world-50-000-radios-stations.p.rapidapi.com",
            'x-rapidapi-key': self.user_data['apikey_radio']
            }
        radioapi_response = requests.get(radio_url, headers=radio_headers, params=radio_querystring).json()'''

        radio_url = "https://scdn.nrjaudio.fm/fr/30607/mp3_128.mp3?origine=mytuner&aw_0_1st.station=Nostalgie-Funk&cdn_path=adswizz_lbs12&adws_out_b1&access_token=538457b5aa0f4d6cbc8a05a67a6b22b3"
        
        self.radio_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.radio_player.setMedia(QMediaContent(QUrl(radio_url)))
        self.btn_radio_play.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.btn_radio_play.clicked.connect(self.play_radio)

        live_stream1 = 'https://www.youtube.com/embed/BHACKCNDMW8?autoplay=1&mute=0&controls=0&rel=0'
        self.video_stream1.load(QUrl(live_stream1))

        live_stream2 = 'https://www.youtube.com/embed/77YwsoKsNV8?autoplay=1&mute=0&controls=0&rel=0'
        self.video_stream2.load(QUrl(live_stream2))
       
        self.delay_load = QTimer()
        self.delay_load.start(3000)
        self.delay_load.timeout.connect(self.load_all_apis)

        # widget.closeEvent = onClose
        
        user_data = self.user_data
        self.btn_window_close.clicked.connect(lambda x:save_data_on_close())  

    def save_conf_data(self):
        self.user_data['auto_login'] = self.cb_auto_login.isChecked()
        self.user_data['default_tab'] =  self.cb_start_tab.currentIndex()
        self.user_data['apikey_news'] = self.api_key_news.text()
        self.user_data['apikey_quotes'] = self.api_key_quotes.text()
        self.user_data['apikey_jokes']  = self.api_key_jokes.text()
        self.user_data['apikey_memes']  = self.api_key_memes.text()
        self.user_data['apikey_humor'] = self.api_key_humor.text()
        self.user_data['apikey_radio'] = self.api_key_radio.text()

        config_file[config_file['last_user']] = user_data
        if user_data:
            with open('config.json', 'w') as f:
                json.dump(config_file, f, indent=4)

    ##Tab - News
    def get_news(self):
        print('starting getting content')
        newsapi_search_keywords = ['country=us', 'sources=bbc-news']
        newsapi_url = (f"https://newsapi.org/v2/top-headlines?{newsapi_search_keywords[0]}&apiKey={self.user_data['apikey_news']}")

        newsapi_response = requests.get(newsapi_url)
        if newsapi_response.status_code == 200:
            newsapi_response = newsapi_response.json()
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
        else:
            print('News feed limit reached')

    ##Tab - Inspire
    def get_quotes(self):
        quote_url = "http://quotes.stormconsultancy.co.uk/random.json"
        quote_response = requests.get(quote_url).json()
        quote = f"Author: {quote_response['author']}\n{quote_response['quote']}"
        self.txt_browser_quotes.setText(quote) 

    ##Tab - Entertain
    # 1 - Jokes
    def get_jokes(self):
        jokesapi_url = "https://humor-jokes-and-memes.p.rapidapi.com/jokes/random"
        jokesapi_querystring = {"api-key":"undefined","max-length":"200","include-tags":"one_liner","min-rating":"7","exclude-tags":"nsfw","keywords":"rocket"}
        jokesapi_headers = {
            'x-rapidapi-host': "humor-jokes-and-memes.p.rapidapi.com",
            'x-rapidapi-key': "self.user_data['apikey_jokes']"
            }
        jokesapi_response = requests.get(jokesapi_url, headers=jokesapi_headers, params=jokesapi_querystring).json()
        try:
            jokesapi_data = jokesapi_response['joke']
            self.txt_jokes.setText(jokesapi_data)
        except:
            self.txt_jokes.setText('Jokes reached maxium per day')

    # 2 - Memes
    def get_memes(self):
        memesapi_url = "https://humor-jokes-and-memes.p.rapidapi.com/memes/random"
        memesapi_querystring = {"api-key":"undefined","number":"3","media-type":"image","keywords-in-image":"true","min-rating":"7"}
        memesapi_headers = {
            'x-rapidapi-host': "humor-jokes-and-memes.p.rapidapi.com",
            'x-rapidapi-key': "self.user_data['apikey_memes']"
            }
        memesapi_response = requests.get(memesapi_url, headers=memesapi_headers, params=memesapi_querystring).json()
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
        base_url = 'https://api.humorapi.com/'
        jokes_url = 'jokes/random?'
        # memes_url = 'memes/random?'
        humorapi_url = f"{base_url}{jokes_url}api-key={self.user_data['apikey_humor']}"
        # meme_url = 'https://api.humorapi.com/memes/random?keywords=rocket'
        humorapi_response = requests.get(humorapi_url).json()
        try:
            humorapi_data = humorapi_response['joke']
            self.txt_humor.setText(humorapi_data)
        except:
            self.txt_humor.setText("Humor reached maximum per day")

    # 4 - Radio
    def play_radio(self):     
        if self.radio_player.state() == self.radio_player.PlayingState:
            self.radio_player.pause()
            self.btn_radio_play.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        else:
            self.radio_player.play() 
            self.btn_radio_play.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
    
    def load_all_apis(self):
        self.delay_load.stop()
        self.get_news()
        self.get_quotes()
        self.get_jokes()
        self.get_memes()
        self.get_humor()

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

# def onClose(event):
#     save_data_on_close()

def save_data_on_close():
    sys.exit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dw = app.desktop()
    screen_width = dw.screenGeometry().width()
    screen_height = dw.availableGeometry().height()
    Page_Auto_Login.set_width = screen_width
    Page_Auto_Login.set_height = screen_height
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
    widget.setWindowFlags(Qt.FramelessWindowHint) 
    widget.setStyleSheet("border-radius: 20px;\n"
    "background-color: transparent; \n")
    # app.setStyle("fusion")
    widget.show()
    app.exec_()