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
        self.smartHome = "http://192.168.2." + str(VMnum) + "/otcs/cs.exe/app/nodes/2000"
        self.driver.get(self.home)
        self.driver.set_window_position(-1000, 0)
        self.driver.maximize_window()
        self.logIn()
    
    # Destructor
    def __del__(self):
        print("This session has ended")

    # Quit
    def quit(self):
        self.driver.quit()

    # Checking if the user would like to continue the test
    def askCont(self):
        cont = ""
        while True:
            print("Would you like to continue? (y/n)")
            cont = input().lower()
            if cont == "y": return
            if cont == "n": self.quit(); print("Ended session early.")


    # Click on an element (Includes waiting for)
    def clickOn(self, by, path):
        by = by.upper()
        self.waitFor(by, path, True)
        self.driver.find_element(eval("By."+ by), path).click()
        return
    
    def error(self, where, lang, expected, received):
        print(f"ERROR!\n Unexpected result for {where} in {lang}.\n Expected '{expected}' but got '{received}'")
        self.askCont()
        return
    
    # Getting an Attribute of an Element
    def getAtt(self, by, path, att):
        by = by.upper()
        self.waitFor(by, path)
        return self.driver.find_element(eval(f"By.{by}"), path).get_attribute(att)
    
    # Returning the text of a field
    def getText(self, by, path):
        by = by.upper()
        self.waitFor(by, path)
        return self.driver.find_element(eval("By."+by), path).text
    
    # Going to a page
    def goTo(self, page="llworkspace"):
        location = self.home.replace("llworkspace", page)
        self.driver.get(location)
        return
    
    # Reloading the page
    def reload(self):
        time.sleep(0.5)
        self.driver.refresh()
        time.sleep(0.5)
        return

    # Wait for function
    def waitFor(self, by, element, clickable=False):
        by = by.upper()
        if clickable:
            try:
                wait = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((eval("By." + by), element))
                )
                return
            except:
                print("There seems to have been an error.")
                print(f"Looking for {by} of {element}.")
                confirm = input("Press enter to continue\n")
                if confirm != "": self.driver.quit()
                return
        try:
            wait = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((eval("By." + by), element))
            )
            return
        except:
            print("There seems to have been an error.")
            print(f"Looking for {by} of {element}.")
            confirm = input("Press enter to continue\n")
            if confirm != "": self.driver.quit()
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

    # Changing the language
    def changeLang (self, lang):
        if lang.lower() == "en": lang = "en_US"; self.SDL = True
        else: lang = lang.lower(); self.SDL = False
        self.goTo("personal.settings")
        self.waitFor("ID", "metadataLang")
        Select(self.driver.find_element(By.ID, "metadataLang")).select_by_value(lang)
        self.clickOn("CLASS_NAME", "saveButton")
        #self.driver.find_element(By.CLASS_NAME, "saveButton").click()
        self.driver.back()
        self.driver.back()
        self.reload()
        time.sleep(1)
        print("Changed language to", lang.upper())
        return
    
    # Returning the title of the page
    def getTitle(self):
        print(self.driver.title)