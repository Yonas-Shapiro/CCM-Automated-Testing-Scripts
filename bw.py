from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time

from session import session

class classicBW(session):
    def __init__(self, num, SDL, nameSDL, nameUDL, attSDL, attUDL, VMnum):
        if int(num) < 10:
            self.name = "BW 0" + str(num)
        else:
            self.name = "BW " + str (num)
        self.SDL = SDL; self.sdlName = nameSDL; self.udlName = nameUDL; self.sdlAtts = attSDL;  self.udlAtts = attUDL
        self.VMnum = super().VMnum
        self.create()
    
    def create(self):
