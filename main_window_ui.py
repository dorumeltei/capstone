from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QTimer as timer
from datetime import datetime as dt, timedelta
import Start, Sources, Access, Config, Test1, Test2
import json, ctypes, time
from itertools import cycle


from PyQt5.QtCore import QEvent


##start import of custom modules
import Email, weather

scaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
page_x_offset = 1
if scaleFactor == 100:
	page_y_offset = 31
elif scaleFactor == 125:
	page_y_offset = 38
elif scaleFactor == 150:
	page_y_offset = 45
elif scaleFactor == 175:
	page_y_offset = 52

###Update clock & date on labels
cur_time = None
def Update_Time():
	global cur_time


	local_time = dt.now()
	utc_time = dt.utcnow()
	weather_offset_time = utc_time + timedelta(seconds = weather.offset)
	
	cur_time = dt.strftime(local_time, '{}  %a, {}'.format(datetime_time_format, datetime_date_format)) #%d-%m-%Y, %d-%b-%y, %b-%d-%Y
	date = dt.strftime(weather_offset_time, '%a, {}'.format(datetime_date_format))
	time = dt.strftime(weather_offset_time, '{}'.format(datetime_time_format)) 

	Gui_Start.lbl_Date.setText(date)
	Gui_Start.lbl_Time.setText(time)
	Gui_Sources.lbl_DateTime.setText(cur_time)
	Gui_Access.lbl_DateTime.setText(cur_time)
	Gui_Config.lbl_DateTime.setText(cur_time)


####Widgets control
with open('config/config.json', 'r') as data_file:	
	try:
		config_data = json.load(data_file)
		accounts = config_data['accounts']
		welcome_msg = config_data['welcome_msg']
		default_theme = config_data['default_theme']
		custom_theme = config_data['custom_theme']
		page_format = config_data['page_format']
		my_email = config_data['my_email']
		my_datetime = config_data['my_datetime']
		my_weather = config_data['my_weather']
	except:
		accounts = {'doru':'2070',
					'manic':'chinad',
					'prem':'secret',
					'mathi':'pwd'
					}
		welcome_msg = ''
		default_theme = 'blue'
		custom_theme = {'BkndColor': 'rgb(0, 173, 210)', 
						'FontSize': '10',
						'FontType': 'MS Shell Dlg 2',
						'FontColor': 'white'
						}
		page_format = {'page_w': 653,
						'page_h': 466,
						'page_x': 100,
						'page_y': 50
						}
		my_email = {'receiver': None, 
					'username': None,
					'password': None,
					'subject': 'Warning - AV System',
					'message':'Warning message',
					'enable': 0
					}
		my_datetime = {'time': '%H:%M',
					   'date': '%d-%m-%Y'	
					}
		my_weather = {'api_key': None,
					  'temperature': 'C',
					  'location':{
							"location1": {"place": None, "enabled": False},
							"location2": {"place": None, "enabled": False},
							"location3": {"place": None, "enabled": False},	
								},
					  'cicle': 300				  
					}					
		print('No data found')

Config_Lib = {
	'accounts': accounts,
	'welcome_msg': welcome_msg,
	'default_theme': default_theme,
	'custom_theme': custom_theme,
	'page_format': page_format,
	'my_email': my_email,
	'my_datetime': my_datetime,
	'my_weather': my_weather
}	

default_theme = Config_Lib['default_theme']
cust_BkndColor = Config_Lib['custom_theme']['BkndColor']
cust_FontType = Config_Lib['custom_theme']['FontType']
cust_FontSize = Config_Lib['custom_theme']['FontSize']
cust_FontColor = Config_Lib['custom_theme']['FontColor']
cust_FontTypeSize = '{}pt "{}"'.format(cust_FontSize, cust_FontType)
page_w = Config_Lib['page_format']['page_w'] 
page_h = Config_Lib['page_format']['page_h']
page_x = Config_Lib['page_format']['page_x']
page_y = Config_Lib['page_format']['page_y']
email_receiver = Email.receiver = Config_Lib['my_email']['receiver']
email_username = Email.username = Config_Lib['my_email']['username']
email_password = Email.password = Config_Lib['my_email']['password']
email_subject = Config_Lib['my_email']['subject']
email_message = Config_Lib['my_email']['message']
email_enable = Config_Lib['my_email']['enable']


