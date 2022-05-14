from asyncio.windows_events import NULL
import time
import re
from seleniumwire import webdriver
from seleniumwire.utils import decode
from selenium.webdriver.common.keys import Keys
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.chrome.options import Options
import os
import urllib
import pydub
import ffmpy
import speech_recognition as sr


def Solve(pro,link):
    option = Options()
    option.headless = True
    option.add_argument("--start-maximized")
    
    if pro != NULL:
        Opti = {
        'proxy' : pro
        }
        driver = webdriver.Chrome(os.getcwd()+"\\chromedriver.exe",options=option,seleniumwire_options=Opti)
    
    else:
        driver = webdriver.Chrome(os.getcwd()+"\\chromedriver.exe",options=option)
    
    try:
        driver.get(link)
        frames = driver.find_elements_by_tag_name("iframe")
        driver.switch_to.frame(frames[0])
        delay()
        driver.find_element_by_class_name("recaptcha-checkbox-border").click()

        delay()
        for req in driver.requests:
            if "https://www.google.com/recaptcha/api2/userverify" in req.url:
                body = str(decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity')))
                tk = re.search('"uvresp","(.*)",', body)[1]
                driver.quit()
                return tk

        for i in range(1,20):
            try:
                driver.switch_to.default_content()
                frames = driver.find_element_by_xpath(f"/html/body/div[{i}]/div[4]").find_elements_by_tag_name("iframe")
                driver.switch_to.frame(frames[0])
                if driver.find_element_by_id("recaptcha-audio-button").is_displayed():
                    driver.find_element_by_id("recaptcha-audio-button").click()
                    break
            except:
                pass

        delay()
        driver.switch_to.default_content()
        frames = driver.find_elements_by_tag_name("iframe")
        driver.switch_to.frame(frames[-1])
        # driver.find_element_by_xpath("/html/body/div/div/div[3]/div/button").click()

        src = driver.find_element_by_id("audio-source").get_attribute("src")
        # print("[INFO] Audio src: %s" % src)

        urllib.request.urlretrieve(src, os.getcwd() + "\\sample.mp3")
        sound = pydub.AudioSegment.from_mp3(os.getcwd() + "\\sample.mp3")
        sound.export(os.getcwd() + "\\sample.wav", format="wav")
        sample_audio = sr.AudioFile(os.getcwd() + "\\sample.wav")
        r = sr.Recognizer()
        with sample_audio as source:
            audio = r.record(source)

        key = r.recognize_google(audio)
        # print("[INFO] Recaptcha Passcode: %s" % key)

        driver.find_element_by_id("audio-response").send_keys(key.lower())
        driver.find_element_by_id("audio-response").send_keys(Keys.ENTER)
        delay()
        for req in driver.requests:
            if "https://www.google.com/recaptcha/api2/userverify" in req.url:
                body = str(decode(req.response.body, req.response.headers.get('Content-Encoding', 'identity')))
                tk = re.search('"uvresp","(.*)",', body)[1]
                driver.quit()
                return tk
        driver.quit()
        Solve(pro,link)
    except:
        driver.quit()
        Solve(pro,link)     

def delay(Delay = 4):
    time.sleep(Delay)


#Proxies = {
#            'http': 'http://127.0.0.1:8080',
#            'https': 'https://127.0.0.1:443'
#        }

#token = Solve(Proxies,"https://www.google.com/recaptcha/api2/demo")
token = Solve(NULL,"https://www.google.com/recaptcha/api2/demo")

print(token)
