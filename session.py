from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

from bw import classicBW

class session:

    # Creating an array of all of the workspaces
    bws = []

    # Constructor
    def __init__(self, VMnum):
        self.VMnum = VMnum
        self.driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")
        self.home = "http://192.168.2." + str(VMnum) + "/otcs/cs.exe?func=llworkspace"
        self.driver.get(self.home)
        self.logIn()

    # Wait for function
    def waitFor(self, , by, element):
        try:
            wait = WebDriverWait(self.driver, 20).until(
                if by == "id":
                    EC.presence_of_element_located((By.ID, ))
            )
    
    # Logging in
    def logIn(self):
        self.driver.find_element(By.ID, "otds_username").send_keys("Admin")
        self.driver.find_element(By.ID, "otds_password").send_keys("livelink" + Keys.RETURN)
        time.sleep(10000)

    # Changing the language
    def changeLang(lang):


    # Multilingualising the workspace attributes
    #def multilingualiseAttributes(self):

    def createBW(self, num, SDL, nameSDL, nameUDL, attSDL, attUDL, VMnum):
        temp = classicBW(num, SDL, nameSDL, nameUDL, attSDL, attUDL, VMnum)
        self.bws.append(temp)
