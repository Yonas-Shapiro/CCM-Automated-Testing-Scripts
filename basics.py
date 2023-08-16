from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
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
        self.actions = ActionChains(self.driver)
        self.logIn()
        self.changeLang("en")
    
    # Destructor
    def __del__(self):
        self.driver.close()
        print("This session has ended")


    # Checking if the user would like to continue the test
    def askCont(self):
        cont = ""
        while True:
            print("Would you like to continue? (y/n)")
            cont = input().lower()
            if cont == "y": return
            if cont == "n": self.__del__()

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
        #print("Changed language to", lang.upper())
        return
    
    # Click on Coordinates
    def clickAtCoordinates(self, x, y, doubleClick=False):
        self.waitFor("tag_name", "body")
        self.actions.move_to_element_with_offset(self.driver.find_element(By.TAG_NAME, "body"), 0, 0).perform()
        if doubleClick: self.actions.move_by_offset(x, y).double_click().perform()
        else: self.actions.move_by_offset(x, y).click().perform()
        return
    
    # Click and Hold Between Two Elements
    def clickAndHold(self, element1, element2, by1='css_selector', by2='css_selector'):
        by1 = by1.upper(); by2 = by2.upper()
        self.actions.move_to_element(self.driver.find_element(eval(f"By.{by1}"), element1)).perform()
        self.actions.move_to_element(self.driver.find_element(eval(f"By.{by2}"), element2)).click_and_hold().perform()
        return

    # Click on an element (Includes waiting for)
    def clickOn(self, by, path):
        by = by.upper()
        self.waitFor(by, path, True)
        try:
            self.driver.find_element(eval("By."+ by), path).click()
        except:
            time.sleep(2)
            self.driver.find_element(eval(f"By.{by}"), path).click()
        return
    


    # Drag and Drop by Coordinates
    def dragAndDropCoordinates(self, x1, y1, x2, y2):
        self.actions.move_to_element_with_offset(self.driver.find_element(By.TAG_NAME, "body"), x1, y1).perform()
        self.actions.click_and_hold().move_by_offset(x2-x1, y2-y1).pause(0.25).release()
        return

    # Giving an Error
    def error(self, where, lang, expected, received):
        print(f"ERROR!\n Unexpected result for {where} in {lang}.\n Expected '{expected}' but got '{received}'")
        self.askCont()
        return
    
    # Getting an Attribute of an Element
    def getAtt(self, by, path, att):
        by = by.upper()
        self.waitFor(by, path)
        return self.driver.find_element(eval(f"By.{by}"), path).get_attribute(att)
    
    # Get Coordinates of an element
    def getCoordinates(self, element):
        coordinates = element.location
        return [coordinates.x, coordinates.y]
    
    # Returning the Text of a Field
    def getText(self, by, path):
        by = by.upper()
        self.waitFor(by, path)
        return self.driver.find_element(eval("By."+by), path).text
    
    # Returning the title of the page
    def getTitle(self):
        print(self.driver.title)
    
    # Going to a Page
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
    
    # Press 'OK' on an Alert
    def okAlert(self):
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        self.driver.switch_to.alert.accept()
    
    # Reloading the Page
    def reload(self):
        time.sleep(0.5)
        self.driver.refresh()
        time.sleep(0.5)
        return
    
    # Switch iFrame
    def switchIframe(self, path=None):
        if not path:
            self.driver.switch_to.default_content()
            return
        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, path))
        return
    
    # Switch Window Focus
    def switchWindow(self, anchored):
        if anchored: currentHandle = self.driver.current_window_handle
        else: currentHandle = False
        for handle in self.driver.window_handles:
            if handle != currentHandle:
                self.driver.switch_to.window(handle)
                return
        return

    # Wait for Function
    def waitFor(self, by, element, clickable=False, firstTime=True):
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
            wait = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((eval("By." + by), element))
            )
            return
        except:
            if firstTime: 
                self.reload
                self.waitFor(by, element, False, False)
            print("There seems to have been an error.")
            print(f"Looking for {by} of {element}.")
            confirm = input("Press enter to continue\n")
            if confirm != "": self.driver.quit()
            return
    
    # Waiting for an Element to Disappear
    def waitForDisappear(self, by, path):
        by = by.upper()
        try:
            wait =  WebDriverWait(self.driver, 20).until(
                EC.invisibility_of_element(eval(f"By.{by}"), path)
                )
            return
        except:
            print(f"Either {by} of {path} not detected, or it didn't disappear.")
            self.askCont()
            return