datetime_time_format = Config_Lib['my_datetime']['time']
datetime_date_format = Config_Lib['my_datetime']['date']
weather_api_key = Config_Lib['my_weather']['api_key']
weather_temp_format = Config_Lib['my_weather']['temperature']
weather_loc1_place = Config_Lib['my_weather']['location']['location1']['place']
weather_loc2_place = Config_Lib['my_weather']['location']['location2']['place']
weather_loc3_place = Config_Lib['my_weather']['location']['location3']['place']
weather_loc1_enable = Config_Lib['my_weather']['location']['location1']['enabled']
weather_loc2_enable = Config_Lib['my_weather']['location']['location2']['enabled']
weather_loc3_enable = Config_Lib['my_weather']['location']['location3']['enabled']
weather_cicle_duration = Config_Lib['my_weather']['cicle']

def Start_GuiInit():
	Gui_Start.btn_SysOn.clicked.connect(Start_SysON)
	Gui_Start.lbl_Welcome.setText(welcome_msg)
	Gui_Start.lbl_ImageLoad.setPixmap(logo_pixmap)
	Gui_Start.btn_SysOn.setIconSize(QtCore.QSize(100, 100))
	Update_Weather()

# Poll_Locations = cycle([weather.location1, weather.location2])
Poll_Locations = cycle([weather_loc1_place, weather_loc2_place, weather_loc3_place])

def Update_Weather():
	weather_location = weather.location = next(Poll_Locations)
	weather.API_Key = weather_api_key
	weather.CheckWeatherAtLocation()
	Gui_Start.lbl_weatherLocation.setText(weather.location)
	Gui_Start.lbl_weatherTemperature.setText(weather.temperature)
	Gui_Start.lbl_weatherStatus.setText((weather.status).capitalize())
	Gui_Start.lbl_weatherFeelsLike.setText('Feels like: {}'.format(weather.feelslike))
	Gui_Start.lbl_weatherHumidity.setText('Humidity: {}'.format(weather.humidity))
	Gui_Start.lbl_weatherWind.setText('Wind: {}'.format(weather.wind))
	Gui_Start.lbl_weatherPressure.setText('Pressure: {}'.format(weather.pressure))
	Gui_Start.lbl_weatherSunrise.setText('Sunrise: {}'.format(weather.sunrise.strftime('{}'.format(datetime_time_format))))
	Gui_Start.lbl_weatherSunset.setText('Sunset: {}'.format(weather.sunset.strftime('{}'.format(datetime_time_format))))	
	# print('{}_{}.png'.format(weather.icon, weather.code))
	weather_icon = 'icons/weather/{}_{}.png'.format(weather.icon, weather.code)
	weather_pixmap = QtGui.QPixmap(weather_icon)
	Gui_Start.lbl_weatherIcon.setPixmap(weather_pixmap)

	if weather_pixmap.isNull():
		if weather.icon[-1] == 'd':
			weather_icon = 'icons/weather/01d_800.png'
			weather_pixmap = QtGui.QPixmap(weather.icon)
			Gui_Start.lbl_weatherIcon.setPixmap(weather_pixmap)
		else:
			weather_icon = 'icons/weather/01n_800.png'
			weather_pixmap = QtGui.QPixmap(weather.icon)
			Gui_Start.lbl_weatherIcon.setPixmap(weather_pixmap)


def Sources_GuiInit():
	Gui_Sources.btn_SysOff.clicked.connect(Sources_SysOFF)
	Gui_Sources.btn_Settings.clicked.connect(Sources_BtnSettings)
	Gui_Sources.slider_horiz.valueChanged.connect(Sources_Volume)
	Gui_Sources.lbl_Volume.setText('80')
	Gui_Sources.btn_YouTube.pressed.connect(Sources_Control_ATV)
	Gui_Sources.btn_Netflix.pressed.connect(Sources_Control_ATV)
	Gui_Sources.btn_Amazon.pressed.connect(Sources_Control_ATV)
	Gui_Sources.btn_IPTV.pressed.connect(Sources_Control_IPTV)
	Gui_Sources.btn_Karaoke.pressed.connect(Sources_Control_Karaoke)	

