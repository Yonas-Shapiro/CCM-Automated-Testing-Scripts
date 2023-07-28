from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import time

#from bw import classicBW

class basics:

    # Constructor
    def __init__(self, VMnum):
        self.VMnum = VMnum
        self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        #self.driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")
        self.home = "http://192.168.2." + str(VMnum) + "/otcs/cs.exe?func=llworkspace"
        self.driver.get(self.home)
        self.driver.set_window_position(-1000, 0)
        self.driver.maximize_window()
        self.logIn()
    
    def __del__(self):
        print("This session has ended")

    def quit(self):
        self.driver.quit()

    # Wait for function
    def waitFor(self, by, element):
        try:
            wait = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((eval("By." + by), element))
            )
            return
        except:
            print("There seems to have been an error.")
            print("Looking for", by, "of", element)
            confirm = input("Press enter to continue\n")
            if confirm != "": self.driver.close()
            return

    # Click on an element (Includes waiting for)
    def clickOn(self, by, path):
        by = by.upper()
        self.waitFor(by, path)
        self.driver.find_element(eval("By."+ by), path).click()
        return

    
    # Reloading the page
    def reload(self):
        time.sleep(0.5)
        self.driver.refresh()
        time.sleep(0.5)
        return

    # Going to a page
    def goTo(self, page="llworkspace"):
        location = self.home.replace("llworkspace", page)
        self.driver.get(location)
        return
    
    # Logging in
    def logIn(self):
        self.waitFor("ID", "otds_username")
        self.driver.find_element(By.ID, "otds_username").send_keys("Admin")
        self.driver.find_element(By.ID, "otds_password").send_keys("livelink" + Keys.ENTER)
        self.waitFor("ID", "browseViewCoreTable")
        #self.clickOn("ID", "loginbutton")
        print("Logged in")
        return

    def getTitle(self):
        print(self.driver.title)

    # Changing the language
    def changeLang (self, lang):
        if lang.lower() == "en": lang = "en_US"
        else: lang = lang.lower()
        self.goTo("personal.settings")
        self.waitFor("ID", "metadataLang")
        Select(self.driver.find_element(By.ID, "metadataLang")).select_by_value(lang)
        self.clickOn("CLASS_NAME", "saveButton")
        #self.driver.find_element(By.CLASS_NAME, "saveButton").click()
        self.driver.back()
        self.driver.back()
        self.reload()
        time.sleep(1)
        print("Changed language to", lang)
        return





    # Getting the id from text (OBSELETE?)
    def getIDFromText(self, text):
        print(text)
        id = self.driver.find_element(By.LINK_TEXT, text)
        return id.get_attribute("id")

    # Creating a Workspace
    def createBW(self, num, SDL, nameSDL, nameUDL, attSDL, attUDL, VMnum):
        if SDL:
            self.changeLang("en")
            self.goTo()
            self.clickOn("LINK_TEXT", "Other Items")
        else:
            self.changeLang("fr")
            self.goTo()
            self.clickOn("LINK_TEXT", "Autres éléments")
        self.clickOn("XPATH", "//a[@class='browseItemNameContainer' and contains(@id, 'node')]")
        self.clickOn("ID", "addItemMenu0Head")
        self.clickOn("ID", "menuItem_848")
        
        time.sleep(10)

        #bw = classicBW(num, SDL, nameSDL, nameUDL, attSDL, attUDL, VMnum)
