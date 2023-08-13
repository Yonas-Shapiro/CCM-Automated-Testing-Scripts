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
        if inSDL: self.changeLang("en")
        else: self.changeLang("fr")

        # Navigating to the folder
        self.driver.get(self.smartHome)
        if self.SDL: self.clickOn("xpath", "//a[@title='Other Items']"); self.clickOn("xpath", "(//span[@title='Folder'])[2]")
        else: self.clickOn("xpath", "//a[@title='Autres éléments']"); self.clickOn("xpath", "(//span[@title='Dossier'])[2]")
        #self.clickOn("xpath", "(//polygon[@fill='#DD8100'])[2]")

        # Creating the Workspace
        self.clickOn("xpath", "(//circle[@class='csui-icon-v2-state'])[2]")
        self.clickOn("link_text", "BW WS Template")


        # Filling in the information

        # Name
        self.clickOn("xpath", "//path[@d includes 'M12']")
        if nameSDL: self.driver.find_element(By.ID, "input-en_US").send_keys(f"BW {num} EN")
        if nameUDL: self.driver.find_element(By.ID, "input-fr").send_keys(f"BW {num} FR")
        self.clickOn("xpath", "//path[@id includes 'M12']")

        # Description
        self.driver.find_element(By.ID, "alpaca5").send_keys(Keys.TAB + Keys.ENTER)
        if nameSDL: self.driver.find_element(By.ID, "input-en_US").send_keys(f"BW {num}" + Keys.ENTER + "EN" + Keys.ENTER + "Description")
        if nameUDL: self.driver.find_element(By.ID, "input-fr").send_keys(f"BW {num}" + Keys.ENTER + "FR" + Keys.ENTER + "Description")
        self.clickOn("xpath", "//path[@id includes 'M12']")

        # Attributes
        self.driver.find_element(By.ID, "alpaca6").send_keys(f"BW {num} {self.SDL}")
        self.clickOn("id", "alpaca8")
        self.driver.find_element(By.ID, "alpaca8").send_keys(Keys.DOWN + Keys.DOWN + Keys.DOWN + Keys.ENTER)
        self.driver.find_element(By.ID, "alpaca10").send_keys("TML" + Keys.DOWN + "Not multilingual")

        # Saving the Workspace
        self.clickOn("id", "okButton")

        # Opening the Properties Tab
        if (inSDL and nameSDL) or (not inSDL and not nameUDL):
            self.clickOn("xpath", f"//span[text()='BW {num} EN]")
        else:
            self.clickOn("xpath", f"//span[text()='BW {num} FR]")
        self.clickOn("id", "dropdownMenuButton51087")
        self.clickOn("link_text", "Properties")

        # Examining the Results

        # SDL First
        self.changeLang('en')
        
        # Name
        val = self.getText("xpath", "(//span[@title contains 'click to edit'])[1]")
        if nameSDL:
            if val != f"BW {num} EN":
                self.error("SDL", f"BW {num} EN", val)
        else:
            if val != f"BW {num} FR":
                self.error("SDL", f"BW {num} FR", val)
        
        # Text Field
        val = self.getText("xpath", "(//div[@class = 'btn-container'])[11]")
        if inSDL:
            if val != f"EN {num}":
                self.error("SDL", f"EN {num}", val)
        else:
            if val != f"FR {num}":
                self.error("SDL", f"FR {num}", val)
        
        # Text Pop-up
        val = self.getText("xpath", "(//div[@class = 'btn-container'])[12]")
        if val != "three":
            self.error("SDL", "three", val)

        # Text Multiline
        val = self.getText("xpath", "(//div[@class = 'btn-container'])[13]")
        if val != "TML\nNot multilingual":
            self.error("SDL", "TML\nNot multilingual", val)

        # UDL Next
        self.changeLang("fr")

        # Name
        val = self.getText("xpath", "(//span[@title contains 'click to edit'])[1]")
        if nameUDL:
            if val != f"BW {num} FR":
                self.error("UDL", f"BW {num} FR", val)
        else:
            if val != f"BW {num} EN":
                self.error("UDL", f"BW {num} EN", val)
        
        # Text Field
        val = self.getText("xpath", "(//div[@class = 'btn-container'])[11]")
        if inSDL:
            if val != f"EN {num}":
                self.error("UDL", f"EN {num}", val)
        else:
            if val != f"FR {num}":
                self.error("UDL", f"FR {num}", val)
        
        # Text Pop-up
        val = self.getText("xpath", "(//div[@class = 'btn-container'])[12]")
        if val != "trois":
            self.error("UDL", "three", val)

        # Text Multiline
        val = self.getText("xpath", "(//div[@class = 'btn-container'])[13]")
        if val != "TML\nNot multilingual":
            self.error("UDL", "TML\nNot multilingual", val)

        # Done with the Workspace
        print(f"BW {num} passed.")
        if pause:
            self.askCont()
        return