def Access_GuiInit():
	Gui_Access.btnBox_OKCancel.accepted.connect(Access_DialogOK)
	Gui_Access.btnBox_OKCancel.rejected.connect(Access_DialogCancel)

def Config_GuiInit():
	Gui_Config.btnBox_SaveCancel.accepted.connect(Config_DialogSave)
	Gui_Config.btnBox_SaveCancel.rejected.connect(Config_DialogCancel)
	Gui_Config.actionAccount.triggered.connect(Config_Main_Acount)
	Gui_Config.actionWelcome_Msg.triggered.connect(Config_Main_Welcome)	
	Gui_Config.Config_Stacked.setCurrentIndex(5)
	Gui_Config.PlainText_welcomeMSG.setPlainText(welcome_msg)
	Gui_Config.lbl_ImageLoad.setPixmap(logo_pixmap)
	Gui_Config.actionLogo.triggered.connect(Config_Main_Logo)
	Gui_Config.btn_LoadImage.pressed.connect(Config_LogoLoad)
	Gui_Config.actionTheme_Blue.triggered.connect(themeBlue)
	Gui_Config.actionTheme_Black.triggered.connect(themeBlack)
	Gui_Config.actionTheme_White.triggered.connect(themeWhite)
	Gui_Config.action_ThemeCustom.triggered.connect(themeCustom)	
	Gui_Config.action_ThemeCustom_edit.triggered.connect(lambda: Gui_Config.Config_Stacked.setCurrentIndex(3))
	Gui_Config.actionEmail.triggered.connect(lambda: Gui_Config.Config_Stacked.setCurrentIndex(4))  
	Gui_Config.fontComboBox_CustTheme.currentFontChanged.connect(Config_CustTheme_FntType)
	Gui_Config.dial_ThemeCust_FntSize.valueChanged.connect(Config_CustTheme_FntSize)
	Gui_Config.comboBox_FntColor.currentTextChanged.connect(Config_CustTheme_FntColor)
	Gui_Config.comboBox_BkndColor.currentTextChanged.connect(Config_CustTheme_BkndColor)
	font = QtGui.QFont()
	font.setFamily(cust_FontType)
	Gui_Config.fontComboBox_CustTheme.setCurrentFont(font)
	Gui_Config.lbl_FntSize.setText(str(cust_FontSize))
	Gui_Config.comboBox_FntColor.setCurrentText(cust_FontColor.capitalize())
	Gui_Config.comboBox_BkndColor.setCurrentText(cust_BkndColor.capitalize())
	Gui_Config.lbl_ThemeCust_SampleText.setStyleSheet('background-color: {}; font: {}pt "{}"; color: {}'\
										.format(cust_BkndColor, cust_FontSize, cust_FontType, cust_FontColor))
	Gui_Config.lineEdit_Email_Receiver.setText(email_receiver)
	Gui_Config.lineEdit_Email_Username.setText(email_username)
	Gui_Config.lineEdit_Email_Password.setText(email_password)
	Gui_Config.lineEdit_Email_Subject.setText(email_subject)	
	Gui_Config.textEdit_Email_Message.setText(email_message)
	Gui_Config.checkBox_warningEnable.setCheckState(email_enable)
	Gui_Config.btn_SendTestEmail.clicked.connect(Config_TestEmail)


	Gui_Config.actionTime_Weather.triggered.connect(lambda: Gui_Config.Config_Stacked.setCurrentIndex(5))
	Gui_Config.radio_Time_12h.clicked.connect(Config_Time)
	Gui_Config.radio_Time_24h.clicked.connect(Config_Time)
	Gui_Config.radio_Date_Wed01112020.clicked.connect(Config_Date)
	Gui_Config.radio_Date_Wed01Nov20.clicked.connect(Config_Date)
	Gui_Config.radio_Date_WedNov012020.clicked.connect(Config_Date)
	Gui_Config.lineEdit_weather_api_key.textChanged.connect(Config_Weather_API)
	Gui_Config.radio_Weather_Temp_C.clicked.connect(Config_Weather_TempFormat)
	Gui_Config.radio_Weather_Temp_F.clicked.connect(Config_Weather_TempFormat)
	Gui_Config.lineEdit_Weather_Edit_Loc1.textChanged.connect(Config_Weather_Location_Edit)
	Gui_Config.lineEdit_Weather_Edit_Loc2.textChanged.connect(Config_Weather_Location_Edit)
	Gui_Config.lineEdit_Weather_Edit_Loc3.textChanged.connect(Config_Weather_Location_Edit)
	Gui_Config.checkBox_Weather_Enable_Loc1.clicked.connect(Config_Weather_Location_Enable)
	Gui_Config.checkBox_Weather_Enable_Loc2.clicked.connect(Config_Weather_Location_Enable)
	Gui_Config.checkBox_Weather_Enable_Loc3.clicked.connect(Config_Weather_Location_Enable)
	Gui_Config.comboBox_Weather_Cicle.currentTextChanged.connect(Config_Weather_Cicle)	

	if datetime_time_format == '%I:%M %p':
		Gui_Config.radio_Time_12h.setChecked(True)
	else:
		Gui_Config.radio_Time_24h.setChecked(True)

	if datetime_date_format == '%d-%m-%Y':
		Gui_Config.radio_Date_Wed01112020.setChecked(True)
	elif datetime_date_format == '%d-%b-%y':
		Gui_Config.radio_Date_Wed01Nov20.setChecked(True)
	else:
		Gui_Config.radio_Date_WedNov012020.setChecked(True)
	Gui_Config.lineEdit_weather_api_key.setText(weather_api_key)
	if weather_temp_format == 'C':
		Gui_Config.radio_Weather_Temp_C.setChecked(True)
	else:
		Gui_Config.radio_Weather_Temp_F.setChecked(True)
	Gui_Config.lineEdit_Weather_Edit_Loc1.setText(weather_loc1_place)
	Gui_Config.lineEdit_Weather_Edit_Loc2.setText(weather_loc2_place)
	Gui_Config.lineEdit_Weather_Edit_Loc3.setText(weather_loc3_place)
	Gui_Config.checkBox_Weather_Enable_Loc1.setChecked(weather_loc1_enable)
	Gui_Config.checkBox_Weather_Enable_Loc2.setChecked(weather_loc2_enable)
	Gui_Config.checkBox_Weather_Enable_Loc3.setChecked(weather_loc3_enable)
	Gui_Config.comboBox_Weather_Cicle.setCurrentText(str(weather_cicle_duration))
	
