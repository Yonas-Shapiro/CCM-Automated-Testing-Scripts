from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

from basics import basics

class businessWorkspace(basics):

    # Init to get Basic Information (Optimization)
    def __init__(self, VMnum):
        basics.__init__(VMnum)

        # Getting Classic BW Folder URL
        self.goTo()
        self.clickOn("link_text", "Other Items")
        self.clickOn("xpath", "//a[@class='browseItemNameContainer' and contains (@id, 'node')]")
        self.classicBWFolder = self.driver.current_url

        # Getting Smart BW Folder URL
        self.goTo(self.smartHome)
        self.svFolderClick("Other Items")
        self.smartBWFolder = self.getAtt("xpath", "//a[@title='Business Workspaces']", "href")




    # Multilingualizing the Workspace
    def multilingualizeWorkspace(self):

        # Going to SDL
        if not self.SDL: self.changeLang("en")

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

        # Printing out a Success Message
        print("Workspace Multilingualized.")
        return
    



    # Setting the Workspace up for Creation in Workflows
    def prepareForWorkflow(self):

        # Going to SDL
        if not self.SDL: self.changeLang("en")

        # Going to the Workspaces Page
        self.goTo("ll&objType=862&objAction=browse")

        # Getting into the Workspace Settings
        self.clickOn("link_text", "Workspace Types")
        self.clickOn("partial_link_text", "BW")

        # Automatic Naming
        self.driver.find_element(By.ID, "mlValue3").clear()
        self.driver.find_element(By.ID, "mlValue3").send_keys("BW ")
        self.driver.find_element(By.ID, "mlValue4").clear()
        self.driver.find_element(By.ID, "mlValue4").send_keys("BW ")

        # Inserting the Attributes to the Name

        # SDL
        self.clickOn("id", "insertAttr_mlLang3")
        self.clickOn("xpath", "//div[text()='BW WS:tf']")
        self.clickOn("id", "selectAttributeFormInsert")

        # UDL
        self.clickOn("id", "insertAttr_mlLang4")
        self.clickOn("xpath", "//div[text()='BW WS:tf']")
        self.clickOn("id", "selectAttributeFormInsert")

        # Only Clicking on the Checkbox if it is not Already Selected
        if not self.driver.find_element(By.ID, "doNameGenerationForEarlyWksp").is_selected():
            self.clickOn("id", "doNameGenerationForEarlyWksp")

        
        # Automatic Location

        # Getting the Location
        Select(self.driver.find_element(By.ID, "cbName1")).select_by_value("StaticNodeId")

        # If the Location is already there, skip
        if not "Business Workspaces" in self.getText("id", "xecmctrl_StaticNodeId_1_text"):
            self.clickOn("xpath", "//input[@name='xecmctrl_StaticNodeId_1_button']")
            self.switchWindow(True)
            self.clickOn("link_text", "Other Items")
            self.clickOn("xpath", "(//a[@href='#'])[3]")
            self.switchWindow(False)

        # Checking the "Use also for manual creation" Checkbox
        if not self.driver.find_element(By.ID, "useLocationForManualCreation").is_selected():
            self.clickOn("id", "useLocationForManualCreation")

        # Saving the Changes
        self.clickOn("id", "FORM_SAVE")

        # Printing out a 'Done' Message
        print("Workspace is prepared for Workflow creation.")
        return




    # Creating a Workspace in Classic View
    def classicBW(self, num, inSDL, nameSDL, nameUDL, attSDL, attUDL, pause):
        # Ensuring num is a string
        num = str(num)

        # Starting in the correct language and then navigating to the BW folder
        if inSDL and not self.SDL: self.changeLang("en")
        elif not inSDL and self.SDL: self.changeLang("fr")
        self.goTo(self.classicBWFolder)

        # Creating the Workspace
        self.clickOn("link_text", "Add Item")
        self.clickOn("link_text", "Business Workspace")

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

        # Checking SDL First
        if not self.SDL: self.changeLang("en")

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
        elif not inSDL and self.SDL: self.changeLang("fr")

        # Navigating to the folder
        self.driver.get(self.smartBWFolder)

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
        if (inSDL and nameSDL) or (not inSDL and not nameUDL): lang = 'EN'; 
        else: lang = 'FR'
        self.svMetadata(f"BW {num} {lang}")


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




    # Creating a Search Query
    def searchQuery(self, inSDL, searchTerm, pause):

        # Starting in the Correct Language
        if inSDL and not self.SDL: self.changeLang("en")
        elif not inSDL and self.SDL: self.changeLang("fr")

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
        if self.getText("id", "CTT_Path") != "Enterprise" or "Content Server:Enterprise":
            self.clickOn("xpath", "//input[@name='CTT_Button']")
            self.switchWindow(True)
            self.clickOn("class_name", "selectArrow")
            self.clickOn("xpath", "(//div[@class='menuItem'])[1]")
            self.clickOn("xpath", "(//a[@href='#'])[5]")
            self.switchWindow(False)

        self.clickOn("id", "addButton")
        # Fixing a Potential Category "<not determined>"
        if len(self.driver.window_handles) > 1:
            self.switchWindow(True)
            self.clickOn("xpath", "//input[@name='done']")
            self.switchWindow(False)
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
    



    # Creating a Workflow which Creates Workspaces
    def createWorkflowForBW(self):

        # Setting Language to SDL
        if not self.SDL: self.changeLang("en")

        # Going to the Folder
        self.goTo(self.classicBWFolder)

        # Creating the Workflow
        self.clickOn("link_text", "Add Item")
        self.clickOn("link_text", "Workflow Map")

        # Giving the Basic Information
        self.driver.find_element(By.ID, "name").send_keys("BW WF")
        self.driver.find_element(By.ID, "comment").send_keys(f"BW WF{Keys.ENTER}Description")
        self.clickOn("id", "addButton")

        # Getting into editing the Workflow
        self.clickOn("xpath", "//a[@title='Function menu for BW WF']")
        self.clickOn("link_text", "Edit")


        # Giving all the Values

        # General
        self.clickOn("link_text", "Map")
        self.clickOn("link_text", "General")
        self.driver.find_element(By.ID, "Description").send_keys(f"BW WF{Keys.ENTER}Description")
        self.clickOn("id", "InitMsg2")
        self.driver.find_element(By.ID, "CustomMsg").send_keys(f"BW WF{Keys.ENTER}Custom Message")
        self.clickOn("class_name", "saveButton")

        # Attributes
        self.clickOn("link_text", "Map")
        self.clickOn("link_text", "Attributes")
        self.clickOn("id", "1MSelectTitle")
        self.clickOn("link_text", "Text: Field")
        self.driver.find_element(By.ID, "AttrDisplayName").send_keys("tf")
        self.clickOn("class_name", "saveButton")
        self.clickOn("id", "1MSelectTitle")
        self.clickOn("link_text", "Text: Popup")
        self.driver.find_element(By.ID, "AttrDisplayName").send_keys("tp")
        self.driver.find_element(By.ID, "validValues").send_keys(f"one{Keys.ENTER}two{Keys.ENTER}three")
        self.clickOn("class_name", "saveButton")
        self.clickOn("id", "1MSelectTitle")
        self.clickOn("link_text", "Text: MultiLine")
        self.driver.find_element(By.ID, "AttrDisplayName").send_keys("tml")
        self.clickOn("class_name", "saveButton")
        time.sleep(0.5)
        self.clickOn("class_name", "saveButton")

        # Multilingualizing the Attributes
        self.clickOn("link_text", "Map")
        self.clickOn("link_text", "Attribute Translation")
        Select(self.driver.find_element(By.ID, "editMLDestLang")).select_by_value("fr")
        self.clickOn("id", "_1_1_2")
        self.clickOn("id", "_1_1_3")
        self.driver.find_element(By.XPATH, "//input[@name='_1_1_2_Dest']").send_keys("TF FR")
        self.driver.find_element(By.XPATH, "//input[@name='_1_1_4_Dest']").send_keys("TML FR")
        self.clickOn("xpath", "//input[@name='radTransType' and @value='1']")
        self.driver.find_element(By.XPATH, "//textarea[@name='_1_1_3_Dest_pp']").clear()
        self.driver.find_element(By.XPATH, "//textarea[@name='_1_1_3_Dest_pp']").send_keys(f"un{Keys.ENTER}deux{Keys.ENTER}trois")
        self.clickOn("id", "btnSave")
        self.clickOn("link_text", "BW WF")

        # Asking User to Finish Creating the Workflow.
        print("Please finish creating the workflow.")
        print("To do this, create a 'Create Workspace' step, fill in the necessary information and edit the workflow to initiate in classic view.")
        self.askCont()


        # Ensuring the Map is Saved
        self.clickOn("link_text", "Map")
        self.clickOn("link_text", "Save")
        self.okAlert()

        # Return with Success Message
        print("Workflow for Business Workspace creation created.")
        return




    # Creating a Business Workspace Via a Workflow
    def createBWWF(self, num, inSDL, pause):
        
        # Getting to the Correct Language
        if inSDL and not self.SDL: self.changeLang("en")
        elif not inSDL and self.SDL: self.changeLang("fr")

        # Getting into the Business Workspaces Folder
        self.goTo(self.classicBWFolder)

        # Initiating the Workflow
        self.clickOn("link_text", "BW WF")

        # Giving the Workflow (and subsequently the Workspace) Attributes
        self.switchIframe("//iframe[@id='iframeLeft']")
        self.clickOn("link_text", "Attributes")
        self.switchIframe()
        self.switchIframe("//iframe[@id='iframeRight']")

        # Text Field (Multilingual)
        self.clickOn("id", "_1_1_2_1Global")
        self.driver.find_element(By.ID, "mle__1_1_2_1_en_US").send_keys(f"WF EN {num}")
        self.driver.find_element(By.ID, "mle__1_1_2_1_fr").send_keys(f"WF FR {num}")
        self.clickOn("id", "mlEditBtnSave")

        # Text Popup
        Select(self.driver.find_element(By.ID, "_1_1_3_1")).select_by_index(3)

        # Text Multiline
        self.driver.find_element(By.ID, "_1_1_4_1").send_keys(f"TML{Keys.ENTER}Not multilingual")

        # Saving and Initiating
        self.clickOn("class_name", "applyButton")
        self.switchIframe()
        self.switchIframe("//iframe[@id='iframeLeft']")
        self.clickOn("class_name", "saveButton")
        self.switchIframe()
        self.clickOn("xpath", "//input[@name='processButton']")


        # Checking the Workspace Attributes

        # Starting in SDL
        if not self.SDL: self.changeLang("en")

        # Clicking into the Workspace
        self.clickOn("link_text", f"BW WF EN {num}")

        # Name
        val = self.getText("id", "otsapwkspPanel_panelTitle")
        if val != f"BW WF EN {num}":
            self.error("BW Name (WF Creation)", "SDL", f"BW WF EN {num}", val)
        
        # Text Field
        val = self.getText("xpath", "(//div[@class='xecmsap_attribute_value'])[1]")[2:-1]
        if val != f"WF EN {num}":
            self.error("Text Field", "SDL", f"WF EN {num}", val)
        
        # Text Popup
        val = self.getText("xpath", "(//div[@class='xecmsap_attribute_value'])[2]")[2:-1]
        if val != "three":
            self.error("Text Popup", "SDL", "three", val)
        
        # Text Multiline
        val = self.getText("xpath", "(//div[@class='xecmsap_attribute_value'])[3]")[2:-1]
        if val != "TML Not multilingual":
            self.error("Text Multiline", "SDL", "TML Not multilingual", val)

        # Switching to UDL Check
        self.changeLang("fr")

        # Name
        val = self.getText("id", "otsapwkspPanel_panelTitle")
        if val != f"BW WF FR {num}":
            self.error("BW Name (WF Creation)", "SDL", f"BW WF FR {num}", val)
        
        # Text Field
        val = self.getText("xpath", "(//div[@class='xecmsap_attribute_value'])[1]")[2:-1]
        if val != f"WF FR {num}":
            self.error("Text Field", "SDL", f"WF FR {num}", val)
        
        # Text Popup
        val = self.getText("xpath", "(//div[@class='xecmsap_attribute_value'])[2]")[2:-1]
        if val != "trois":
            self.error("Text Popup", "SDL", "trois", val)
        
        # Text Multiline
        val = self.getText("xpath", "(//div[@class='xecmsap_attribute_value'])[3]")[2:-1]
        if val != "TML Not multilingual":
            self.error("Text Multiline", "SDL", "TML Not multilingual", val)


        # Finishing Up
        self.changeLang("en")
        print(f"BW WF {num} passed.")
        if pause:
            self.askCont()
        return