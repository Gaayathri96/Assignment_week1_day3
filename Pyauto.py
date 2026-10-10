import pyautogui 
import webbrowser 
from datetime import datetime
import time

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 1.5

print("Step1: Open Chrome and navigate to a new window")
pyautogui.hotkey('win', 'r')
time.sleep(2)
pyautogui.write('chrome')
pyautogui.press('enter')
time.sleep(2)

print("Step2: Open a new tab and navigate to the AccuWeather Chennai weather forecast page")
# pyautogui.hotkey('ctrl', 't')
# time.sleep(2)
pyautogui.write('https://www.accuweather.com/en/in/chennai/206671/weather-forecast/206671')
time.sleep(2)
pyautogui.press('enter')
time.sleep(5)

print("Step3: Select all text and copy it")
pyautogui.hotkey('ctrl', 'a', interval=0.25)
time.sleep(2)
pyautogui.hotkey('ctrl', 'c', interval=0.25)   
time.sleep(2)

print("Step4: Open Notepad and paste the copied text")
pyautogui.hotkey('win', 'r')
time.sleep(2)
pyautogui.write('notepad')
pyautogui.press('enter')
time.sleep(2)

pyautogui.hotkey('ctrl', 'v', interval=0.25)
time.sleep(2)
pyautogui.hotkey('ctrl', 's', interval=0.25)
time.sleep(2)
pyautogui.write('daily_report_' + datetime.now().strftime("%Y-%m-%d"))
pyautogui.press('enter')

print("Step5: Take a screenshot of the current screen and save it with the current date")
pyautogui.screenshot().save("daily_report_" + datetime.now().strftime("%Y-%m-%d")+".png")