def Config_Time():	
	global datetime_time_format
	if Gui_Config.radio_Time_12h.isChecked() == True: 
		datetime_time_format = '%I:%M %p'
	else:
		datetime_time_format = '%H:%M'
	Config_Lib['my_datetime']['time'] = datetime_time_format

def Config_Date():
	global datetime_date_format
	if Gui_Config.radio_Date_Wed01112020.isChecked() == True:
		datetime_date_format = '%d-%m-%Y'
	elif Gui_Config.radio_Date_Wed01Nov20.isChecked() == True: 
		datetime_date_format = '%d-%b-%y'
	else:
		datetime_date_format = '%b-%d-%Y'
	Config_Lib['my_datetime']['date'] = datetime_date_format

def Config_Weather_API(value):
	global globalweather_api_key
	weather_api_key = Config_Lib['my_weather']['api_key'] = Gui_Config.lineEdit_weather_api_key.text()
	
def Config_Weather_TempFormat():
	global weather_temp_format
	if Gui_Config.radio_Weather_Temp_C.isChecked() == True: 
		weather_temp_format = 'C'
	else:
		weather_temp_format = 'F'
	Config_Lib['my_weather']['temperature'] = weather_temp_format

def Config_Weather_Location_Edit():	
	weather_loc1_place = Gui_Config.lineEdit_Weather_Edit_Loc1.text()
	weather_loc2_place = Gui_Config.lineEdit_Weather_Edit_Loc2.text()
	weather_loc3_place = Gui_Config.lineEdit_Weather_Edit_Loc3.text()
	Config_Lib['my_weather']['location']['location1']['place'] = weather_loc1_place
	Config_Lib['my_weather']['location']['location2']['place'] = weather_loc2_place
	Config_Lib['my_weather']['location']['location3']['place'] = weather_loc3_place

