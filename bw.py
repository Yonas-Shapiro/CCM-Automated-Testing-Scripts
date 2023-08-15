from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import time

from basics import basics

class businessWorkspace(basics):

    # Multilingualizing the Workspace
    def multilingualizeWorkspace(self):
        # Going to the Categories Page
        self.goTo("ll&objType=133&objAction=browse")

        # Getting into the multilingual tab of the workspace
        self.clickOn("xpath", "//a[@title='Function menu for BW WS']")
        self.clickOn("xpath", "//*[contains(@id, 'menuItem_Properties')]")
        self.clickOn("link_text", "Multilingual")

        # Multilingualizing the workspace
        Select(self.driver.find_element(By.ID, "editMLDestLang")).select_by_value("fr")
        self.clickOn("id", "_1_1_2")
        self.clickOn("id", "_1_1_3")
        self.driver.find_element(By.NAME, "_1_1_2_Dest").send_keys("tf fr")
        self.driver.find_element(By.NAME, "_1_1_4_Dest").send_keys("tml fr")
        self.clickOn("xpath", "//input[@name='radTransType' and @value='1']")
        self.driver.find_element(By.NAME, "_1_1_3_Dest_pp").clear()
        self.driver.find_element(By.NAME, "_1_1_3_Dest_pp").send_keys("un" + Keys.RETURN + "deux" + Keys.RETURN + "trois")
        self.clickOn("id", "btnSave")
        return

    # Creating a workspace in Classic View
    def classicBW(self, num, inSDL, nameSDL, nameUDL, attSDL, attUDL, pause):
        # Ensuring num is a string
        num = str(num)

        # Starting in the correct language and then navigating to the BW folder
        if inSDL:
            self.changeLang("en")
            self.goTo()
            self.clickOn("link_text", "Other Items")
        else:
            self.changeLang("fr")
            self.goTo()
            self.clickOn("link_text", "Autres éléments")
        self.clickOn("xpath", "//a[@class='browseItemNameContainer' and contains (@id, 'node')]")
        self.clickOn("id", "addItemMenu0Head")
        self.clickOn("id", "menuItem_848")

        # Making the number a two-digit code (01-99) for easier sorting due to alphabetizing
        if int(num) < 10:
            name = "BW 0" + num
        else:
            name = "BW " + num

        # Giving the workspace a name
        self.clickOn("id", "nameGlobal")
        self.driver.find_element(By.ID, "meta_name_en_US").clear()
        if nameSDL:
            self.driver.find_element(By.ID, "meta_name_en_US").send_keys(name + " EN")
        if nameUDL:
            self.driver.find_element(By.ID, "meta_name_fr").send_keys(name + " FR")

        # Giving the workspace a description        
        self.clickOn("link_text", "Description")
        if nameSDL:
            self.driver.find_element(By.ID, "meta_comment_en_US").send_keys(name + Keys.ENTER + "EN" + Keys.ENTER + "Description")
        if nameUDL:
            self.driver.find_element(By.ID, "meta_comment_fr").send_keys(name + Keys.ENTER + "FR" + Keys.ENTER + "Description")
        self.clickOn("xpath", "//button[text()='OK']")

        # Giving the workspace Metadata
        self.clickOn("xpath", "//*[@value='Next >>']")

        # Text Field
        self.clickOn("id", "_1_1_2_1Global")
        if attSDL:
            self.driver.find_element(By.ID, "mle__1_1_2_1_en_US").send_keys("EN " + num)
        if attUDL:
            self.driver.find_element(By.ID, "mle__1_1_2_1_fr").send_keys("FR " + num)
        self.clickOn("id", "mlEditBtnSave")
        
        # Text Popup
        Select(self.driver.find_element(By.ID, "_1_1_3_1")).select_by_index(3)

        # Text Multiline
        self.driver.find_element(By.ID, "_1_1_4_1").send_keys("TML" + Keys.ENTER + "Not multilingual")

        # Moving on (every 2nd run ends "early")
        if int(num)%2==1:
            self.clickOn("xpath", "//*[@value='Next >>']")
        self.clickOn("id", "FinishButton")

        # Examining the results

        # BWs 7-10 are expected to error out
        if inSDL==False and attUDL==False:
            self.waitFor("link_text", "Quit Wizard")
            print("BW", num, "passed with the expected result of an error")
            return

        # Ensuring proper values are displayed
        self.clickOn("xpath", "//*[@value='Continue']")
        time.sleep(1)
        self.changeLang("en")

        # Checking the name
        val = self.getText("id", "otsapwkspPanel_panelTitle")
        if nameSDL:
            if val != (name + " EN"): 
                self.error("BW Name", "SDL", (name + " EN"), val)
        else:
            if val != (name + " FR"):
                self.error("BW Name", "SDL", (name + " FR"), val)
        
        # Checking the Text Field
        val = self.getText("xpath", "(//div[@class='xecmsap_attribute_value'])[1]")[2:-1]
        #self.getText("xpath", f"//li[@class='xecmsap_attribute_value' and (@title='EN {num}')]")
        if attSDL:
            if val != ("EN " + num):
                self.error("Text Field", "SDL", ("EN " + num), val)
        else:
            if val != ("FR " + num):
                self.error("Text Field", "SDL", ("FR " + num), val)

        # Checking the Text Popup
        val = self.getText("xpath", "(//div[@class='xecmsap_attribute_value'])[2]")[2:-1]
        if val != "three":
            self.error("Text Popup", "SDL", "three", val)
        
        # Checking the Text Multiline
        val = self.getText("xpath", "(//div[@class='xecmsap_attribute_value'])[3]")[2:-1]
        if val != "TML Not multilingual":
            self.error("Text Multiline", "SDL", "TML Not multilingual", val)
        
        # Checking in UDL
        self.changeLang("fr")
        
        # Checking the name
        val = self.getText("class_name", "xecmTitleBar")
        if nameUDL:
            if val != (name + " FR"):
                self.error("BW Name", "UDL", (name + " FR"), val)
        else:
            if val != (name + " EN"):
                self.error("BW Name", "UDL", (name + " EN"), val)
        
        # Checking the Text Field
        # Text Field does not appear in UDL if no UDL value is provided, so additional measures must be taken to insure the proper field is being checked.
        check = 1
        if attUDL:
            val = self.getText("xpath", f"(//div[@class='xecmsap_attribute_value'])[{check}]")[2:-1]
            if val != ("FR " + num):
                self.error("Text Field", "UDL", ("FR " + num), val)
            check += 1

        # Checking the Text Popup
        val = self.getText("xpath", f"(//div[@class='xecmsap_attribute_value'])[{check}]")[2:-1]
        check += 1
        if val != "trois":
            self.error("Text Popup", "UDL", "trois", val)
        
        # Checking the Text Multiline
        val = self.getText("xpath", f"(//div[@class='xecmsap_attribute_value'])[{check}]")[2:-1]
        if val != "TML Not multilingual":
            self.error("Text Multiline", "UDL", "TML Not multilingual", val)

        # Done with the workspace
        print(f"{name} passed.")
        if pause:
            self.askCont()
        return
    


    # Creating a Business Workspace in Smart View
    def smartBW(self, num, inSDL, nameSDL, nameUDL, pause):
        # Ensuring num is a string
        num = str(num)

        # Starting in the right language
        if inSDL and not self.SDL: self.changeLang("en")
        if not inSDL and self.SDL: self.changeLang("fr")

        # Navigating to the folder
        self.driver.get(self.smartHome)
        if self.SDL:
            self.driver.get(self.getAtt("xpath", "//a[@title='Other Items']", "href"))
            self.driver.get(self.getAtt("xpath", "//a[@title='Business Workspaces']", "href"))
        else:
            self.driver.get(self.getAtt("xpath", "//a[@title='Autres éléments']", "href"))
            self.driver.get(self.getAtt("xpath", "//a[@title='Business Workspaces']", "href"))

        # Creating the Workspace
        self.clickOn("xpath", "//a[@title='Add item']")
        self.clickOn("link_text", "BW WS Template")


        # Filling in the information

        # Name
        self.clickOn("xpath", "(//button[@title='Edit in multiple languages'])[1]")
        if nameSDL: self.driver.find_element(By.ID, "input-en_US").send_keys(f"BW {num} EN")
        if nameUDL: self.driver.find_element(By.ID, "input-fr").send_keys(f"BW {num} FR")
        self.clickOn("class_name", "globe-icon-mask")

        # Description
        self.driver.find_element(By.ID, "alpaca5").send_keys(Keys.TAB + Keys.ENTER)
        if nameSDL: self.driver.find_element(By.ID, "input-en_US").send_keys(f"BW {num}" + Keys.ENTER + "EN" + Keys.ENTER + "Description")
        if nameUDL: self.driver.find_element(By.ID, "input-fr").send_keys(f"BW {num}" + Keys.ENTER + "FR" + Keys.ENTER + "Description")
        self.clickOn("class_name", "globe-icon-mask")

        # Attributes
        if self.SDL: self.driver.find_element(By.ID, "alpaca6").send_keys(f"EN {num}")
        else: self.driver.find_element(By.ID, "alpaca6").send_keys(f"FR {num}")
        self.clickOn("id", "alpaca8")
        self.driver.find_element(By.ID, "alpaca8").send_keys(Keys.DOWN + Keys.DOWN + Keys.DOWN + Keys.DOWN + Keys.ENTER)
        self.driver.find_element(By.ID, "alpaca10").send_keys("TML" + Keys.ENTER + "Not multilingual")

        # Saving the Workspace
        self.clickOn("id", "okButton")

        # Opening the Properties Tab
        if (inSDL and nameSDL) or (not inSDL and not nameUDL):
            self.driver.get(self.getAtt("xpath", f"//a[@title='BW {num} EN']", "href"))
        else:
            self.driver.get(self.getAtt("xpath", f"//a[@title='BW {num} FR']", "href"))
        self.clickOn("xpath", "//span[@title='Show more']")
        self.clickOn("link_text", "Properties")

        # Examining the Results

        # SDL First
        if not self.SDL: self.changeLang('en')
        
        # Name
        val = self.getText("xpath", "(//span[contains(@title, 'click to edit')])[1]")
        if nameSDL:
            if val != f"BW {num} EN":
                self.error("Name", "SDL", f"BW {num} EN", val)
        else:
            if val != f"BW {num} FR":
                self.error("Name", "SDL", f"BW {num} FR", val)
        
        # Text Field
        val = self.getText("xpath", "(//div[@class = 'btn-container'])[11]")
        if inSDL:
            if val != f"EN {num}":
                self.error("Text Field", "SDL", f"EN {num}", val)
        else:
            if val != f"FR {num}":
                self.error("Text Field", "SDL", f"FR {num}", val)
        
        # Text Pop-up
        val = self.getText("xpath", "(//div[@class = 'btn-container'])[12]")
        if val != "three":
            self.error("Text Pop-up", "SDL", "three", val)

        # Text Multiline
        val = self.getText("xpath", "(//div[@class = 'btn-container'])[13]")
        val = val.strip()
        if val != "TML\nNot multilingual":
            self.error("Text Multiline", "SDL", "TML\nNot multilingual", val)

        # UDL Next
        self.changeLang("fr")

        # Name
        val = self.getText("xpath", "(//span[contains(@title, 'click to edit')])[1]")
        if nameUDL:
            if val != f"BW {num} FR":
                self.error("Name", "UDL", f"BW {num} FR", val)
        else:
            if val != f"BW {num} EN":
                self.error("Name", "UDL", f"BW {num} EN", val)
        
        # Text Field
        val = self.getText("xpath", "(//div[@class = 'btn-container'])[11]")
        if inSDL:
            if val != "Add value":
                self.error("Text Field", "UDL", "Add value", val)
        else:
            if val != f"FR {num}":
                self.error("Text Field", "UDL", f"FR {num}", val)
        
        # Text Pop-up
        val = self.getText("xpath", "(//div[@class = 'btn-container'])[12]")
        if val != "trois":
            self.error("Text Popup", "UDL", "three", val)

        # Text Multiline
        val = self.getText("xpath", "(//div[@class = 'btn-container'])[13]")
        val = val.strip()
        if val != "TML\nNot multilingual":
            self.error("Text Multiline", "UDL", "TML\nNot multilingual", val)

        # Done with the Workspace
        print(f"BW {num} passed.")
        if pause:
            self.askCont()
        return




    # Creating a Poll
    def searchQuery(self, inSDL, searchTerm, pause):

        # Starting in the Correct Language
        if inSDL and not self.SDL: self.changeLang("en")
        if not inSDL and self.SDL: self.changeLang("fr")

        # Creating the Search
        self.goTo("ll&objType=258&objAction=searchprompt")

        # Entering the Information
        self.driver.find_element(By.XPATH, "(//input[@class='valueEditable'])[1]").send_keys(searchTerm)
        self.clickOn("id", "searchBtnMiddle")

        # Getting the results
        initResults = self.driver.find_elements(By.XPATH, "//span[contains(@id, 'searchResult')]")
        results = []
        for result in initResults:
            results.append(result.text)

        # Saving the Search Query
        self.clickOn("id", "SearchFunctionMenuText_ahref")
        self.clickOn("link_text", "Save Search Query")
        searchName = f"{searchTerm} Search"
        self.driver.find_element(By.ID, "name").send_keys(searchName)

        # Getting the Correct Location (Enterprise)
        mainHandle = self.driver.current_window_handle
        if self.getText("id", "CTT_Path") != "Enterprise" or "Content Server:Enterprise":
            self.clickOn("xpath", "//input[@name='CTT_Button']")
            for handle in self.driver.window_handles:
                if handle != mainHandle:
                    popup = handle
            self.driver.switch_to.window(popup)
            self.clickOn("class_name", "selectArrow")
            self.clickOn("xpath", "(//div[@class='menuItem'])[1]")
            self.clickOn("xpath", "(//a[@href='#'])[4]")
            self.driver.switch_to.window(mainHandle)
            popup = False

        self.clickOn("id", "addButton")
        # Fixing a Potential Category "<not determined>"
        if len(self.driver.window_handles) > 1:
            mainHandle = self.driver.current_window_handle
            for handle in self.driver.window_handles:
                if handle != mainHandle:
                    self.driver.switch_to.window(handle)
                    self.clickOn("xpath", "//input[@name='done']")
                    self.driver.switch_to.window(mainHandle)
                    self.clickOn("id", "addButton")



        # Confirming values

        # SDL Classic View
        if self.SDL == False: self.changeLang("en")
        self.goTo()
        self.clickOn("link_text", searchName)

        tempVals = self.driver.find_elements(By.XPATH, "//span[contains(@id, 'searchResult')]")
        vals = []
        for val in tempVals: vals.append(val.text)

        if vals != results:
            self.error(searchName, "SDL", results, vals)
        
        # UDL Classic View
        self.changeLang("fr")
        self.goTo()
        self.clickOn("link_text", searchName)

        tempValsFR = self.driver.find_elements(By.XPATH, "//span[contains(@id, 'searchResult')]")
        valsFR = []
        for val in tempValsFR: valsFR.append(val.text)

        if valsFR != results:
            self.error(searchName, "UDL", results, valsFR)

        # UDL Smart View
        self.driver.get(self.smartHome)
        self.driver.get(self.getAtt("link_text", searchName, "href"))

        self.waitFor("xpath", "//div[@class='csui-search-item-name ']")
        tempValsFRSV = self.driver.find_elements(By.XPATH, "//div[@class='csui-search-item-name ']")
        valsFRSV = []
        for val in tempValsFRSV: valsFRSV.append(val.text)

        if valsFRSV != results:
            self.error(searchName, "UDL", results, valsFRSV)
        
        # SDL Smart View
        self.changeLang("en")
        self.driver.get(self.smartHome)
        self.driver.get(self.getAtt("link_text", searchName, "href"))

        self.waitFor("xpath", "//div[@class='csui-search-item-name ']")
        tempValsSV = self.driver.find_elements(By.XPATH, "//div[@class='csui-search-item-name ']")
        valsSV = []
        for val in tempValsSV: valsSV.append(val.text)

        if valsSV != results:
            self.error(searchName, "SDL", results, valsSV)
        

        # If Completed, Output Message
        print(f"Search Query for {searchTerm} passed.")
        if pause:
            self.askCont()
        return