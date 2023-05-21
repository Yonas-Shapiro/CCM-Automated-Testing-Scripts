from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import time

#from bw import classicBW

class session:

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
            return
        except:
            print("There seems to have been an error.")
            print("Looking for", by, "of", element)
            confirm = input("Press enter to continue\n")
            if confirm != "": self.driver.close()
            return

    # Click on an element (Includes waiting for)
    def clickOn(self, by, path):
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
        self.driver.find_element(By.ID, "otds_username").send_keys("Admin")
        self.driver.find_element(By.ID, "otds_password").send_keys("livelink" + Keys.RETURN)
        print("Logged in")
        return

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

    # Multilingualizing the Workspace
    def multilingualizeWorkspace(self):
        self.goTo("ll&objType=133&objAction=browse")
        self.clickOn("XPATH", "//a[@title='Function menu for BW WS']")
        self.clickOn("XPATH", "//*[contains(@id, 'menuItem_Properties')]")
        self.clickOn("LINK_TEXT", "Multilingual")
        Select(self.driver.find_element(By.ID, "editMLDestLang")).select_by_value("fr")
        self.clickOn("ID", "_1_1_2")
        self.clickOn("ID", "_1_1_3")
        self.driver.find_element(By.NAME, "_1_1_2_Dest").send_keys("tf fr")
        self.driver.find_element(By.NAME, "_1_1_4_Dest").send_keys("tml fr")
        self.clickOn("XPATH", "//input[@name='radTransType' and @value='1']")
        self.driver.find_element(By.NAME, "_1_1_3_Dest_pp").clear()
        self.driver.find_element(By.NAME, "_1_1_3_Dest_pp").send_keys("un" + Keys.RETURN + "deux" + Keys.RETURN + "trois")
        self.clickOn("ID", "btnSave")
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