def Config_Weather_Location_Enable():
	weather_loc1_enable = Gui_Config.checkBox_Weather_Enable_Loc1.isChecked()
	weather_loc2_enable = Gui_Config.checkBox_Weather_Enable_Loc2.isChecked()
	weather_loc3_enable = Gui_Config.checkBox_Weather_Enable_Loc3.isChecked()
	Config_Lib['my_weather']['location']['location1']['enabled'] = weather_loc1_enable
	Config_Lib['my_weather']['location']['location2']['enabled'] = weather_loc2_enable
	Config_Lib['my_weather']['location']['location3']['enabled'] = weather_loc3_enable

def Config_Weather_Cicle(value):
	global weather_cicle_duration
	weather_cicle_duration = Config_Lib['my_weather']['cicle'] = int(value)

def Config_TestEmail():
	Config_DialogSave()
	subject = 'Warning - AV system is started!'
	message = 'AV system started at {}'.format(cur_time)
	if email_enable == 2:		
		Email.sendEmail(subject, message)
		email_testResult = Email.testResult
	else:
		email_testResult = 'Email warning is disabled'
	Gui_Config.lbl_TestEmailResult.setText(email_testResult)
	# time.sleep(2)
	# Gui_Config.lbl_TestEmailResult.setText('')
		

def Config_CustTheme_FntType(value):
	global cust_FontType
	cust_FontType = value.family()
	CustomFont_Preview()

def Config_CustTheme_FntSize(value):
	global cust_FontSize
	cust_FontSize = value
	CustomFont_Preview()

def Config_CustTheme_FntColor(value):
	global cust_FontColor
	cust_FontColor = value.lower()
	CustomFont_Preview()

def Config_CustTheme_BkndColor(value):
	global cust_BkndColor
	cust_BkndColor = value.lower()
	CustomFont_Preview()

def CustomFont_Preview():
	Gui_Config.lbl_ThemeCust_SampleText.setStyleSheet('background-color: {}; font: {}pt "{}"; color: {}'\
										.format(cust_BkndColor, cust_FontSize, cust_FontType, cust_FontColor))
	
def Config_LogoLoad():
	image = QtWidgets.QFileDialog.getOpenFileName(None,'OpenFile','',"Image load...(*.png)")
	image_LoadPath = image[0]
	logo_file = QtCore.QFile(image_LoadPath)
	try:
		logo_file.remove(logo_path)
		logo_file.copy(image_LoadPath, logo_path)
		logo_pixmap = QtGui.QPixmap(image_LoadPath)
		Gui_Start.lbl_ImageLoad.setPixmap(logo_pixmap)
		Gui_Config.lbl_ImageLoad.setPixmap(logo_pixmap)		
		print('Copy file - success')
	except:
		print('Copy file - failed')
	
####Pages control
###START###
def Start_SysON():
	Page_Sources.resize(page_w, page_h)
	Page_Sources.move(page_x - page_x_offset, page_y - page_y_offset)
	Page_Sources.show()
	Page_Start.hide()
	Gui_Access.lbl_loginStatus.setText('')
	Gui_Sources.btn_YouTube.setChecked(True)
	

###SOURCES###
def Sources_SysOFF():
	Page_Start.resize(page_w, page_h)
	Page_Start.move(page_x - page_x_offset, page_y - page_y_offset)
	Page_Start.show()
	Page_Sources.hide()
	

def Sources_BtnSettings():
	Page_Access.resize(page_w, page_h)
	Page_Access.move(page_x - page_x_offset, page_y - page_y_offset)
	Page_Access.show()
	Page_Sources.hide()
	Gui_Access.lineEdit_Login_Username.setText('')
	Gui_Access.lineEdit_Login_Password.setText('')

def Sources_Volume(lvl_volume):
	print(lvl_volume)

def Sources_Control_ATV():
	Gui_Sources.Sources_Stacked.setCurrentIndex(0)

