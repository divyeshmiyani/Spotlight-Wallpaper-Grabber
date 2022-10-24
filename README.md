# Spotlight-Wallpaper-Grabber
Saves Windows Spotlight Wallpaper

## Contains
[Requirements](https://github.com/divyeshmiyani/Spotlight-Wallpaper-Grabber/README.md#requirements)  
[Setup](https://github.com/divyeshmiyani/Spotlight-Wallpaper-Grabber/README.md#setup)  
[Make build](https://github.com/divyeshmiyani/Spotlight-Wallpaper-Grabber/README.md#make-buid)  
[Usage](https://github.com/divyeshmiyani/Spotlight-Wallpaper-Grabber/README.md#usage)  
[Tested on](https://github.com/divyeshmiyani/Spotlight-Wallpaper-Grabber/README.md#tested-on)

## Requirements  
google_auth_oauthlib==0.4.4  
google_api_python_client==2.55.0  
Pillow==9.2.0  
protobuf==4.21.4  
PyQt5==5.15.7  

## Setup

Run `pip install -r requirements.txt` or `python -m pip install -r requirements.txt` command in cmd to resolve requirements

## Make buid
Clone repository Using git command  
`git clone https://github.com/divyeshmiyani/Spotlight-Wallpaper-Grabber.git `  
Or Simple Download and extract  

Run commands in terminal  
`pyinstaller --onefile --noconsole --clean SWG.py`  

Executable file will be found in `./dist` folder

## Usage
Run `SWG.exe` file ( to create .exe file refer [this](https://github.com/divyeshmiyani/Spotlight-Wallpaper-Grabber/edit/main/README.md#make-buid) )  
**OR**  
Just run the `SWG.py` file
window will appear like this  

<img src=Screenshots/first_screen.png>  

Click on `Browse` button or enter path
Click on `Save` button  

Currently running Spotlight Wallpaper will be saved to your desired directory.

Click on Connect Button to connect to Google Drive and click on Sync Button to Upload currently present wallpaper to Google Drive.
In Google drive wallpaper will be saved in `SpotlightWallpaper` folder.

## Tested on
Windows 10
