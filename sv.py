from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

from basics import basics

class svTest(basics):

    # Init to get Basic Information
    def __init__(self, VMnum):
        basics.__init__(VMnum)

        # Getting the 'Standard Basic Folder' in both Smart View and Classic View
        self.goTo(self.smartHome)
        self.svFolderClick("Test Data")
        self.standardBasic = self.driver.get(self.getAtt("xpath", "//a[@title='Standard Basic]", "href"))
        self.goTo()
        self.clickOn("link_text", "Test Data")
        self.clickOn("link_text", "Standard Basic")
        self.classicStandardBasic = self.driver.current_url

    


    # Create a Folder and Give Category Attributes
    def createFolder(self, num, inSDL, infoSDL, infoUDL, pause):

        # Starting in the Right Language
        if inSDL and not self.SDL: self.changeLang("en")
        elif not inSDL and self.SDL: self.changeLang("fr")

        # Going to the Standard Basic Folder
        self.goTo(self.standardBasic)

        # Creating the Folder
        self.clickOn("xpath", "//a[@title='Add item']")
        if inSDL: self.clickOn("link_text", "Folder")
        else: self.clickOn("link_text", "Dossier")

        # Adding Basic Information (Non-Category)
        self.clickOn("xpath", "//div[@title='Edit in multiple languages']")

        # Name of the Folder
        if infoSDL: self.driver.find_element(By.ID, "input-en_US").send_keys(f"SV-F{num} EN")
        if infoUDL: self.driver.find_element(By.ID, "input-fr").send_keys(f"SV-F{num} FR")
        
        # Saving the Folder
        self.clickOn("xpath", "//div[@title='Edit in multiple languages']")
        self.clickOn("xpath", "//button[@title='Save']")


        # Adding the Metadata
        if (inSDL and infoSDL) or not infoUDL: self.svMetadata(f"SV-F{num} EN")
        else: self.svMetadata(f"SV-F{num} FR")

        # Multilingual Text: Field
        self.clickOn("class_name", "smartemlc-icon-edit")
        if inSDL:
            if infoSDL: self.driver.find_element(By.XPATH, "(//input[@class='`valueml_${locale.LanguageCode}`'])[1]").send_keys(f"EN {num}")
            if infoUDL: self.driver.find_element(By.XPATH, "(//input[@class='`valueml_${locale.LanguageCode}`'])[4]").send_keys(f"FR {num}")

        if not inSDL:
            if infoSDL: self.driver.find_element(By.XPATH, "(//input[@class='`valueml_${locale.LanguageCode}`'])[4]").send_keys(f"EN {num}")
            if infoUDL: self.driver.find_element(By.XPATH, "(//input[@class='`valueml_${locale.LanguageCode}`'])[1]").send_keys(f"FR {num}")

        self.clickOn("xpath", "//button[text()='Save']")

        # Integer Field
        self.clickOn("xpath", "//span[text()='Add value']")
        self.driver.find_element(By.ID, "alpaca12").send_keys(str(num)*3)

        # Date Dropdown
        self.clickOn("xpath", "(//span[text()='Select value])[1]")
        self.clickOn("xpath", "//span[text()='11/20/2023']")

        # Date Selection
        self.clickOn("xpath", "//span[text()='Add date']")
        self.driver.find_element(By.ID, "alpaca6").send_keys(f"0{num}/01/2000")

        # Text: Multiline
        self.clickOn("xpath", "//span[text()='Add text']")
        self.driver.find_element(By.ID, "alpaca14").send_keys(f"TML{Keys.ENTER}Not multilingual")

        # Text: Popup
        self.clickOn("xpath", "//span[text()='Select value']")

        val = num%3

        if val==1: colour = "Red"; colourFR = "Rouge2"
        elif val==2: colour = "Green"; colourFR = "Vert"
        else: colour == "Blue"; colourFR = "Bleu2"

        if inSDL: self.clickOn("link_text", colour)
        else: self.clickOn("link_text", colourFR)

        # User
        self.clickOn("xpath", "//span[text()='Add user']")
        self.driver.find_element("id", "alpaca16").send_keys("Admin" + Keys.ENTER)
        self.clickOn("class_name", "alpaca-control")

        # Examining the results
        self.reload()

        # SDL First
        if not inSDL: self.changeLang("en")

        # Date Field
        val = self.getText("xpath", "(//div[@class='btn-container'])[9]")
        if val != f"0{num}/01/2000":
            self.error("Date Field", "SDL", f"0{num}/01/2000", val)

        # Date Dropdown
        val = self.getText("xpath", "(//div[@class='btn-container'])[10]")
        if val != "11/20/2023":
            self.error("Date Popup", "SDL", "11/20/2023", val)

        # Integer Field
        val = self.getText("xpath", "(//div[@class='btn-container'])[11]")
        if val != str(num)*3:
            self.error("Integer Field", "SDL", str(num)*3, val)
        
        # Text Field (Multilingual)
        val = self.getText("xpath", "(//div[@class='btn-container'])[12]")
        if infoSDL:
            if val != f"EN {num}":
                self.error("Text Field (multilingual)", "SDL", f"EN {num}", val)
        else:
            if val != f"FR {num}":
                self.error("Text Field (multilingual)", "SDL" ,f"FR {num}", val)
        
        # Text Multiline
        val = self.getText("xpath", "(//div[@class='btn-container'])[13]")
        if val != "TML\nNot multilingual":
            self.error("Text Multiline", "SDL", f"TML{Keys.ENTER}Not multilingual", val)
        
        # Text Popup
        val = self.getText("xpath", "(//div[@class='btn-container'])[14]")
        if val != colour:
            self.error("Text Popup", "SDL", colour, val)
        
        # User Field
        val = self.getText("xpath", "(//div[@class='btn-container'])[15]")
        if val != "Admin":
            self.error("User Field", "SDL", "Admin", val)
        

        # UDL
        self.changeLang("fr")

        # Date Field
        val = self.getText("xpath", "(//div[@class='btn-container'])[9]")
        if val != f"0{num}/01/2000":
            self.error("Date Field", "UDL", f"0{num}/01/2000", val)

        # Date Dropdown
        val = self.getText("xpath", "(//div[@class='btn-container'])[10]")
        if val != "11/20/2023":
            self.error("Date Popup", "UDL", "11/20/2023", val)

        # Integer Field
        val = self.getText("xpath", "(//div[@class='btn-container'])[11]")
        if val != str(num)*3:
            self.error("Integer Field", "UDL", str(num)*3, val)
        
        # Text Field (Multilingual)
        val = self.getText("xpath", "(//div[@class='btn-container'])[12]")
        if infoUDL:
            if val != f"FR {num}":
                self.error("Text Field (multilingual)", "UDL", f"FR {num}", val)
        else:
            if val != "Add value":
                self.error("Text Field (multilingual)", "UDL" , "Add value", val)
        
        # Text Multiline
        val = self.getText("xpath", "(//div[@class='btn-container'])[13]")
        if val != "TML\nNot multilingual":
            self.error("Text Multiline", "UDL", f"TML{Keys.ENTER}Not multilingual", val)
        
        # Text Popup
        val = self.getText("xpath", "(//div[@class='btn-container'])[14]")
        if val != colourFR:
            self.error("Text Popup", "UDL", colourFR, val)
        
        # User Field
        val = self.getText("xpath", "(//div[@class='btn-container'])[15]")
        if val != "Admin":
            self.error("User Field", "UDL", "Admin", val)

        
        # Checking in Classic View
        self.goTo(self.classicStandardBasic)
        self.clickOn("xpath", f"//a[contains(@title, 'Function menu for SV-F{num})]")
        self.clickOn("link_text", "Properties")
        self.clickOn("link_text", "Categories")

        # Date Field
        val = self.getText("id", "_datepicker__1_1_2_1")
        if val != f"0{num}/01/2000":
            self.error("Date Field", "UDL", f"0{num}/01/2000", val)

        # Date Dropdown
        val = self.getText("id", "_1_1_3_1")
        if val != "11/20/2023":
            self.error("Date Popup", "UDL", "11/20/2023", val)

        # Integer Field
        val = self.getText("id", "_1_1_5_1")
        if val != str(num)*3:
            self.error("Integer Field", "UDL", str(num)*3, val)
        
        # Text Field (Multilingual)
        val = self.getText("id", "_1_1_6_1")
        if infoUDL:
            if val != f"FR {num}":
                self.error("Text Field (multilingual)", "UDL", f"FR {num}", val)
        else:
            if val != "Add value":
                self.error("Text Field (multilingual)", "UDL" , "Add value", val)
        
        # Text Multiline
        val = self.getText("id", "_1_1_7_1")
        if val != "TML\nNot multilingual":
            self.error("Text Multiline", "UDL", f"TML{Keys.ENTER}Not multilingual", val)
        
        # Text Popup
        val = self.getText("id", "_1_1_8_1")
        if val != colourFR:
            self.error("Text Popup", "UDL", colourFR, val)
        
        # User Field
        val = self.getText("id", "_1_1_9_1_Name")
        if val != "Admin":
            self.error("User Field", "UDL", "Admin", val)


        # SDL
        self.changeLang("en")

        # Date Field
        val = self.getText("id", "_datepicker__1_1_2_1")
        if val != f"0{num}/01/2000":
            self.error("Date Field", "SDL", f"0{num}/01/2000", val)

        # Date Dropdown
        val = self.getText("id", "_1_1_3_1")
        if val != "11/20/2023":
            self.error("Date Popup", "SDL", "11/20/2023", val)

        # Integer Field
        val = self.getText("id", "_1_1_5_1")
        if val != str(num)*3:
            self.error("Integer Field", "SDL", str(num)*3, val)
        
        # Text Field (Multilingual)
        val = self.getText("id", "_1_1_6_1")
        if infoSDL:
            if val != f"EN {num}":
                self.error("Text Field (multilingual)", "SDL", f"EN {num}", val)
        else:
            if val != f"FR {num}":
                self.error("Text Field (multilingual)", "SDL" , f"FR {num}", val)
        
        # Text Multiline
        val = self.getText("id", "_1_1_7_1")
        if val != "TML\nNot multilingual":
            self.error("Text Multiline", "SDL", f"TML{Keys.ENTER}Not multilingual", val)
        
        # Text Popup
        val = self.getText("id", "_1_1_8_1")
        if val != colour:
            self.error("Text Popup", "SDL", colour, val)
        
        # User Field
        val = self.getText("id", "_1_1_9_1_Name")
        if val != "Admin":
            self.error("User Field", "SDL", "Admin", val)

        
        # Print Passed Message
        print(f"SV-F{num} passed.")
        if pause:
            self.askCont()
        return