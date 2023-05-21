from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import time

#from bw import classicBW

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
    def waitFor(self, by, element):
        try:
            wait = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((eval("By." + by), element))
            )
        except:
            print("There seems to have been an error.")
            print("Looking for", by, "of", element)
            confirm = input("Press enter to continue\n")
            if confirm != "": self.driver.close()
    
    # Reloading the page
    def reload(self):
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.COMMAND + "r")

    # Going to a page
    def goTo(self, page):
        location = self.home.replace("llworkspace", page)
        self.driver.get(location)
    
    # Logging in
    def logIn(self):
        self.driver.find_element(By.ID, "otds_username").send_keys("Admin")
        self.driver.find_element(By.ID, "otds_password").send_keys("livelink" + Keys.RETURN)
        print("Logged in")

    # Changing the language
    def changeLang (self, lang):
        self.goTo("personal.settings")
        self.waitFor("ID", "metadataLang")
        Select(self.driver.find_element(By.ID, "metadataLang")).select_by_value(lang.lower())
        self.driver.find_element(By.CLASS_NAME, "saveButton").click()
        self.reload()
        self.driver.back()
        self.driver.back()
        print("Changed language to", lang)

    # Multilingualizing the Workspace
    def multilingualizeWorkspace(self):
        self.goTo("ll&objType=133&objAction=browse")
        #BWWSID = self.getIDFromText("BW WS")
        #self.driver.find_element(By.ID, self.getIDFromText("BW WS")).click()
        #self.driver.find_element(By.XPATH, "//a[@title='Functions']").click()
        self.driver.find_element(By.XPATH, "//a[@title='Function menu for BW WS']").click()
        self.driver.find_element(By.XPATH, "//*[contains(@id, 'menuItem_Properties')]").click()
        time.sleep(20)

    # Getting the id from text
    def getIDFromText(self, text):
        print(text)
        id = self.driver.find_element(By.LINK_TEXT, text)
        return id.get_attribute("id")

    # Creating a Workspace
    def createBW(self, num, SDL, nameSDL, nameUDL, attSDL, attUDL, VMnum):
        temp = classicBW(num, SDL, nameSDL, nameUDL, attSDL, attUDL, VMnum)
        self.bws.append(temp)
