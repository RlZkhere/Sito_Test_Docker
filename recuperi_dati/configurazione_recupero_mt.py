import time
import os
import traceback
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
opzioni=Options()
opzioni.add_argument('headless')
opzioni.add_argument("--no-sandbox")
opzioni.add_argument("window-size=1920,1080")
opzioni.add_argument("--disable-dev-shm-usage")
opzioni.add_argument("--disable-gpu")
service=Service()
service=Service(executable_path="/usr/bin/chromedriver")
opzioni.binary_location = "/usr/bin/chromium-browser"
browser=webdriver.Chrome(service=service,options=opzioni)