def Sources_Control_IPTV():
	Gui_Sources.Sources_Stacked.setCurrentIndex(1)

def Sources_Control_Karaoke():
	Gui_Sources.Sources_Stacked.setCurrentIndex(2)


###ACCESS###
def Access_DialogOK():
	username = Gui_Access.lineEdit_Login_Username.text()
	password = Gui_Access.lineEdit_Login_Password.text()

	if username in accounts.keys():
		if password == accounts[username]:
			Gui_Access.lbl_loginStatus.setText('Access granted')
			timer2sec.startTimer()
		else:
			Gui_Access.lbl_loginStatus.setText('Wrong password. Try again.')
			Gui_Access.lineEdit_Login_Password.setText('')
	else:
		Gui_Access.lbl_loginStatus.setText('Wrong username. Try again')	
		Gui_Access.lineEdit_Login_Username.setText('')
		Gui_Access.lineEdit_Login_Password.setText('')

def Access_DialogCancel():
	Page_Sources.resize(page_w, page_h)
	Page_Sources.move(page_x - page_x_offset, page_y - page_y_offset)
	Page_Sources.show()
	Page_Access.hide()
	Gui_Access.lbl_loginStatus.setText('')

###CONFIGURATION###
def ShowConfigPage():
	Page_Config.resize(page_w, page_h)
	Page_Config.move(page_x - page_x_offset, page_y - page_y_offset)
	Page_Config.show()	
	Page_Access.hide()

def Config_DialogSave():
	global welcome_msg
	global email_receiver, email_username, email_password, email_subject, email_message, email_enable
	Config_Lib['welcome_msg'] = welcome_msg = Gui_Config.PlainText_welcomeMSG.toPlainText() 
	Gui_Start.lbl_Welcome.setText(welcome_msg)
	Config_Lib['default_theme'] = default_theme
	Config_Lib['custom_theme']['BkndColor'] = cust_BkndColor
	Config_Lib['custom_theme']['FontType'] = cust_FontType
	Config_Lib['custom_theme']['FontSize'] = cust_FontSize
	Config_Lib['custom_theme']['FontColor'] = cust_FontColor
	Config_Lib['page_format']['page_w'] = page_w 
	Config_Lib['page_format']['page_h'] = page_h
	Config_Lib['page_format']['page_x'] = page_x
	Config_Lib['page_format']['page_y'] = page_y
	Config_Lib['my_email']['receiver'] = email_receiver = Email.receiver = Gui_Config.lineEdit_Email_Receiver.text()
	Config_Lib['my_email']['username'] = email_username = Email.username = Gui_Config.lineEdit_Email_Username.text()
	Config_Lib['my_email']['password'] = email_password = Email.password = Gui_Config.lineEdit_Email_Password.text()
	Config_Lib['my_email']['subject'] = email_subject = Gui_Config.lineEdit_Email_Subject.text()
	Config_Lib['my_email']['message'] = email_message = Gui_Config.textEdit_Email_Message.toPlainText()
	Config_Lib['my_email']['enable'] = email_enable = Gui_Config.checkBox_warningEnable.checkState()
	with open ('config/config.json', 'w') as json_outfile:
		json.dump(Config_Lib, json_outfile, indent=2)
	

def Config_DialogCancel():
	Gui_Access.lbl_loginStatus.setText('')
	Page_Sources.resize(page_w, page_h)
	Page_Sources.move(page_x - page_x_offset, page_y - page_y_offset)
	Page_Sources.show()
	Page_Config.hide()

def Config_Main_Acount():
	Gui_Config.Config_Stacked.setCurrentIndex(0)

def Config_Main_Welcome():
	Gui_Config.Config_Stacked.setCurrentIndex(1)

def Config_Main_Logo():
	Gui_Config.Config_Stacked.setCurrentIndex(2)

#########Timer##########
class Timer():
	def __init__(self, interval, func):
		self.timer = timer()
		self.timer.interval = interval
		self.func = func 
		self.timer.setInterval(self.timer.interval)
		self.timer.setSingleShot(True)

	def startTimer(self):
		self.timer.timeout.connect(self.func)
		self.timer.start()

##########create timers (miliseconds, function to run)
timer2sec = Timer(2000, ShowConfigPage)	

