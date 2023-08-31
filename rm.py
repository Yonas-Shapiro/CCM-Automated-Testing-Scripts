from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

from basics import basics

class recordsManagement(basics):

    # Init for Basic Information
    def __init__(self, VMnum):
        super().__init__(VMnum)

        self.rsi = "ll&objid=15758&objAction=ViewRSIs&viewType=1"
        self.classifications = "ll&objtype=198&objaction=browse"
        self.tableManagement = "RecMan.TableMaintenance"



    
    # Creating a Code
    def createCode(self, id, name, insideID, num, sdl, udl, translate):
        Select(self.driver.find_element(By.ID, id)).select_by_visible_text("<Create New Code>")
        self.switchWindow(True)

        # Name
        self.waitFor("id", insideID)
        self.driver.find_element(By.ID, insideID).send_keys(f"{name} {num}")

        # Description
        if not (sdl or udl): self.driver.find_element(By.ID, (insideID + "_Desc_E")).send_keys(f"{name} {num} Not ML")
        else:
            self.clickOn("id", (insideID + "_Desc_EGlobal"))
            if sdl: self.driver.find_element(By.ID, ("meta_" + insideID + "_Desc_E_en_US")).send_keys(f"{name} {num} EN")
            if udl and not translate: self.driver.find_element(By.ID, ("meta_" + insideID + "_Desc_E_fr")).send_keys(f"{name} {num} FR")
            self.clickOn("xpath", "//button[text()='OK']")

            # Translating if Necessary
            if translate:
                self.clickOn("xpath", "//button[@value='Translate']")
                Select(self.driver.find_element(By.ID, "srcLang")).select_by_value("en_US")
                Select(self.driver.find_element(By.ID, "destLang")).select_by_value("fr")
                self.clickOn("id", "atBtnXlate")
                if self.getText("id", (insideID + "_Desc_EDest")) != f"{name} {num} FR":
                    self.driver.find_element(By.ID, (insideID + "_Desc_EDest")).clear()
                    self.driver.find_element(By.ID, (insideID + "_Desc_EDest")).send_keys(f"{name} {num} FR")
                self.clickOn("id", "atBtnSave")
            
        # Saving the Code
        self.clickOn("xpath", "//input[@title='Submit']")
        self.switchWindow(False)

        return
    


    # Creating a Code (Table Maintenance)
    def tableCode(self, name, codename, num, infoSDL, infoUDL, insideID = None):

        # Getting the ID for Inside the Code
        if not insideID:
            insideID = name.upper()
        
        # Entering the Table
        self.goTo(self.tableManagement)
        self.clickOn("link_text", name)

        # Creating a New Code
        self.waitFor("id", "addItem")
        Select(self.driver.find_element(By.ID, "addItem")).select_by_index(1)

        # Code Name
        self.driver.find_element(By.ID, insideID).send_keys(f"{codename} {num}")

        # Description
        if not infoSDL and not infoUDL:
            self.driver.find_element(By.ID, f"{insideID}_Desc_E").send_keys(f"{codename} {num} NOT ML")
        else:
            self.clickOn("id", f"{insideID}_Desc_EGlobal")
            if infoSDL:
                self.driver.find_element(By.ID, f"meta_{insideID}_Desc_E_en_US")
            if infoUDL:
                self.driver.find_element(By.ID, f"meta_{insideID}_Desc_E_fr")
            self.clickOn("xpath", "//button[text()='OK']")

        # Special Cases

        # Hold Type
        if name == "Hold Type":
            self.driver.find_element(By.ID, "DefaultPeriod").send_keys(str(num))
        
        # RSI Retention Stage
        elif name == "RSI Retention Stage":
            self.driver.find_element(By.ID, "RetStageOrder").send_keys(str(num)*3)

        # Provenance Type
        elif name == "Provenance Type":
            if not infoSDL and not infoUDL:
                self.driver.find_element(By.ID, "provenanceTypeDesc_add").send_keys(f"Not ML {num}")
            else:
                self.clickOn("id", "provenanceTypeDesc_addGlobal")
                if infoSDL:
                    self.driver.find_element(By.ID, f"meta_{insideID}Desc_add_en_US").send_keys(f"EN {num}")
                if infoUDL:
                    self.driver.find_element(By.ID, f"meta_{insideID}Desc_add_fr").send_keys(f"FR {num}")
                self.clickOn("xpath", "//button[text()='OK']")

        # Saving the Code
        self.clickOn("xpath", "//input[@value='Submit']")
        self.waitFor("id", "addItem")


        # Checking the Code

        return

        






    # Creating a "Set" (RSI, RM, Folder)
    def createSet(self, num, inSDL, infoSDL = False, infoUDL = False, translate = False):

        # Starting in the Correct Language
        if inSDL and not self.SDL: self.changeLang("en")
        elif not inSDL and self.SDL: self.changeLang("fr")

        # Creating an RSI
        self.goTo(self.rsi)
        self.clickOn("link_text", "Add Item")
        self.clickOn("link_text", "RSI")


        # Adding the Information

        # Name
        self.waitFor("id", "rsiName")
        self.driver.find_element(By.ID, "rsiName").send_keys(f"RSI {num}")

        # If Pre-EMLC
        if not (infoSDL or infoUDL):
            # Title
            self.driver.find_element(By.ID, "title").send_keys(f"RSI {num}{Keys.ENTER}Title")
            # Description
            self.driver.find_element(By.ID, "description").send_keys(f"RSI {num}{Keys.ENTER}Description")
            # Subject
            self.driver.find_element(By.ID, "subject").send_keys(f"RSI {num}{Keys.ENTER}Subject")


        else:
            # Title
            self.clickOn("titleGlobal")
            if infoSDL:
                self.driver.find_element(By.ID, "meta_title_en_US").send_keys(f"RSI {num}{Keys.ENTER}Title{Keys.ENTER}EN")
            if infoUDL and not translate:
                self.driver.find_element(By.ID, "meta_title_fr").send_keys(f"RSI {num}{Keys.ENTER}Title{Keys.ENTER}FR")

            # Description
            self.clickOn("link_text", "Description")
            if infoSDL:
                self.driver.find_element(By.ID, "meta_description_en_US").send_keys(f"RSI {num}{Keys.ENTER}Description{Keys.ENTER}EN")
            if infoUDL and not translate:
                self.driver.find_element(By.ID, "meta_description_fr").send_keys(f"RSI {num}{Keys.ENTER}Description{Keys.ENTER}FR")

            # Subject
            self.clickOn("link_text", "Subject")
            if infoSDL:
                self.driver.find_element(By.ID, "meta_subject_en_US").send_keys(f"RSI {num}{Keys.ENTER}Subject{Keys.ENTER}EN")
            if infoUDL and not translate:
                self.driver.find_element(By.ID, "meta_subject_fr").send_keys(f"RSI {num}{Keys.ENTER}Subject{Keys.ENTER}FR")

            self.clickOn("xpath", "//button[text()='OK']")

        
        # Status
        self.createCode("status", "RS", "RSIStatus", num, infoSDL, infoSDL, translate)
        
        # Translating the RSI if Necessary
        if translate:
            self.clickOn("xpath", "//input[@value='Translate']")
            Select(self.driver.find_element(By.ID, "srcLang")).select_by_value("en_US")
            Select(self.driver.find_element(By.ID, "destLang")).select_by_value("fr")
            self.clickOn("id", "atBtnXlate")
            self.clickOn("id", "atBtnSave")
        
        # Saving the RSI
        self.clickOn("xpath", "//input[@title='Add']")
        self.waitFor("link_text", "Add Item")

        # Creating the RM Classification
        self.goTo(self.classifications)
        self.clickOn("link_text", "Add Item")
        self.clickOn("link_text", "RM Classification")

        # RM Classification Information
        if not (infoSDL or infoUDL):
            # Name
            self.driver.find_element(By.ID, "name").send_keys(f"RM {num}")
            # Description
            self.driver.find_element(By.ID, "comment").send_keys(f"RM {num}{Keys.ENTER}Description")
            # Disposition Authority
            self.driver.find_element(By.ID, "dispAuthority").send_keys(f"RM {num}")
            # Subject
            self.driver.find_element(By.ID, "subject").send_keys(f"RM {num}{Keys.ENTER}Subject")
            # Keywords
            self.driver.find_element(By.ID, "keywords").send_keys(f"RM {num}{Keys.ENTER}Key")

        else:
            # Multilingual Attributes
            self.clickOn("id", "nameGlobal")

            # Name
            if infoSDL: self.driver.find_element(By.ID, "meta_name_en_US").send_keys(f"RM {num} EN")
            if infoUDL and not translate: self.driver.find_element(By.ID, "meta_name_fr").send_keys(f"RM {num} FR")

            # Description
            self.clickOn("link_text", "Description")
            if infoSDL: self.driver.find_element(By.ID, "meta_comment_en_US").send_keys(f"RM {num}{Keys.ENTER}EN{Keys.ENTER}Comment")
            if infoUDL and not translate: self.driver.find_element(By.ID, "meta_comment_fr").send_keys(f"RM {num}{Keys.ENTER}FR{Keys.ENTER}Comment")

            # Disposition Authority
            self.clickOn("link_text", "Disposition Authority")
            if infoSDL: self.driver.find_element(By.ID, "meta_dispAuthority_en_US").send_keys(f"RM {num} EN")
            if infoUDL and not translate: self.driver.find_element(By.ID, "meta_name_fr").send_keys(f"RM {num} FR")

            # Subject
            self.clickOn("link_text", "Subject")
            if infoSDL: self.driver.find_element(By.ID, "meta_subject_en_US").send_keys(f"RM {num} EN Subject")
            if infoUDL and not translate: self.driver.find_element(By.ID, "meta_subject_fr").send_keys(f"RM {num} FR Subject")

            # Keywords
            self.clickOn("link_text", "Keywords")
            if infoSDL: self.driver.find_element(By.ID, "meta_keywords_en_US").send_keys(f"RM {num} EN Key")
            if infoUDL and not translate: self.driver.find_element(By.ID, "meta_keywords_fr").send_keys(f"RM {num} FR Key")



        # File Number
        self.driver.find_element(By.ID, "fileNumber").send_keys(f"{num}0001")

        # Codes
        self.createCode("status", "RMS", "FILE_STATUS", num, infoSDL, infoUDL, translate)
        self.createCode("essential", "ESS", "ESS_RECORDS", num, infoSDL, infoUDL, translate)
        self.createCode("storage", "STM", "STORAGE", num, infoSDL, infoUDL, translate)

        # Cycle Period Dropdown
        Select(self.driver.find_element(By.ID, "vitalRecordCycle")).select_by_index(num)

        # Selecting the Associated RSI
        Select(self.driver.find_element(By.ID, "selectRSI")).select_by_visible_text("Search RSI's")
        self.switchWindow(True)
        #self.waitFor("xpath", f"(//a[text()='Select >'])[{num}]")
        self.clickOn("xpath", f"(//a[text()='Select >'])[{num}]")
        self.switchWindow(False)


        # Translating if necessary
        if translate:

            # Translating
            self.clickOn("xpath", "//input[@value='Translate']")
            Select(self.driver.find_element(By.ID, "srcLang")).select_by_value("en_US")
            Select(self.driver.find_element(By.ID, "destLang")).select_by_value("fr")
            self.clickOn("id", "atBtnXlate")
            self.askCont()

            # Checking if "EN" translated to "FR"
            if not "FR" in self.getText("id", "nameDest"):
                self.replaceText("id", "nameDest", "EN", "FR")
            if not "FR" in self.getText("id", "commentDest"):
                self.replaceText("id", "commentDest", "EN", "FR")
            if not "FR" in self.getText("id", "dispAuthorityDest"):
                self.replaceText("id", "dispAuthorityDest", "EN", "FR")
            if not "FR" in self.getText("id", "subjectDest"):
                self.replaceText("id", "subjectDest", "EN", "FR")
            if not "FR" in self.getText("id", "keywordsDest"):
                self.replaceText("id", "keywordsDest", "EN", "FR")

            # Closing the Translate Popup
            self.clickOn("id", "atBtnSave")
            

        # Saving the RM Classification
        self.clickOn("id", "addButton")



        # Creating the Folder
        self.goTo()
        self.clickOn("link_text", "Add Item")
        self.clickOn("link_text", "Folder")

        # Name + Description
        # Pre-EMLC
        if not (infoSDL or infoUDL):
            self.driver.find_element(By.ID, "name").send_keys(f"F{num}")
            self.driver.find_element(By.ID, "comment").send_keys(f"F{num}{Keys.ENTER}Description")
        # Post EMLC
        else:
            # Name
            self.clickOn("id", "nameGlobal")
            if infoSDL: self.driver.find_element(By.ID, "meta_name_en_US").send_keys(f"F{num} EN")
            if infoUDL: self.driver.find_element(By.ID, "meta_name_fr").send_keys(f"F{num} FR")

            # Description
            self.clickOn("link_text", "Description")
            if infoSDL: self.driver.find_element(By.ID, "meta_comment_en_US").send_keys(f"F{num}{Keys.ENTER}EN{Keys.ENTER}Description")
            if infoUDL: self.driver.find_element(By.ID, "meta_comment_fr").send_keys(f"F{num}{Keys.ENTER}EN{Keys.ENTER}Description")

            # Saving the ML Information
            self.clickOn("xpath", "//button[text()='OK']")

        # Adding the RM Classification
        Select(self.driver.find_element(By.XPATH, "//select[@name='selectClassify']")).select_by_visible_text("Browse Classifications")
        self.switchWindow(True)
        val = num + 1
        self.clickOn("xpath", f"(//input[@value='CheckBox'])[{val}]")
        self.clickOn("xpath", "//input[@name='submit']")
        self.switchWindow(False)
        time.sleep(2.5)

        # Saving the Folder
        self.clickOn("id", "addButton")


        # Verifying the Information
        
        # Classic View First (SDL)
        if not self.SDL: self.changeLang("en")
        self.goTo()

        # Getting to the Classifications Tab
        self.clickOn("xpath", f"(//img[@title='Click to see Record Details'])[{num}]")


        # Checking the Information

        # File Status
        val = Select(self.driver.find_element(By.ID, "fileStatus")).first_selected_option.text
        if not infoSDL and not infoUDL:
            if f"RMS {num} NOT ML" not in val:
                self.error(f"F{num} Classic View RM Info", "SDL", f"RMS {num} NOT ML", val)
        elif infoSDL:
            if f"RMS {num} EN" not in val:
                self.error(f"F{num} Classic View RM Info", "SDL", f"RMS {num} EN", val)
        else:
            if f"RMS {num} FR" not in val:
                self.error(f"F{num} Classic View RM Info", "SDL", f"RMS {num} FR", val)
        
        # Essential
        val = Select(self.driver.find_element(By.ID, "essential")).first_selected_option.text
        if not infoSDL and not infoUDL:
            if f"ESS {num} NOT ML" not in val:
                self.error(f"F{num} Classic View RM Info", "SDL", f"ESS {num} NOT ML", val)
        elif infoSDL:
            if f"ESS {num} EN" not in val:
                self.error(f"F{num} Classic View RM Info", "SDL", f"ESS {num} EN", val)
        else:
            if f"ESS {num} FR" not in val:
                self.error(f"F{num} Classic View RM Info", "SDL", f"ESS {num} FR", val)

        # Storage Medium
        val = Select(self.driver.find_element(By.ID, "storage")).first_selected_option.text
        if not infoSDL and not infoUDL:
            if f"STM {num} NOT ML" not in val:
                self.error(f"F{num} Classic View RM Info", "SDL", f"STM {num} NOT ML", val)
        elif infoSDL:
            if f"STM {num} EN" not in val:
                self.error(f"F{num} Classic View RM Info", "SDL", f"STM {num} EN", val)
        else:
            if f"STM {num} FR" not in val:
                self.error(f"F{num} Classic View RM Info", "SDL", f"STM {num} FR", val)

        # RSI
        val = self.getAtt("xpath", "//input[contains(@id, 'rsi')]", "value")
        if f"RSI {num}" not in val:
            self.error(f"F{num} Classic View RM Info", "SDL", f"RSI {num}", val)

        # File Number
        val = self.getText("xpath", "//td[@class='valueStatic']")
        if val != f"{num}0001":
            self.error(f"F{num} Classic View RM Info", "SDL", f"{num}0001", val)


        # UDL
        self.changeLang("fr")

        # File Status
        val = Select(self.driver.find_element(By.ID, "fileStatus")).first_selected_option.text
        if not infoSDL and not infoUDL:
            if f"RMS {num} NOT ML" not in val:
                self.error(f"F{num} Classic View RM Info", "UDL", f"RMS {num} NOT ML", val)
        elif infoUDL:
            if f"RMS {num} FR" not in val:
                self.error(f"F{num} Classic View RM Info", "UDL", f"RMS {num} EN", val)
        else:
            if f"RMS {num} EN" not in val:
                self.error(f"F{num} Classic View RM Info", "UDL", f"RMS {num} FR", val)
        
        # Essential
        val = Select(self.driver.find_element(By.ID, "essential")).first_selected_option.text
        if not infoSDL and not infoUDL:
            if f"ESS {num} NOT ML" not in val:
                self.error(f"F{num} Classic View RM Info", "UDL", f"ESS {num} NOT ML", val)
        elif infoUDL:
            if f"ESS {num} FR" not in val:
                self.error(f"F{num} Classic View RM Info", "UDL", f"ESS {num} FR", val)
        else:
            if f"ESS {num} EN" not in val:
                self.error(f"F{num} Classic View RM Info", "UDL", f"ESS {num} EN", val)

        # Storage Medium
        val = Select(self.driver.find_element(By.ID, "storage")).first_selected_option.text
        if not infoSDL and not infoUDL:
            if f"STM {num} NOT ML" not in val:
                self.error(f"F{num} Classic View RM Info", "UDL", f"STM {num} NOT ML", val)
        elif infoUDL:
            if f"STM {num} FR" not in val:
                self.error(f"F{num} Classic View RM Info", "UDL", f"STM {num} FR", val)
        else:
            if f"STM {num} EN" not in val:
                self.error(f"F{num} Classic View RM Info", "UDL", f"STM {num} EN", val)

        # RSI
        val = self.getAtt("xpath", "//input[contains(@id, 'rsi')]", "value")
        if f"RSI {num}" not in val:
            self.error(f"F{num} Classic View RM Info", "UDL", f"RSI {num}", val)

        # File Number
        val = self.getText("xpath", "//td[@class='valueStatic']")
        if val != f"{num}0001":
            self.error(f"F{num} Classic View RM Info", "UDL", f"{num}0001", val)
        

        # Smart View
        self.driver.get(self.smartHome)
        self.clickOn("xpath", f"(//span[@title='View Record details'])[{num}]")

        # Status
        val = self.getText("xpath", "(//div[@class='btn-container'])[13]")
        if not infoSDL and not infoUDL:
            if f"RMS {num} NOT ML" not in val:
                self.error(f"F{num} Smart View RM Info", "UDL", f"RMS {num} NOT ML", val)
        elif infoUDL:
            if f"RMS {num} FR" not in val:
                self.error(f"F{num} Smart View RM Info", "UDL", f"RMS {num} EN", val)
        else:
            if f"RMS {num} EN" not in val:
                self.error(f"F{num} Smart View RM Info", "UDL", f"RMS {num} FR", val)
        
        # Essential
        val = self.getText("xpath", "(//div[@class='btn-container'])[16]")
        if not infoSDL and not infoUDL:
            if f"ESS {num} NOT ML" not in val:
                self.error(f"F{num} Smart View RM Info", "UDL", f"ESS {num} NOT ML", val)
        elif infoUDL:
            if f"ESS {num} FR" not in val:
                self.error(f"F{num} Smart View RM Info", "UDL", f"ESS {num} FR", val)
        else:
            if f"ESS {num} EN" not in val:
                self.error(f"F{num} Smart View RM Info", "UDL", f"ESS {num} EN", val)

        # Storage Medium
        val = self.getText("xpath", "(//div[@class='btn-container'])[20]")
        if not infoSDL and not infoUDL:
            if f"STM {num} NOT ML" not in val:
                self.error(f"F{num} Smart View RM Info", "UDL", f"STM {num} NOT ML", val)
        elif infoUDL:
            if f"STM {num} FR" not in val:
                self.error(f"F{num} Smart View RM Info", "UDL", f"STM {num} FR", val)
        else:
            if f"STM {num} EN" not in val:
                self.error(f"F{num} Smart View RM Info", "UDL", f"STM {num} EN", val)

        # RSI
        val = self.getText("xpath", "(//div[@class='btn-container'])[11]")
        if f"RSI {num}" != val:
            self.error(f"F{num} Smart View RM Info", "UDL", f"RSI {num}", val)

        # File Number
        val = self.getText("xpath", "(//div[@class='btn-container'])[10]")
        if str(val) != f"{num}0001":
            self.error(f"F{num} Smart View RM Info", "UDL", f"{num}0001", val)


        # SDL Smart View
        self.driver.get(self.smartHome)
        self.clickOn("xpath", f"(//span[@title='View Record details'])[{num}]")

        # Status
        val = self.getText("xpath", "(//div[@class='btn-container'])[13]")
        if not infoSDL and not infoUDL:
            if f"RMS {num} NOT ML" not in val:
                self.error(f"F{num} Smart View RM Info", "SDL", f"RMS {num} NOT ML", val)
        elif infoSDL:
            if f"RMS {num} EN" not in val:
                self.error(f"F{num} Smart View RM Info", "SDL", f"RMS {num} EN", val)
        else:
            if f"RMS {num} FR" not in val:
                self.error(f"F{num} Smart View RM Info", "SDL", f"RMS {num} FR", val)
        
        # Essential
        val = self.getText("xpath", "(//div[@class='btn-container'])[16]")
        if not infoSDL and not infoUDL:
            if f"ESS {num} NOT ML" not in val:
                self.error(f"F{num} Smart View RM Info", "SDL", f"ESS {num} NOT ML", val)
        elif infoSDL:
            if f"ESS {num} EN" not in val:
                self.error(f"F{num} Smart View RM Info", "SDL", f"ESS {num} EN", val)
        else:
            if f"ESS {num} FR" not in val:
                self.error(f"F{num} Smart View RM Info", "SDL", f"ESS {num} FR", val)

        # Storage Medium
        val = self.getText("xpath", "(//div[@class='btn-container'])[20]")
        if not infoSDL and not infoUDL:
            if f"STM {num} NOT ML" not in val:
                self.error(f"F{num} Smart View RM Info", "SDL", f"STM {num} NOT ML", val)
        elif infoSDL:
            if f"STM {num} EN" not in val:
                self.error(f"F{num} Smart View RM Info", "SDL", f"STM {num} EN", val)
        else:
            if f"STM {num} FR" not in val:
                self.error(f"F{num} Smart View RM Info", "SDL", f"STM {num} FR", val)

        # RSI
        val = self.getText("xpath", "(//div[@class='btn-container'])[11]")
        if f"RSI {num}" != val:
            self.error(f"F{num} Smart View RM Info", "SDL", f"RSI {num}", val)

        # File Number
        val = self.getText("xpath", "(//div[@class='btn-container'])[10]")
        if str(val) != f"{num}0001":
            self.error(f"F{num} Smart View RM Info", "SDL", f"{num}0001", val)

        
        # Printing a Success Message
        print(f"RM Group {num} Passed.")
        return
    



    # Table Run
    def tableRun(self, inSDL, num, infoSDL=False, infoUDL=False):

        # Starting in the Correct Language
        if inSDL and not self.SDL: self.changeLang("en")
        elif not inSDL and self.SDL: self.changeLang("fr")

        # Running the Codes
        self.tableCode("Accession", "ACC", num, infoSDL, infoUDL)
        self.tableCode("Disposition", "DIS", num, infoSDL, infoUDL)
        self.tableCode("Essential Record", "ER", num, infoSDL, infoUDL, "ESS_RECORDS")
        self.tableCode("Hold Type", "HT", num, infoSDL, infoUDL, "HoldType")
        self.tableCode("Jurisdiction", "JSD", num, infoSDL, infoUDL, "JurisdCode")
        self.tableCode("Provenance Type", "PVT", num, infoSDL, infoUDL, "ProvenanceType")
        self.tableCode("RSI Retention", "RSIR", num, infoSDL, infoUDL, "RetCode")
        self.tableCode("RSI Retention Stage", "RSIRS", num, infoSDL, infoUDL, "RetStage")
        self.tableCode("RSI Rule", "RR", num, infoSDL, infoUDL, "RSIRuleCode")
        self.tableCode("RSI Status", "RSIS", num, infoSDL, infoUDL, "RSIStatus")
        self.tableCode("Status", "STAT", num, infoSDL, infoUDL, "FILE_STATUS")
        self.tableCode("Storage Medium", "SM", num, infoSDL, infoUDL, "STORAGE")

        # Printing Success Message
        print("Table Run Passed.")
        return