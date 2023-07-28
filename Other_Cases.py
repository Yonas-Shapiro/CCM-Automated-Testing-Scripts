from bw import businessWorkspace
import time

#
VMnum = input("Which VM are you running?\n")
thisSession = businessWorkspace(VMnum)



#thisSession.changeLang("fr")
#thisSession.getTitle()
#thisSession.changeLang("en")
thisSession.multilingualizeWorkspace()
#thisSession.createBW(1, False, 1, 1, 1, 1, 1)

thisSession.quit()
del thisSession