def themeBlue():
	global default_theme
	Theme('rgb(0, 173, 210)', '10pt "MS Shell Dlg 2"', 'rgb(255, 255, 255)')
	default_theme = 'blue'

def themeBlack():
	global default_theme
	Theme('black', '14pt "Arial"', 'red')
	default_theme = 'black'

def themeWhite():
	global default_theme
	Theme('white', '14pt "Arial"', 'green')
	default_theme = 'white'


def themeCustom():
	global default_theme
	Theme(cust_BkndColor, '{}pt "{}"'.format(cust_FontSize, cust_FontType), cust_FontColor)
	default_theme = 'custom'


def defaultTheme():
	if default_theme == 'black':
		themeBlack()
	elif default_theme == 'white':
		themeWhite()
	elif default_theme == 'custom':
		themeCustom()
	else:
		themeBlue()	

def Theme(background_color, font, color):
	Page_Start.setStyleSheet("background-color: {}; font:{};color:{}".format(background_color, font, color))
	Page_Sources.setStyleSheet("background-color: {}; font:{};color:{}".format(background_color, font, color))
	Page_Access.setStyleSheet("background-color: {}; font:{};color:{}".format(background_color, font, color))
	Page_Config.setStyleSheet("background-color: {}; font:{};color:{}".format(background_color, font, color))

def onResize(event):
	global page_w, page_h
	size = event.size()
	page_w = size.width()
	page_h = size.height()
 
def onMove(event):
	global page_x, page_y
	location = event.pos()
	page_x = location.x()
	page_y = location.y()

def onClose(event):
	with open ('config/config.json', 'w') as json_outfile:
		Config_Lib['page_format']['page_w'] = page_w 
		Config_Lib['page_format']['page_h'] = page_h
		Config_Lib['page_format']['page_x'] = page_x
		Config_Lib['page_format']['page_y'] = page_y
		json.dump(Config_Lib, json_outfile, indent=2)



########## TEST ENVIRONMENT ONLY ################
def Test1_GuiInit():
	Gui_Start.btn_Test.clicked.connect(Test1_Page)
	Gui_Test1.btn_Test1_GoTest2.clicked.connect(Test2_Page)
	Gui_Test1.btn_Test1_GoMain.clicked.connect(Test1ShowStart)
	Gui_Test1.btn_color.clicked.connect(Test1_DialogColor)
	Gui_Test1.btn_font.clicked.connect(Test1_DialogFont)
	Gui_Test1.btn_input.clicked.connect(Test1_DialogInput)
	Gui_Test1.btn_progress.clicked.connect(Test1_DialogProgress)

def Test2_GuiInit():
	Gui_Test2.btn_Test2_GoTest1.clicked.connect(Test1_Page)

def Test1ShowStart():
	Page_Start.resize(page_w, page_h)
	Page_Start.move(page_x - page_x_offset, page_y - page_y_offset)
	Page_Start.show()
	Page_Test1.hide()	

def Test1_Page():
	Page_Test1.resize(page_w, page_h)
	Page_Test1.move(page_x - page_x_offset, page_y - page_y_offset)
	Page_Test1.show()
	Page_Test2.hide()
	Page_Start.hide()	

def Test1_DialogColor():
	ChoseColor = QtWidgets.QColorDialog.getColor()
	color = ChoseColor.name()
	print(color)
	Gui_Test1.lbl_color.setStyleSheet('background-color:{}'.format(color))	

def Test1_DialogFont():
	ChoseFont = QtWidgets.QFontDialog.getFont()	
	fontString = ChoseFont[0].toString()
	fontType = fontString.split(",")[0]
	fontSize = fontString.split(",")[1]	
	Gui_Test1.lbl_font.setStyleSheet('font:{}pt "{}"'.format(fontSize, fontType))

def Test1_DialogInput():
	items = ["Spring", "Summer", "Fall", "Winter"]
	dialogInput = QtWidgets.QInputDialog()
	dialogInput.setGeometry(300, 300, 300, 140)
	# text = dialogInput.getText(QtWidgets.QInputDialog(), 'What is your name?', 'Enter your name:')
	text = dialogInput.getItem(QtWidgets.QInputDialog(),"Pick a season", "Season:", items, 0, False)
	print(text[0])

