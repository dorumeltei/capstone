# Daily Digest app
A simple and intuitive app that gets categorized information via APIs. 

## Project description: 
* Scope: build an app with pyqt and QT Designer that will pull  and organize relevant information, via APIs. Information is related to daily activities using most popular/common apps and websites. Data will be grouped into 3 categories: News, Inspire, Entertain. 

## Dependencies:

* OS: 
    Windows 10 or 11

* Python library:
    PyQt5==5.15.6
    PyQt5-Qt5==5.15.2
    PyQt5-sip==12.9.1
    PyQtWebEngine==5.15.5
    requests==2.27.1

* APIs used:
    * https://newsapi.org/
    * http://quotes.stormconsultancy.co.uk/
    * https://rapidapi.com/humorapi/api/humor-jokes-and-memes
    * https://api.humorapi.com/
    * https://rapidapi.com/vitlabs27/api/radio-world-50-000-radios-stations 

### Installing

* Follow the API links to get needed keys
* Place all .ui pages + "daily-digest.exe" in the same folder. 
* Run portable executable.
* There is an issue playing any mp4 stream (IE from Youtube) using QtWebEngineWidgets so look for streams that are not mp4 format. 

### Executing program

* Run "daily-digest.exe"
* Initial configuration: 
    * A local "config.json" file is created at first initialization. All user-based configuration is stored here. A more secure solution for account storage will be implemented in future releases.
    * create a new user and login
    * Go to configuration page, add the keys and save. Restart the app. 
* APIs will load after successful login

## Authors

* Doru Meltei (dhoroo1ro@yahoo.com) 
* Cagdas Yetkin (cagdasyetkin@yahoo.com)

## Version History

* 0.1
    * Initial Release

## License

This project is not licensed.

## Acknowledgments

* [great API library](https://rapidapi.com)

## Relevant images
Check relevant images in "img" folder