def Test1_DialogProgress():
	dialogProgress = QtWidgets.QWidget()
	progress = QtWidgets.QProgressDialog("Please Wait!", "Cancel", 0, 100, dialogProgress)
	progress.setWindowModality(QtCore.Qt.WindowModal)
	progress.setAutoReset(True)
	progress.setAutoClose(True)
	progress.resize(500,100)	
	count = 0
	while count < 100:
		count += 1
		time.sleep(0.1)
		progress.setValue(count)
	
def Test2_Page():
	Page_Test2.resize(page_w, page_h)
	Page_Test2.move(page_x - page_x_offset, page_y - page_y_offset)
	Page_Test2.show()
	Page_Test1.hide()



########## START TEST ################
if __name__ == '__main__':
	import sys
	app = QtWidgets.QApplication(sys.argv)
	##initialize Start page
	Page_Start = QtWidgets.QMainWindow()
	Gui_Start = Start.Ui_Start()
	Gui_Start.setupUi(Page_Start)
	Page_Start.resizeEvent = onResize
	Page_Start.moveEvent = onMove	
	Page_Start.closeEvent = onClose
	Page_Start.resize(page_w, page_h)  
	Page_Start.move(page_x - page_x_offset, page_y - page_y_offset)
	logo_path = 'config/logo.png'
	logo_pixmap = QtGui.QPixmap(logo_path)	
	Start_GuiInit()

	##initialize Sources page	
	Page_Sources = QtWidgets.QMainWindow()
	Gui_Sources = Sources.Ui_Sources()
	Gui_Sources.setupUi(Page_Sources)
	Page_Sources.resizeEvent = onResize
	Page_Sources.moveEvent = onMove
	Page_Sources.closeEvent = onClose
	Sources_GuiInit()

	##initialize Access page
	Page_Access = QtWidgets.QMainWindow()
	Gui_Access = Access.Ui_Access()
	Gui_Access.setupUi(Page_Access)	
	Page_Access.resizeEvent = onResize
	Page_Access.moveEvent = onMove
	Page_Access.closeEvent = onClose
	Access_GuiInit()

	##initialize Configuration page
	Page_Config = QtWidgets.QMainWindow()
	Gui_Config = Config.Ui_Config()
	Gui_Config.setupUi(Page_Config)
	Page_Config.resizeEvent = onResize
	Page_Config.moveEvent = onMove
	Page_Config.closeEvent = onClose
	Config_GuiInit()

	Page_Test1 = QtWidgets.QMainWindow()
	Gui_Test1 = Test1.Ui_Test1()
	Gui_Test1.setupUi(Page_Test1)
	Page_Test1.resizeEvent = onResize
	Page_Test1.moveEvent = onMove
	Page_Test1.closeEvent = onClose
	Test1_GuiInit()

	Page_Test2 = QtWidgets.QMainWindow()
	Gui_Test2 = Test2.Ui_Test2()
	Gui_Test2.setupUi(Page_Test2)
	Page_Test2.resizeEvent = onResize
	Page_Test2.moveEvent = onMove
	Page_Test2.closeEvent = onClose	
	Test2_GuiInit()

	
	##use timers
	timer_poll_time = QtCore.QTimer()
	timer_poll_time.start(1000)
	timer_poll_time.timeout.connect(Update_Time)
	
	timer_poll_weather = QtCore.QTimer()
	timer_poll_weather.start(10000) #1000 = 1s
	timer_poll_weather.timeout.connect(Update_Weather)

	Page_Sources.show()  ##Remove innitial pages flicker 	
	Page_Access.show()	 ##by showing and hiding each pages
	Page_Config.show()
	Page_Test1.show() 				
	Page_Test2.show()  
	Page_Sources.hide()
	Page_Access.hide()
	Page_Config.hide()
	Page_Test1.hide()
	Page_Test2.hide()

	defaultTheme()  #apply theme after show/hide pages so all widgets get the stylesheet settings

	# Page_Start.show()
	Page_Start.show()
	sys.exit(app.exec_())	
